//+------------------------------------------------------------------+
//| GrabarTicksFTMO.mq5                                              |
//| Bot v3 - rama trabajo/f17-ordenes (2026-11-26)                   |
//|                                                                  |
//| F17, el grabador (ADR-0099 §5): graba los ticks de EURUSD del    |
//| servidor de la demo de FTMO (time_msc, bid, ask, flags), un CSV  |
//| por hora del servidor, F17G_<AAAA-MM-DD>_<HH>.csv en MQL5/Files, |
//| escrito de forma atomica (se escribe en .part y se renombra al   |
//| cerrar la hora). Lo lee scripts/leer_ordenes_f17.py (grabador).  |
//| Instrucciones: docs/runbooks/F17-ORDENES.md.                     |
//|                                                                  |
//| SOLO LEE (tests/contract/test_grabar_ticks_ftmo.py):             |
//| - no llama a ninguna funcion de trading ni de ordenes;           |
//| - se niega a correr si la cuenta no es DEMO, con la condicion    |
//|   de MedirDemoFTMO.mq5:759; solo EURUSD;                         |
//| - la primera vez empieza al inicio de la hora en que se lanza,   |
//|   nunca en «el primer tick disponible»; al relanzarlo, rehace    |
//|   desde la hora siguiente al ultimo CSV entero, del servidor.    |
//|                                                                  |
//| Lo que da por supuesto de MT5 (ADR-0082 D7), de la documentacion |
//| de MQL5 (F17-ORDENES.md, 0.3): CopyTicks desde un time_msc y     |
//| CopyTicksRange con los dos bordes dentro; FileMove sin           |
//| FILE_REWRITE no sobrescribe; IsStopped. POR MEDIR en la corrida: |
//| hasta donde guarda el servidor los ticks hacia atras (el control |
//| dice cuantos da cada hora rehecha) y que un script no vuelve     |
//| solo tras reiniciar el terminal (el runbook dice que se relanza).|
//+------------------------------------------------------------------+
#property copyright "Bot v3"
#property version   "1.00"
#property description "Graba los ticks de EURUSD de una cuenta DEMO, un CSV por hora del servidor. No opera."

#define VERSION_SCRIPT "1.0"
#define SIMBOLO        "EURUSD"
#define PREFIJO        "F17G_"
#define PAUSA_MS       1000
#define INTENTOS       3
#define LOTE_TICKS     2000
#define HORA_S         3600
// al relanzarlo, cuanto atras rehace como mucho: un fin de semana y una noche (arreglo 2)
#define MAX_HORAS_REHACER 72

int      g_control  = INVALID_HANDLE;
int      g_part     = INVALID_HANDLE;
int      g_digits   = 5;
datetime g_hora     = 0;  // la hora del servidor que se esta escribiendo (su inicio)
long     g_ultimo   = 0;  // el time_msc del ultimo tick escrito
int      g_repetidos = 0; // cuantos ticks con ese mismo time_msc se han escrito ya
int      g_en_hora  = 0;  // ticks escritos en la hora en curso

//+------------------------------------------------------------------+
//| Utilidades                                                       |
//+------------------------------------------------------------------+
string Campo(const string texto)
  {
   string t = texto;
   StringReplace(t, "\"", "\"\"");
   return "\"" + t + "\"";
  }

void Control(const string clave, const string valor, const string nota = "")
  {
   FileWriteString(g_control, Campo(clave) + "," + Campo(valor) + "," + Campo(nota) + "\r\n");
   FileFlush(g_control);
  }

datetime InicioDeLaHora(const datetime t)
  {
   return t - t % HORA_S;
  }

string NombreDeLaHora(const datetime hora)
  {
   MqlDateTime s;
   TimeToStruct(hora, s);
   return StringFormat("%s%04d-%02d-%02d_%02d", PREFIJO, s.year, s.mon, s.day, s.hour);
  }

// La hora de un nombre F17G_AAAA-MM-DD_HH.csv; 0 si no es de esos.
datetime HoraDelNombre(const string nombre)
  {
   if(StringLen(nombre) != StringLen(PREFIJO) + 17 || StringFind(nombre, PREFIJO) != 0 ||
      StringSubstr(nombre, StringLen(nombre) - 4) != ".csv")
      return 0;
   string f = StringSubstr(nombre, StringLen(PREFIJO), 10);
   StringReplace(f, "-", ".");
   string h = StringSubstr(nombre, StringLen(PREFIJO) + 11, 2);
   return StringToTime(f + " " + h + ":00");
  }

string Linea(const MqlTick &t)
  {
   return IntegerToString(t.time_msc) + "," + DoubleToString(t.bid, g_digits) + "," +
          DoubleToString(t.ask, g_digits) + "," + IntegerToString(t.flags) + "\r\n";
  }

