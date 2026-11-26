//+------------------------------------------------------------------+
//| ExportarTicksFTMO.mq5                                            |
//| Bot v3 - rama trabajo/f17-historial (2026-11-26)                 |
//|                                                                  |
//| Exporta el HISTORIAL de ticks de EURUSD que el servidor de la    |
//| demo de FTMO ya guarda (F17, ADR-0099 §5), un dia por CSV, con   |
//| la M1 del propio servidor, y un CSV de control con los relojes.  |
//| Escribe en MQL5/Files con el prefijo F17_. Lo lee                |
//| scripts/leer_historial_f17.py con el criterio pre-registrado de  |
//| docs/plan/F17-HISTORIAL.yaml. Instrucciones:                     |
//| docs/runbooks/F17-HISTORIAL.md.                                  |
//|                                                                  |
//| SOLO LEE (tests/contract/test_exportar_ticks_ftmo.py):           |
//| - no llama a ninguna funcion de trading ni de ordenes;           |
//| - se niega a correr si la cuenta no es DEMO, con la condicion    |
//|   de MedirDemoFTMO.mq5:759;                                      |
//| - solo EURUSD, y solo dias de los meses de construccion          |
//|   (MESES_CONSTRUCCION, la lista de criterio_fidelidad.yaml): si  |
//|   un dia del rango pedido es de otro mes, sale sin pedir nada.   |
//|                                                                  |
//| Lo que da por supuesto de MT5 (ADR-0082 D7): los limites del     |
//| rango de CopyTicksRange (>= from_msc, <= to_msc) y COPY_TICKS_ALL|
//| salen de la documentacion de MQL5 (docs/series/copyticksrange);  |
//| en que reloj van time_msc y las barras, si la M1 es BID y si los |
//| ticks son los guardados queda POR MEDIR en la corrida: el lector |
//| lo contrasta con el control y con los puntos (c) y (d).          |
//+------------------------------------------------------------------+
#property copyright "Bot v3"
#property version   "1.00"
#property description "Exporta el historial de ticks y la M1 de EURUSD del servidor de una cuenta DEMO, solo de los meses de construccion. No opera."
#property script_show_inputs

#define VERSION_SCRIPT "1.0"
#define SIMBOLO        "EURUSD"
#define INTENTOS       3
#define PAUSA_MS       1000

// la lista de construccion de knowledge/cases/criterio_fidelidad.yaml; un test exige que sea esa
string MESES_CONSTRUCCION[] = {"2026-01", "2026-04", "2026-07", "2026-08"};

input string InpDesde = "2026.04.01"; // primer dia, en la fecha del servidor (AAAA.MM.DD)
input string InpHasta = "2026.04.30"; // ultimo dia, incluido

int g_control = INVALID_HANDLE;
int g_digits  = 5;

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

string Mes(const datetime t)
  {
   MqlDateTime s;
   TimeToStruct(t, s);
   return StringFormat("%04d-%02d", s.year, s.mon);
  }

string Dia(const datetime t)
  {
   MqlDateTime s;
   TimeToStruct(t, s);
   return StringFormat("%04d-%02d-%02d", s.year, s.mon, s.day);
  }