//+------------------------------------------------------------------+
//| La negativa                                                      |
//+------------------------------------------------------------------+
bool Comprobaciones(string &motivo)
  {
   if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)
     {
      motivo = "la cuenta NO es DEMO: el script no hace nada";
      return false;
     }
   if(!SymbolSelect(SIMBOLO, true))
     {
      motivo = "no existe el simbolo EURUSD en esta cuenta";
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
//| Una hora entera, de forma atomica: .part y FileMove              |
//+------------------------------------------------------------------+
// Cierra la hora en curso: su .part pasa a .csv (FILE_REWRITE) y el control lo apunta.
void CerrarHora()
  {
   if(g_part == INVALID_HANDLE)
      return;
   FileClose(g_part);
   g_part = INVALID_HANDLE;
   string base = NombreDeLaHora(g_hora);
   bool movido = FileMove(base + ".part", 0, base + ".csv", FILE_REWRITE);
   Control("hora_" + StringSubstr(base, StringLen(PREFIJO)) + "_ticks", IntegerToString(g_en_hora),
           movido ? "grabada" : "NO SE PUDO RENOMBRAR (error " + IntegerToString(GetLastError()) + ")");
   Control("hora_" + StringSubstr(base, StringLen(PREFIJO)) + "_desfase_servidor_gmt_min",
           IntegerToString((int)((TimeTradeServer() - TimeGMT()) / 60)), "al cerrarla");
  }

bool AbrirHora(const datetime hora)
  {
   g_hora = hora;
   g_en_hora = 0;
   g_part = FileOpen(NombreDeLaHora(hora) + ".part", FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(g_part == INVALID_HANDLE)
      return false;
   FileWriteString(g_part, "time_msc,bid,ask,flags\r\n");
   return true;
  }

void Escribir(const MqlTick &t)
  {
   datetime hora = InicioDeLaHora((datetime)(t.time_msc / 1000));
   if(hora < g_hora || (hora == g_hora && g_part == INVALID_HANDLE))
     {
      // un tick de una hora ya cerrada: no se reabre su fichero (lo truncaria); se cuenta
      Control("tick_tarde", IntegerToString(t.time_msc), "de una hora ya cerrada: no se escribe");
      return;
     }
   if(hora != g_hora)
     {
      CerrarHora();
      AbrirHora(hora);
     }
   if(g_part == INVALID_HANDLE)
      return;
   FileWriteString(g_part, Linea(t));
   g_en_hora++;
   if(t.time_msc == g_ultimo)
      g_repetidos++;
   else
     {
      g_ultimo = t.time_msc;
      g_repetidos = 1;
     }
  }

// Rehace del servidor la hora `hora` entera (CopyTicksRange) y la deja en su .csv.
void RehacerHora(const datetime hora)
  {
   MqlTick ticks[];
   int n = -1, error = 0, intento = 0;
   for(intento = 1; intento <= INTENTOS; intento++)
     {
      ResetLastError();
      n = CopyTicksRange(SIMBOLO, ticks, COPY_TICKS_ALL, (ulong)hora * 1000, ((ulong)hora + HORA_S) * 1000 - 1);
      error = GetLastError();
      if(n >= 0 && error == 0)
         break;
      Sleep(PAUSA_MS);
     }
   string clave = "rehecha_" + StringSubstr(NombreDeLaHora(hora), StringLen(PREFIJO));
   // una hora sin ticks en sabado o domingo del servidor es el mercado cerrado, no un hueco
   // (revision del consultor, arreglo 5)
   MqlDateTime s;
   TimeToStruct(hora, s);
   bool fin_de_semana = (s.day_of_week == 0 || s.day_of_week == 6);
   string vacia = fin_de_semana ? "mercado_cerrado" : "HUECO: el servidor no devuelve ticks de esa hora";
   Control(clave + "_ticks", IntegerToString(n), n <= 0 ? vacia : "");
   Control(clave + "_error", IntegerToString(error));
   Control(clave + "_intentos", IntegerToString(MathMin(intento, INTENTOS)));
   if(n <= 0)
      return;
   AbrirHora(hora);
   for(int i = 0; i < n; i++)
      Escribir(ticks[i]);
   CerrarHora();
  }

// La hora siguiente al ultimo .csv entero; 0 si no hay ninguno (primera vez).
datetime SiguienteAlUltimo()
  {
   datetime ultima = 0;
   string nombre = "";
   long h = FileFindFirst(PREFIJO + "*.csv", nombre);
   if(h == INVALID_HANDLE)
      return 0;
   do
     {
      datetime t = HoraDelNombre(nombre);
      if(t > ultima)
         ultima = t;
     }
   while(FileFindNext(h, nombre));
   FileFindClose(h);
   return (ultima == 0) ? 0 : ultima + HORA_S;
  }

// Borra los .part de una ejecucion anterior: su hora se rehace del servidor.
void BorrarPartes()
  {
   string nombre = "";
   long h = FileFindFirst(PREFIJO + "*.part", nombre);
   if(h == INVALID_HANDLE)
      return;
   do
     {
      if(FileDelete(nombre))
         Control("parte_borrada", nombre, "se rehace del servidor");
     }
   while(FileFindNext(h, nombre));
   FileFindClose(h);
  }

//+------------------------------------------------------------------+
//| OnStart                                                          |
//+------------------------------------------------------------------+
void OnStart()
  {
   string motivo = "";
   if(!Comprobaciones(motivo))
     {
      Alert("GrabarTicksFTMO: ", motivo);
      return;
     }
   g_digits = (int)SymbolInfoInteger(SIMBOLO, SYMBOL_DIGITS);
   MqlDateTime s;
   TimeToStruct(TimeCurrent(), s);
   string nombre = StringFormat("%scontrol_%04d%02d%02d_%02d%02d%02d.csv", PREFIJO, s.year, s.mon, s.day, s.hour,
                                s.min, s.sec);
   g_control = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(g_control == INVALID_HANDLE)
     {
      Alert("GrabarTicksFTMO: no se pudo crear ", nombre, " (error ", GetLastError(), ")");
      return;
     }
   FileWriteString(g_control, "clave,valor,nota\r\n");
   Control("version_script", VERSION_SCRIPT);
   Control("cuenta_demo", "si");
   // para saber de que prueba es cada grabacion (arreglo 2); el CSV vive fuera de git y el login no
   // se copia a ningun manifiesto ni informe: el repositorio es publico
   Control("login", IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)), "no se copia al repositorio");
   Control("servidor", AccountInfoString(ACCOUNT_SERVER));
   Control("empresa", AccountInfoString(ACCOUNT_COMPANY));
   Control("build", IntegerToString(TerminalInfoInteger(TERMINAL_BUILD)));
   Control("digits", IntegerToString(g_digits));
   Control("time_trade_server_s", IntegerToString((long)TimeTradeServer()));
   Control("time_current_s", IntegerToString((long)TimeCurrent()), "hora del ultimo tick recibido");
   Control("time_gmt_s", IntegerToString((long)TimeGMT()), "sale del reloj del ordenador: tiene que estar en hora");
   Control("desfase_servidor_gmt_min", IntegerToString((int)((TimeTradeServer() - TimeGMT()) / 60)));

   BorrarPartes();
   datetime ahora = InicioDeLaHora(TimeCurrent());
   datetime desde = SiguienteAlUltimo();
   if(desde == 0)
     {
      desde = ahora; // la primera vez: el inicio de la hora en que se lanza
      Control("inicio", "primera_vez", "desde el inicio de la hora en que se lanza");
     }
   else if(desde < ahora - MAX_HORAS_REHACER * HORA_S)
     {
      // mas atras de MAX_HORAS_REHACER (seguramente los CSV de una prueba anterior): no se rehace
      // nada y se empieza como la primera vez (revision del consultor, arreglo 2)
      Control("hueco_largo", IntegerToString((long)((ahora - desde) / HORA_S)),
              "horas entre la siguiente al ultimo CSV y ahora: mas de MAX_HORAS_REHACER, no se rehacen");
      desde = ahora;
      Control("inicio", "primera_vez", "desde el inicio de la hora en que se lanza (tras un hueco largo)");
     }
   else
      Control("inicio", "relanzado", "rehace del servidor desde la hora siguiente al ultimo CSV entero");
   for(datetime h = desde; h < ahora; h += HORA_S)
      RehacerHora(h);

   // la hora en curso, desde su inicio, y despues en bucle
   g_ultimo = (long)ahora * 1000;
   g_repetidos = 0;
   g_hora = 0;
   while(!IsStopped())
     {
      MqlTick ticks[];
      ResetLastError();
      long desde_msc = g_ultimo;
      int ya = g_repetidos;
      int n = CopyTicks(SIMBOLO, ticks, COPY_TICKS_ALL, (ulong)desde_msc, LOTE_TICKS);
      int saltados = 0;
      for(int i = 0; i < n; i++)
        {
         // los del mismo milisegundo que el ultimo escrito ya estan escritos: se saltan `ya`
         if(ticks[i].time_msc == desde_msc && saltados < ya)
           {
            saltados++;
            continue;
           }
         if(ticks[i].time_msc < desde_msc)
            continue;
         Escribir(ticks[i]);
        }
      // la hora del servidor ya paso (con un minuto de margen, porque TimeCurrent puede ser de otro
      // simbolo): se cierra la que estaba abierta aunque no lleguen mas ticks
      if(g_part != INVALID_HANDLE && TimeCurrent() >= g_hora + HORA_S + 60)
         CerrarHora();
      if(n < LOTE_TICKS)
         Sleep(PAUSA_MS);
     }
   // parado: la hora en curso queda en .part y se rehace al relanzarlo
   if(g_part != INVALID_HANDLE)
     {
      FileClose(g_part);
      g_part = INVALID_HANDLE;
     }
   Control("terminado", "si", "la hora en curso queda en .part y se rehace al relanzarlo");
   FileClose(g_control);
   g_control = INVALID_HANDLE;
  }
//+------------------------------------------------------------------+