bool EsDeConstruccion(const datetime t)
  {
   string mes = Mes(t);
   for(int i = 0; i < ArraySize(MESES_CONSTRUCCION); i++)
      if(MESES_CONSTRUCCION[i] == mes)
         return true;
   return false;
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

// Todos los dias de [desde, hasta] tienen que ser de construccion: se comprueba ANTES de pedir
// nada al servidor (heredado 6: febrero no se toca ni se descarga).
bool RangoDeConstruccion(const datetime desde, const datetime hasta, string &motivo)
  {
   if(desde <= 0 || hasta < desde)
     {
      motivo = "el rango de fechas no se entiende: " + InpDesde + " a " + InpHasta;
      return false;
     }
   for(datetime d = desde; d <= hasta; d += 86400)
      if(!EsDeConstruccion(d))
        {
         motivo = "el dia " + Dia(d) + " no es de un mes de construccion: no se pide nada";
         return false;
        }
   return true;
  }

//+------------------------------------------------------------------+
//| Un dia: ticks y M1 del servidor                                  |
//+------------------------------------------------------------------+
int ExportarTicks(const datetime dia, int &intentos, int &error, long &primero, long &ultimo)
  {
   MqlTick ticks[];
   ulong desde_ms = (ulong)dia * 1000;
   ulong hasta_ms = ((ulong)dia + 86400) * 1000 - 1;
   int n = -1;
   for(intentos = 1; intentos <= INTENTOS; intentos++)
     {
      ResetLastError();
      n = CopyTicksRange(SIMBOLO, ticks, COPY_TICKS_ALL, desde_ms, hasta_ms);
      error = GetLastError();
      if(n >= 0 && error == 0)
         break;
      Sleep(PAUSA_MS);
     }
   if(intentos > INTENTOS)
      intentos = INTENTOS;
   primero = 0;
   ultimo = 0;
   if(n <= 0)
      return n;
   string nombre = "F17_" + Dia(dia) + "_ticks.csv";
   int f = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(f == INVALID_HANDLE)
      return -1;
   FileWriteString(f, "time_msc,bid,ask,flags\r\n");
   for(int i = 0; i < n; i++)
      FileWriteString(f, IntegerToString(ticks[i].time_msc) + "," + DoubleToString(ticks[i].bid, g_digits) +
                      "," + DoubleToString(ticks[i].ask, g_digits) + "," + IntegerToString(ticks[i].flags) + "\r\n");
   FileClose(f);
   primero = ticks[0].time_msc;
   ultimo = ticks[n - 1].time_msc;
   return n;
  }

int ExportarM1(const datetime dia)
  {
   MqlRates velas[];
   ResetLastError();
   int n = CopyRates(SIMBOLO, PERIOD_M1, dia, dia + 86399, velas);
   if(n <= 0)
      return n;
   string nombre = "F17_" + Dia(dia) + "_m1.csv";
   int f = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(f == INVALID_HANDLE)
      return -1;
   FileWriteString(f, "time,open,high,low,close,tick_volume,spread,real_volume\r\n");
   for(int i = 0; i < n; i++)
      FileWriteString(f, IntegerToString((long)velas[i].time) + "," + DoubleToString(velas[i].open, g_digits) + "," +
                      DoubleToString(velas[i].high, g_digits) + "," + DoubleToString(velas[i].low, g_digits) + "," +
                      DoubleToString(velas[i].close, g_digits) + "," + IntegerToString(velas[i].tick_volume) + "," +
                      IntegerToString(velas[i].spread) + "," + IntegerToString(velas[i].real_volume) + "\r\n");
   FileClose(f);
   return n;
  }

//+------------------------------------------------------------------+
//| OnStart                                                          |
//+------------------------------------------------------------------+
void OnStart()
  {
   string motivo = "";
   if(!Comprobaciones(motivo))
     {
      Alert("ExportarTicksFTMO: ", motivo);
      return;
     }
   datetime desde = StringToTime(InpDesde);
   datetime hasta = StringToTime(InpHasta);
   if(!RangoDeConstruccion(desde, hasta, motivo))
     {
      Alert("ExportarTicksFTMO: ", motivo);
      return;
     }
   g_digits = (int)SymbolInfoInteger(SIMBOLO, SYMBOL_DIGITS);

   MqlDateTime s;
   TimeToStruct(TimeTradeServer(), s);
   string nombre = StringFormat("F17_control_%04d%02d%02d_%02d%02d%02d.csv", s.year, s.mon, s.day, s.hour, s.min, s.sec);
   g_control = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(g_control == INVALID_HANDLE)
     {
      Alert("ExportarTicksFTMO: no se pudo crear ", nombre, " (error ", GetLastError(), ")");
      return;
     }
   FileWriteString(g_control, "clave,valor,nota\r\n");
   // los relojes, como MedirReloj de MedirDemoFTMO.mq5 (ADR-0090 §1: TimeGMT sale del ordenador)
   datetime servidor = TimeTradeServer();
   datetime gmt = TimeGMT();
   Control("version_script", VERSION_SCRIPT);
   Control("cuenta_demo", "si");
   Control("servidor", AccountInfoString(ACCOUNT_SERVER));
   Control("empresa", AccountInfoString(ACCOUNT_COMPANY));
   Control("build", IntegerToString(TerminalInfoInteger(TERMINAL_BUILD)));
   Control("digits", IntegerToString(g_digits));
   Control("time_trade_server_s", IntegerToString((long)servidor));
   Control("time_current_s", IntegerToString((long)TimeCurrent()), "hora del ultimo tick recibido");
   Control("time_gmt_s", IntegerToString((long)gmt), "sale del reloj del ordenador: tiene que estar en hora");
   Control("time_local_s", IntegerToString((long)TimeLocal()));
   Control("desfase_servidor_gmt_min", IntegerToString((int)((servidor - gmt) / 60)));
   Control("desfase_local_gmt_min", IntegerToString(-TimeGMTOffset() / 60));
   Control("horario_verano_local_seg", IntegerToString(TimeDaylightSavings()));
   // la profundidad del historial de M1, como metadato de la serie (respuesta a la PARADA, punto 1)
   Control("primera_m1_servidor_s", IntegerToString(SeriesInfoInteger(SIMBOLO, PERIOD_M1, SERIES_SERVER_FIRSTDATE)));
   Control("primera_m1_terminal_s", IntegerToString(SeriesInfoInteger(SIMBOLO, PERIOD_M1, SERIES_TERMINAL_FIRSTDATE)));
   Control("desde", InpDesde);
   Control("hasta", InpHasta);

   string mes_actual = "";
   long primero_del_mes = 0;
   for(datetime d = desde; d <= hasta; d += 86400)
     {
      int intentos = 0, error = 0;
      long primero = 0, ultimo = 0;
      int n = ExportarTicks(d, intentos, error, primero, ultimo);
      int m1 = ExportarM1(d);
      string dia = Dia(d);
      Control("dia_" + dia + "_ticks", IntegerToString(n));
      Control("dia_" + dia + "_m1", IntegerToString(m1));
      Control("dia_" + dia + "_error", IntegerToString(error));
      Control("dia_" + dia + "_intentos", IntegerToString(intentos));
      Control("dia_" + dia + "_primer_msc", IntegerToString(primero));
      Control("dia_" + dia + "_ultimo_msc", IntegerToString(ultimo));
      // el primer tick de cada mes pedido, buscado dentro de ese mismo mes (punto 1)
      if(Mes(d) != mes_actual)
        {
         if(mes_actual != "")
            Control("mes_" + mes_actual + "_primer_msc", IntegerToString(primero_del_mes));
         mes_actual = Mes(d);
         primero_del_mes = 0;
        }
      if(primero_del_mes == 0 && primero > 0)
         primero_del_mes = primero;
     }
   if(mes_actual != "")
      Control("mes_" + mes_actual + "_primer_msc", IntegerToString(primero_del_mes));
   Control("terminado", "si");
   FileClose(g_control);
   g_control = INVALID_HANDLE;
   Alert("ExportarTicksFTMO: terminado. Ficheros F17_* en MQL5\\Files (control: ", nombre, ")");
  }
//+------------------------------------------------------------------+
