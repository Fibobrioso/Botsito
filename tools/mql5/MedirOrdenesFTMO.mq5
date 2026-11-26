//+------------------------------------------------------------------+
//| MedirOrdenesFTMO.mq5                                             |
//| Bot v3 - rama trabajo/f17-ordenes (2026-11-26)                   |
//|                                                                  |
//| F17, la medida de las ordenes stop (ADR-0099 §5): coloca en la   |
//| DEMO de FTMO una orden stop cada vez, alternando compra y venta, |
//| y registra cada entrada stop, cada cierre por stop y cada cierre |
//| a mercado, con los ticks del servidor desde que se puso hasta    |
//| que se lleno. NO calcula el deslizamiento: lo hace               |
//| scripts/leer_ordenes_f17.py con el criterio pre-registrado de    |
//| docs/plan/F17-ORDENES.yaml. Instrucciones:                       |
//| docs/runbooks/F17-ORDENES.md.                                    |
//|                                                                  |
//| SEGURIDAD (tests/contract/test_medir_ordenes_ftmo.py):           |
//| - se niega a correr si la cuenta no es DEMO, con la condicion    |
//|   de MedirDemoFTMO.mq5:759, antes de cualquier peticion;         |
//| - solo EURUSD y su numero magico (MAGICO), que no es el de       |
//|   MedirDemoFTMO; la limpieza solo toca lo de ese numero;         |
//| - toda pendiente lleva caducidad y stop (y un objetivo lejano de |
//|   respaldo, por si el script muere); un ciclo cada vez;          |
//| - al empezar, al terminar, tras cada ciclo y si algo falla,      |
//|   borra sus pendientes y cierra sus posiciones, y lo comprueba;  |
//| - los topes de D4, cada uno leido de la cuenta y de su historial |
//|   (valen igual si se relanza el mismo dia): (a) peor caso de lo  |
//|   vivo <= TOPE_PEOR_CASO_USD; (b) equity >= saldo al empezar el  |
//|   dia de riesgo - TOPE_DIA_USD; (c) equity >= capital inicial -  |
//|   TOPE_TOTAL_USD; (d) peticiones del dia < TOPE_PETICIONES, con  |
//|   PAUSA_MS entre ellas; (e) nada a menos de MARGEN_CIERRE_MIN    |
//|   del cierre de la sesion; y la ventana muerta de                |
//|   HORA_MUERTA_DESDE a HORA_MUERTA_HASTA del servidor, sin nada   |
//|   vivo, para que el saldo a las 00:00 del servidor sea el de las |
//|   00:00 de Espana (respuesta a la PARADA, punto 3).              |
//|                                                                  |
//| Lo que da por supuesto de MT5 (ADR-0082 D7), de la documentacion |
//| de MQL5 (F17-ORDENES.md, 0.3): ORDER_TIME_SETUP_MSC y            |
//| DEAL_TIME_MSC en ms; DEAL_REASON_SL y DEAL_REASON_EXPERT;        |
//| HistorySelect en hora del servidor; TimeCurrent formado en el    |
//| servidor; CopyTicksRange con los dos bordes dentro. POR MEDIR en |
//| la corrida: el huso de SymbolInfoSessionTrade (la capa lo da por |
//| servidor), si una peticion rechazada entra en el historial (por  |
//| eso cuenta tambien las suyas, de sus CSV) y si el terminal tiene |
//| todos los ticks a los ESPERA_TICKS_MS del llenado.               |
//+------------------------------------------------------------------+
#property copyright "Bot v3"
#property version   "1.00"
#property description "Mide en una cuenta DEMO el llenado de ordenes stop, de cierres por stop y de cierres a mercado de EURUSD, con los ticks del servidor. Solo EURUSD."
#property script_show_inputs

#define VERSION_SCRIPT "1.0"
#define SIMBOLO        "EURUSD"
#define MAGICO         57057100

// Los del criterio (docs/plan/F17-ORDENES.yaml, bloque guion); un test exige que sean esos
#define STOP_PUNTOS              18
#define SALIDA_A_MERCADO_S       300
#define ESPERA_LLENADO_S         120
#define DISTANCIA_ENTRADA_PUNTOS 5

// El lote del bot (ADR-0081 D2); un test los compara con el registro
#define RIESGO_FRACCION       0.005 // riesgo_por_operacion, 0,5 % del saldo actual (base_calculo_riesgo)
#define MARGEN_LIBRE_FRACCION 0.95  // lote_margen_libre_fraccion
#define LOTE_UNO              1.00  // el estrato «uno»

// Los topes (D4); un test los compara con docs/runbooks/F17-ORDENES.md
#define TOPE_PEOR_CASO_USD 1000.0
#define TOPE_DIA_USD       3000.0
#define TOPE_TOTAL_USD     8000.0
#define TOPE_PETICIONES    500
#define PAUSA_MS           1500
#define MARGEN_CIERRE_MIN  150
#define HORA_MUERTA_DESDE  22
#define HORA_MUERTA_HASTA  3
#define CAPITAL_INICIAL    100000.0
// El peor caso de (a), como el paso 8 de MedirDemoFTMO: comision conservadora y deslizamiento supuesto
#define COMISION_LADO_USD  5.00
#define DESLIZ_PEOR_PUNTOS 10
// Lo mas que algo del ciclo esta vivo: la espera del llenado, la de la salida y un minuto de margen
// (que cubre las esperas del historial, ESPERA_HISTORIAL_MS cada una); los ticks se copian despues
// de cerrar, con nada vivo
#define DURACION_MAXIMA_CICLO_S (ESPERA_LLENADO_S + SALIDA_A_MERCADO_S + 60)
// El objetivo de respaldo: lejos, para que no salte en SALIDA_A_MERCADO_S; solo cierra si el script muere
#define OBJETIVO_RESPALDO_PUNTOS (3 * STOP_PUNTOS)
#define ESPERA_TICKS_MS    5000
#define ESPERA_HISTORIAL_MS 10000 // lo que se espera a que un deal llegue al historial
#define INTENTOS_TICKS     3
#define CADUCIDAD_S        900

input string InpEstrato = "uno"; // estrato: «uno» (1,00 lote) o «bot» (el lote de ADR-0081 D2)
input int    InpCiclos  = 50;    // ciclos como mucho en esta ejecucion

int    g_csv     = INVALID_HANDLE;
int    g_fila    = 0;
int    g_digits  = 5;
double g_point   = 0.00001;
string g_estrato = "";
int    g_rechazadas_previas = 0; // peticiones rechazadas de los CSV de hoy de ejecuciones anteriores
int    g_rechazadas = 0;         // las de esta ejecucion

//+------------------------------------------------------------------+
//| Utilidades de texto                                              |
//+------------------------------------------------------------------+
string Campo(const string texto)
  {
   string t = texto;
   StringReplace(t, "\"", "\"\"");
   return "\"" + t + "\"";
  }

string Precio(const double p)
  {
   if(p <= 0.0)
      return "";
   return DoubleToString(p, g_digits);
  }

string Lotes(const double v)
  {
   return DoubleToString(v, 2);
  }

string Hora(const datetime t)
  {
   return TimeToString(t, TIME_DATE | TIME_SECONDS);
  }

string Fecha(const datetime t)
  {
   MqlDateTime s;
   TimeToStruct(t, s);
   return StringFormat("%04d%02d%02d", s.year, s.mon, s.day);
  }

string NombreMotivo(const long r)
  {
   switch((int)r)
     {
      case DEAL_REASON_CLIENT: return "CLIENT";
      case DEAL_REASON_MOBILE: return "MOBILE";
      case DEAL_REASON_WEB:    return "WEB";
      case DEAL_REASON_EXPERT: return "EXPERT";
      case DEAL_REASON_SL:     return "SL";
      case DEAL_REASON_TP:     return "TP";
      case DEAL_REASON_SO:     return "SO";
     }
   return "OTRO_" + IntegerToString(r);
  }

//+------------------------------------------------------------------+
//| Una fila del CSV. Columnas en EscribirCabecera.                  |
//+------------------------------------------------------------------+
void Fila(const int ciclo, const string evento, const string clase, const string lado, const ulong orden,
          const ulong deal, const ulong posicion, const double nivel, const double lotes, const double lote_d2,
          const double precio, const long instante_msc, const long puesta_msc, const MqlTick &cot,
          const string motivo, const uint retcode, const string ticks_fichero, const int ticks_n,
          const int ticks_error, const double comision, const string nota)
  {
   g_fila++;
   string linea = Campo(VERSION_SCRIPT) + "," + IntegerToString(g_fila) + "," + IntegerToString(ciclo) + "," +
                  Campo(g_estrato) + "," + Campo(evento) + "," + Campo(clase) + "," + Campo(lado) + "," +
                  IntegerToString((long)orden) + "," + IntegerToString((long)deal) + "," +
                  IntegerToString((long)posicion) + "," + Precio(nivel) + "," + Lotes(lotes) + "," +
                  Lotes(lote_d2) + "," + Precio(precio) + "," + IntegerToString(instante_msc) + "," +
                  IntegerToString(puesta_msc) + "," + Precio(cot.bid) + "," + Precio(cot.ask) + "," +
                  IntegerToString(cot.time_msc) + "," + Campo(motivo) + "," + IntegerToString(retcode) + "," +
                  Campo(ticks_fichero) + "," + IntegerToString(ticks_n) + "," + IntegerToString(ticks_error) +
                  "," + DoubleToString(comision, 2) + "," + Campo(Hora(TimeCurrent())) + "," +
                  Campo(Hora(TimeGMT())) + "," + Campo(nota);
   FileWriteString(g_csv, linea + "\r\n");
   FileFlush(g_csv);
  }

void Dato(const string evento, const string clave, const string valor, const string nota = "")
  {
   MqlTick vacio;
   ZeroMemory(vacio);
   // en una fila que no es de llenado, `clase` lleva la clave y `motivo` el valor
   Fila(0, evento, clave, "", 0, 0, 0, 0, 0, 0, 0, 0, 0, vacio, valor, 0, "", 0, 0, 0, nota);
  }

void EscribirCabecera()
  {
   FileWriteString(g_csv, "version_script,fila,ciclo,estrato,evento,clase,lado,orden,deal,posicion,nivel,"
                   "lotes,lote_d2,precio,instante_msc,puesta_msc,cot_bid,cot_ask,cot_msc,motivo,retcode,"
                   "ticks_fichero,ticks_n,ticks_error,comision,hora_servidor,hora_gmt,nota\r\n");
  }

//+------------------------------------------------------------------+
//| Mercado y ordenes (Llenado y PonerCaducidad, de MedirDemoFTMO)   |
//+------------------------------------------------------------------+
bool Cotizacion(MqlTick &t)
  {
   if(!SymbolInfoTick(SIMBOLO, t))
      return false;
   return (t.bid > 0.0 && t.ask > 0.0);
  }

ENUM_ORDER_TYPE_FILLING Llenado()
  {
   long modos = SymbolInfoInteger(SIMBOLO, SYMBOL_FILLING_MODE);
   if((modos & SYMBOL_FILLING_FOK) != 0)
      return ORDER_FILLING_FOK;
   if((modos & SYMBOL_FILLING_IOC) != 0)
      return ORDER_FILLING_IOC;
   return ORDER_FILLING_RETURN;
  }

// Toda pendiente caduca (D1): sin el fallback a GTC de MedirDemoFTMO. Si el simbolo no admite
// SYMBOL_EXPIRATION_SPECIFIED, Comprobaciones se niega antes de pedir nada (revisor, b4).
void PonerCaducidad(MqlTradeRequest &req)
  {
   req.type_time = ORDER_TIME_SPECIFIED;
   req.expiration = TimeTradeServer() + CADUCIDAD_S;
  }

bool AdmiteCaducidad()
  {
   return ((SymbolInfoInteger(SIMBOLO, SYMBOL_EXPIRATION_MODE) & SYMBOL_EXPIRATION_SPECIFIED) != 0);
  }

// Toda peticion pasa por aqui: la escribe (aceptada o rechazada), la cuenta si se rechaza y espera
// PAUSA_MS. Devuelve si el servidor la acepto.
bool Pedir(MqlTradeRequest &req, MqlTradeResult &res, const int ciclo, const string que)
  {
   ZeroMemory(res);
   bool ok = OrderSend(req, res);
   bool aceptada = ok && (res.retcode == TRADE_RETCODE_DONE || res.retcode == TRADE_RETCODE_PLACED ||
                          res.retcode == TRADE_RETCODE_DONE_PARTIAL);
   if(!aceptada)
      g_rechazadas++;
   MqlTick vacio;
   ZeroMemory(vacio);
   Fila(ciclo, aceptada ? "peticion" : "peticion_rechazada", que, "", res.order, res.deal, 0, req.price,
        req.volume, 0, res.price, 0, 0, vacio, "", res.retcode, "", 0, 0, 0, res.comment);
   Sleep(PAUSA_MS);
   return aceptada;
  }

// Una orden stop de entrada: con MAGICO, stop en la orden, objetivo de respaldo y caducidad.
bool ColocarStop(const bool compra, const double volumen, const double nivel, const int ciclo, MqlTradeResult &res)
  {
   MqlTradeRequest req;
   ZeroMemory(req);
   req.action = TRADE_ACTION_PENDING;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.volume = volumen;
   req.type = compra ? ORDER_TYPE_BUY_STOP : ORDER_TYPE_SELL_STOP;
   req.price = NormalizeDouble(nivel, g_digits);
   req.sl = NormalizeDouble(compra ? nivel - STOP_PUNTOS * g_point : nivel + STOP_PUNTOS * g_point, g_digits);
   req.tp = NormalizeDouble(compra ? nivel + OBJETIVO_RESPALDO_PUNTOS * g_point
                                   : nivel - OBJETIVO_RESPALDO_PUNTOS * g_point, g_digits);
   req.type_filling = Llenado();
   req.comment = "MedirOrdenesFTMO";
   PonerCaducidad(req);
   return Pedir(req, res, ciclo, compra ? "colocar_buy_stop" : "colocar_sell_stop");
  }

uint BorrarPendiente(const ulong ticket, const int ciclo)
  {
   MqlTradeRequest req;
   MqlTradeResult res;
   ZeroMemory(req);
   req.action = TRADE_ACTION_REMOVE;
   req.order = ticket;
   Pedir(req, res, ciclo, "borrar_pendiente");
   return res.retcode;
  }

// Cierra a mercado la posicion `ticket` (cuenta HEDGING: req.position). `cot`, la cotizacion leida
// justo antes de pedirlo.
bool CerrarPosicion(const ulong ticket, const int ciclo, MqlTick &cot, MqlTradeResult &res)
  {
   ZeroMemory(res);
   if(!PositionSelectByTicket(ticket))
      return false;
   if(!Cotizacion(cot))
      return false;
   MqlTradeRequest req;
   ZeroMemory(req);
   long tipo = PositionGetInteger(POSITION_TYPE);
   req.action = TRADE_ACTION_DEAL;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.position = ticket;
   req.volume = PositionGetDouble(POSITION_VOLUME);
   req.type = (tipo == POSITION_TYPE_BUY) ? ORDER_TYPE_SELL : ORDER_TYPE_BUY;
   req.price = (tipo == POSITION_TYPE_BUY) ? cot.bid : cot.ask;
   req.deviation = 50;
   req.type_filling = Llenado();
   req.comment = "MedirOrdenesFTMO cierre";
   return Pedir(req, res, ciclo, "cerrar_a_mercado");
  }

//+------------------------------------------------------------------+
//| LIMPIEZA: borra toda pendiente y cierra toda posicion del        |
//| numero magico en EURUSD. Reintenta y cuenta lo que quede.        |
//+------------------------------------------------------------------+
int QuedanAbiertas()
  {
   int n = 0;
   for(int i = OrdersTotal() - 1; i >= 0; i--)
     {
      ulong tk = OrderGetTicket(i);
      if(tk != 0 && OrderGetInteger(ORDER_MAGIC) == MAGICO && OrderGetString(ORDER_SYMBOL) == SIMBOLO)
         n++;
     }
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong tk = PositionGetTicket(i);
      if(tk != 0 && PositionGetInteger(POSITION_MAGIC) == MAGICO && PositionGetString(POSITION_SYMBOL) == SIMBOLO)
         n++;
     }
   return n;
  }

int Limpiar(const string cuando)
  {
   for(int intento = 0; intento < 5; intento++)
     {
      for(int i = OrdersTotal() - 1; i >= 0; i--)
        {
         ulong tk = OrderGetTicket(i);
         if(tk != 0 && OrderGetInteger(ORDER_MAGIC) == MAGICO && OrderGetString(ORDER_SYMBOL) == SIMBOLO)
            BorrarPendiente(tk, 0);
        }
      for(int i = PositionsTotal() - 1; i >= 0; i--)
        {
         ulong tk = PositionGetTicket(i);
         if(tk != 0 && PositionGetInteger(POSITION_MAGIC) == MAGICO && PositionGetString(POSITION_SYMBOL) == SIMBOLO)
           {
            MqlTick cot;
            MqlTradeResult res;
            CerrarPosicion(tk, 0, cot, res);
           }
        }
      if(QuedanAbiertas() == 0)
         break;
      Sleep(2000);
     }
   int quedan = QuedanAbiertas();
   if(g_csv != INVALID_HANDLE)
      Dato("limpieza", "quedan_abiertas_" + cuando, IntegerToString(quedan),
           quedan == 0 ? "" : "QUEDAN ORDENES O POSICIONES DEL SCRIPT: cerrarlas a mano");
   if(quedan != 0)
      Alert("MedirOrdenesFTMO: quedan ", quedan, " ordenes o posiciones del script (", cuando,
            "). Cierralas a mano en la pestana Trading (Ctrl+T).");
   return quedan;
  }

//+------------------------------------------------------------------+
//| El lote (ADR-0081 D2) y el peor caso (tope a)                    |
//+------------------------------------------------------------------+
int DecimalesVolumen()
  {
   double paso = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP);
   if(paso <= 0.0)
      return 2;
   return (int)MathMax(0.0, MathRound(-MathLog10(paso)));
  }

// El mayor volumen admitido <= objetivo; 0 si queda por debajo del minimo.
double VolumenHaciaAbajo(const double objetivo)
  {
   double minimo = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MIN);
   double maximo = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MAX);
   double paso = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP);
   if(paso <= 0.0 || objetivo <= 0.0)
      return 0.0;
   double v = NormalizeDouble(MathFloor(objetivo / paso + 1e-9) * paso, DecimalesVolumen());
   if(v > maximo)
      v = maximo;
   if(v < minimo - 1e-9)
      return 0.0;
   return v;
  }

// El margen de 1 lote A MERCADO (ORDER_TYPE_BUY al ASK o ORDER_TYPE_SELL al BID): nunca con el tipo
// stop, cuya tasa de margen es 0;0 en la prueba (DEMO-EJECUCIONES-2-3.md:84-86; respuesta, punto 2).
double MargenDeUnLote(const bool compra, const MqlTick &t)
  {
   double m = 0.0;
   if(!OrderCalcMargin(compra ? ORDER_TYPE_BUY : ORDER_TYPE_SELL, SIMBOLO, 1.0, compra ? t.ask : t.bid, m))
      return -1.0;
   return m;
  }

// Lo que vale un punto con 1 lote, en la moneda de la cuenta.
double ValorDelPunto(const MqlTick &t)
  {
   double p = 0.0;
   if(!OrderCalcProfit(ORDER_TYPE_BUY, SIMBOLO, 1.0, t.ask, t.ask + g_point, p))
      return -1.0;
   return p;
  }

// El lote de ADR-0081 D2: el menor del riesgo, el maximo del simbolo y lo que cabe en el margen libre.
double LoteDelBot(const bool compra, const MqlTick &t)
  {
   double punto = ValorDelPunto(t);
   double margen = MargenDeUnLote(compra, t);
   if(punto <= 0.0 || margen <= 0.0)
      return 0.0;
   double riesgo = RIESGO_FRACCION * AccountInfoDouble(ACCOUNT_BALANCE) / (STOP_PUNTOS * punto);
   double cabe = AccountInfoDouble(ACCOUNT_MARGIN_FREE) * MARGEN_LIBRE_FRACCION / margen;
   return VolumenHaciaAbajo(MathMin(MathMin(riesgo, cabe), SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MAX)));
  }

// La perdida, en USD, de una compra o una venta de `vol` lotes desde `precio` hasta su stop `sl` mas
// DESLIZ_PEOR_PUNTOS en contra, mas la comision de ida y vuelta. -1 si no se puede calcular.
double PerdidaHastaElStop(const bool compra, const double vol, const double precio, const double sl)
  {
   double p = 0.0;
   double cierre = compra ? sl - DESLIZ_PEOR_PUNTOS * g_point : sl + DESLIZ_PEOR_PUNTOS * g_point;
   if(!OrderCalcProfit(compra ? ORDER_TYPE_BUY : ORDER_TYPE_SELL, SIMBOLO, vol, precio, cierre, p))
      return -1.0;
   return MathAbs(p) + 2.0 * COMISION_LADO_USD * vol;
  }

// (a) El peor caso de TODO lo vivo del numero magico (leido de la terminal, no de una variable),
// compras y ventas, mas la orden candidata (vol 0: ninguna). Una posicion o pendiente sin stop es
// infinita: -1, y el ciclo no se hace.
double PeorCaso(const bool compra, const double vol, const double nivel, const double sl)
  {
   double total = 0.0;
   for(int i = OrdersTotal() - 1; i >= 0; i--)
     {
      ulong tk = OrderGetTicket(i);
      if(tk == 0 || OrderGetInteger(ORDER_MAGIC) != MAGICO || OrderGetString(ORDER_SYMBOL) != SIMBOLO)
         continue;
      long tipo = OrderGetInteger(ORDER_TYPE);
      bool c = (tipo == ORDER_TYPE_BUY_STOP || tipo == ORDER_TYPE_BUY_LIMIT || tipo == ORDER_TYPE_BUY);
      double s = OrderGetDouble(ORDER_SL);
      if(s <= 0.0)
         return -1.0;
      double x = PerdidaHastaElStop(c, OrderGetDouble(ORDER_VOLUME_CURRENT), OrderGetDouble(ORDER_PRICE_OPEN), s);
      if(x < 0.0)
         return -1.0;
      total += x;
     }
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong tk = PositionGetTicket(i);
      if(tk == 0 || PositionGetInteger(POSITION_MAGIC) != MAGICO || PositionGetString(POSITION_SYMBOL) != SIMBOLO)
         continue;
      bool c = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY);
      double s = PositionGetDouble(POSITION_SL);
      if(s <= 0.0)
         return -1.0;
      double x = PerdidaHastaElStop(c, PositionGetDouble(POSITION_VOLUME), PositionGetDouble(POSITION_PRICE_OPEN), s);
      if(x < 0.0)
         return -1.0;
      total += x;
     }
   if(vol > 0.0)
     {
      double x = PerdidaHastaElStop(compra, vol, nivel, sl);
      if(x < 0.0)
         return -1.0;
      total += x;
     }
   return total;
  }

//+------------------------------------------------------------------+
//| Los topes (b) a (e) y la ventana muerta, de la cuenta y de su    |
//| historial                                                        |
//+------------------------------------------------------------------+
// Las 00:00 del dia del servidor de `t` (TimeCurrent: formado en el servidor).
datetime InicioDelDia(const datetime t)
  {
   return t - t % 86400;
  }

// La ventana muerta: de HORA_MUERTA_DESDE a HORA_MUERTA_HASTA del servidor. Dentro, nada se coloca ni
// se tiene: las dos medianoches (servidor y Espana) caen en ella (respuesta a la PARADA, punto 3).
bool EnHoraMuerta(const datetime t)
  {
   MqlDateTime s;
   TimeToStruct(t, s);
   return (s.hour >= HORA_MUERTA_DESDE || s.hour < HORA_MUERTA_HASTA);
  }

// (b) El saldo al empezar el dia de riesgo, rehecho del historial de TODA la cuenta: el saldo de
// ahora menos lo que han movido los deals DE TRADING (DEAL_TYPE_BUY y DEAL_TYPE_SELL) desde las
// 00:00 del servidor. Un deposito u otro movimiento de saldo no es perdida del dia: el dia en que se
// activa la prueba, el DEAL_TYPE_BALANCE de 100.000 esta en el historial de hoy, y restarlo dejaba
// el saldo del dia en 0 y el tope sin saltar (revision del consultor, arreglo 1). -1 si no se lee.
double SaldoAlEmpezarElDia()
  {
   datetime desde = InicioDelDia(TimeCurrent());
   if(!HistorySelect(desde, TimeCurrent() + 3600))
      return -1.0;
   double movido = 0.0;
   for(int i = HistoryDealsTotal() - 1; i >= 0; i--)
     {
      ulong d = HistoryDealGetTicket(i);
      if(d == 0)
         continue;
      long tipo = HistoryDealGetInteger(d, DEAL_TYPE);
      if(tipo != DEAL_TYPE_BUY && tipo != DEAL_TYPE_SELL)
         continue;
      movido += HistoryDealGetDouble(d, DEAL_PROFIT) + HistoryDealGetDouble(d, DEAL_COMMISSION) +
                HistoryDealGetDouble(d, DEAL_SWAP) + HistoryDealGetDouble(d, DEAL_FEE);
     }
   return AccountInfoDouble(ACCOUNT_BALANCE) - movido;
  }

// (c) El capital inicial, del historial entero: la suma de los deals de saldo (DEAL_TYPE_BALANCE).
double CapitalDelHistorial()
  {
   if(!HistorySelect(0, TimeCurrent() + 3600))
      return -1.0;
   double capital = 0.0;
   for(int i = HistoryDealsTotal() - 1; i >= 0; i--)
     {
      ulong d = HistoryDealGetTicket(i);
      if(d != 0 && HistoryDealGetInteger(d, DEAL_TYPE) == DEAL_TYPE_BALANCE)
         capital += HistoryDealGetDouble(d, DEAL_PROFIT);
     }
   return capital;
  }

// (d) Las peticiones de trading del dia de riesgo: cada orden del numero magico desde las 00:00 del
// servidor (en el historial o viva) cuenta una, y una borrada (ORDER_STATE_CANCELED) otra mas por su
// borrado; mas las rechazadas, que quiza no entran en el historial (0.3): las de los CSV de hoy de
// ejecuciones anteriores y las de esta (respuesta a la PARADA, punto 4).
int PeticionesDelDia()
  {
   datetime desde = InicioDelDia(TimeCurrent());
   int n = 0;
   if(HistorySelect(desde, TimeCurrent() + 3600))
      for(int i = HistoryOrdersTotal() - 1; i >= 0; i--)
        {
         ulong o = HistoryOrderGetTicket(i);
         // solo las que pide el script: la orden que crea el servidor al saltar un stop
         // (ORDER_REASON_SL) no es una peticion
         if(o == 0 || HistoryOrderGetInteger(o, ORDER_MAGIC) != MAGICO ||
            HistoryOrderGetInteger(o, ORDER_REASON) != ORDER_REASON_EXPERT)
            continue;
         n++;
         if(HistoryOrderGetInteger(o, ORDER_STATE) == ORDER_STATE_CANCELED)
            n++;
        }
   else
      return TOPE_PETICIONES; // sin historial, no se sabe: como si se hubiera llegado al tope
   for(int i = OrdersTotal() - 1; i >= 0; i--)
     {
      ulong tk = OrderGetTicket(i);
      if(tk != 0 && OrderGetInteger(ORDER_MAGIC) == MAGICO &&
         (datetime)OrderGetInteger(ORDER_TIME_SETUP) >= desde)
         n++;
     }
   return n + g_rechazadas_previas + g_rechazadas;
  }

// Las rechazadas de los CSV de hoy (por la fecha del servidor en su nombre) de ejecuciones anteriores.
int RechazadasDeHoy(const string propio)
  {
   string hoy = Fecha(TimeCurrent());
   int n = 0;
   string nombre = "";
   long h = FileFindFirst("F17M_*.csv", nombre);
   if(h == INVALID_HANDLE)
      return 0;
   do
     {
      bool del_estrato = (StringFind(nombre, "F17M_uno_") == 0 || StringFind(nombre, "F17M_bot_") == 0);
      if(!del_estrato || nombre == propio || StringFind(nombre, "_" + hoy + "_") < 0)
         continue;
      int f = FileOpen(nombre, FILE_READ | FILE_TXT | FILE_ANSI | FILE_SHARE_READ);
      if(f == INVALID_HANDLE)
         continue;
      while(!FileIsEnding(f))
         if(StringFind(FileReadString(f), "\"peticion_rechazada\"") >= 0)
            n++;
      FileClose(f);
     }
   while(FileFindNext(h, nombre));
   FileFindClose(h);
   return n;
  }

// (e) Si quedan menos de MARGEN_CIERRE_MIN minutos para el fin de la sesion de hoy de
// SymbolInfoSessionTrade (segundos desde las 00:00; el huso, POR MEDIR: la capa lo da por servidor),
// o si ahora no hay sesion, no se coloca.
bool CercaDelCierre(const datetime ahora, string &nota)
  {
   MqlDateTime s;
   TimeToStruct(ahora, s);
   int segundo = s.hour * 3600 + s.min * 60 + s.sec;
   datetime desde, hasta;
   for(uint i = 0; i < 32; i++)
     {
      if(!SymbolInfoSessionTrade(SIMBOLO, (ENUM_DAY_OF_WEEK)s.day_of_week, i, desde, hasta))
         break;
      int a = (int)(desde % 86400);
      int b = (int)(hasta % 86400);
      if(b == 0)
         b = 86400;
      if(segundo >= a && segundo < b)
        {
         nota = "sesion " + IntegerToString(a) + "-" + IntegerToString(b) + " s; faltan " +
                IntegerToString((b - segundo) / 60) + " min";
         return (b - segundo < MARGEN_CIERRE_MIN * 60);
        }
     }
   nota = "ahora no hay sesion de trading";
   return true;
  }

// Si se puede empezar un ciclo con `vol` lotes del lado `compra` en `nivel` y stop `sl`. Escribe el
// tope que salta. Los topes (a) a (e) y la ventana muerta, todos desde la cuenta y su historial.
bool PuedeEmpezarCiclo(const int ciclo, const bool compra, const double vol, const double nivel,
                       const double sl, string &tope)
  {
   datetime ahora = TimeCurrent();
   string nota = "";
   if(EnHoraMuerta(ahora) || EnHoraMuerta(ahora + DURACION_MAXIMA_CICLO_S))
     {
      tope = "hora_muerta";
      nota = "de " + IntegerToString(HORA_MUERTA_DESDE) + ":00 a " + IntegerToString(HORA_MUERTA_HASTA) +
             ":00 del servidor no se coloca ni se tiene nada";
     }
   else if(CercaDelCierre(ahora, nota))
      tope = "e_cierre_de_sesion";
   else
     {
      double equity = AccountInfoDouble(ACCOUNT_EQUITY);
      double saldo_dia = SaldoAlEmpezarElDia();
      double capital = CapitalDelHistorial();
      int peticiones = PeticionesDelDia();
      double peor = PeorCaso(compra, vol, nivel, sl);
      if(saldo_dia < 0.0 || equity < saldo_dia - TOPE_DIA_USD)
        {
         tope = "b_dia";
         nota = "equity " + DoubleToString(equity, 2) + "; saldo al empezar el dia " + DoubleToString(saldo_dia, 2);
        }
      else if(MathAbs(capital - CAPITAL_INICIAL) > 0.005 || equity < CAPITAL_INICIAL - TOPE_TOTAL_USD)
        {
         tope = "c_total";
         nota = "equity " + DoubleToString(equity, 2) + "; capital del historial " + DoubleToString(capital, 2);
        }
      else if(peticiones + 3 > TOPE_PETICIONES)
        {
         tope = "d_peticiones";
         nota = IntegerToString(peticiones) + " peticiones hoy (un ciclo pide hasta 3)";
        }
      else if(peor < 0.0 || peor > TOPE_PEOR_CASO_USD)
        {
         tope = "a_peor_caso";
         nota = "peor caso " + DoubleToString(peor, 2) + " USD";
        }
      else
         return true;
     }
   Dato("tope", tope, "salta", nota);
   return false;
  }

// Durante la espera de un ciclo: si la equity rompe (b) o (c), o se entra en la ventana muerta, hay
// que cerrar ya.
bool HayQueCortar(string &tope)
  {
   double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   double saldo_dia = SaldoAlEmpezarElDia();
   if(EnHoraMuerta(TimeCurrent()))
      tope = "hora_muerta";
   else if(saldo_dia < 0.0 || equity < saldo_dia - TOPE_DIA_USD)
      tope = "b_dia";
   else if(equity < CAPITAL_INICIAL - TOPE_TOTAL_USD)
      tope = "c_total";
   else
      return false;
   Dato("tope", tope, "salta_en_el_ciclo", "equity " + DoubleToString(equity, 2));
   return true;
  }

//+------------------------------------------------------------------+
//| El historial de un llenado                                       |
//+------------------------------------------------------------------+
// El deal de la orden `orden` (el de entrada o el de un cierre a mercado). false si no lo hay.
bool DealDeLaOrden(const ulong orden, ulong &deal)
  {
   deal = 0;
   if(!HistorySelect(TimeCurrent() - 86400, TimeCurrent() + 3600))
      return false;
   for(int i = HistoryDealsTotal() - 1; i >= 0; i--)
     {
      ulong d = HistoryDealGetTicket(i);
      if(d != 0 && (ulong)HistoryDealGetInteger(d, DEAL_ORDER) == orden)
        {
         deal = d;
         return true;
        }
     }
   return false;
  }

// El deal que cierra la posicion `posicion` (DEAL_ENTRY_OUT). false si sigue abierta.
bool DealDeSalida(const ulong posicion, ulong &deal)
  {
   deal = 0;
   if(!HistorySelect(TimeCurrent() - 86400, TimeCurrent() + 3600))
      return false;
   for(int i = HistoryDealsTotal() - 1; i >= 0; i--)
     {
      ulong d = HistoryDealGetTicket(i);
      if(d != 0 && (ulong)HistoryDealGetInteger(d, DEAL_POSITION_ID) == posicion &&
         HistoryDealGetInteger(d, DEAL_ENTRY) == DEAL_ENTRY_OUT)
        {
         deal = d;
         return true;
        }
     }
   return false;
  }

// Espera, hasta ESPERA_HISTORIAL_MS, a que el deal de la orden llegue al historial (revisor, b7).
bool EsperarDealDeLaOrden(const ulong orden, ulong &deal)
  {
   for(int ms = 0; ms <= ESPERA_HISTORIAL_MS; ms += 500)
     {
      if(DealDeLaOrden(orden, deal))
         return true;
      Sleep(500);
     }
   return false;
  }

// Espera, hasta ESPERA_HISTORIAL_MS, a que el deal de salida de la posicion llegue al historial.
bool EsperarDealDeSalida(const ulong posicion, ulong &deal)
  {
   for(int ms = 0; ms <= ESPERA_HISTORIAL_MS; ms += 500)
     {
      if(DealDeSalida(posicion, deal))
         return true;
      Sleep(500);
     }
   return false;
  }

ulong TicketDeLaPosicion(const ulong posicion)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong tk = PositionGetTicket(i);
      if(tk != 0 && (ulong)PositionGetInteger(POSITION_IDENTIFIER) == posicion)
         return tk;
     }
   return 0;
  }

// Los ticks del servidor de [desde_msc, hasta_msc] (CopyTicksRange: los dos bordes dentro), a
// F17M_ticks_<deal>.csv, tras ESPERA_TICKS_MS para que el terminal los tenga. Devuelve cuantos.
int GuardarTicks(const ulong deal, const long desde_msc, const long hasta_msc, string &fichero, int &error)
  {
   fichero = "";
   error = 0;
   // sin un inicio conocido no se pide nada: CopyTicksRange desde 0 bajaria historial desde 1970
   // (revisor, b7 iii)
   if(desde_msc <= 0 || hasta_msc < desde_msc)
      return -1;
   Sleep(ESPERA_TICKS_MS);
   MqlTick ticks[];
   int n = -1;
   for(int intento = 1; intento <= INTENTOS_TICKS; intento++)
     {
      ResetLastError();
      n = CopyTicksRange(SIMBOLO, ticks, COPY_TICKS_ALL, (ulong)desde_msc, (ulong)hasta_msc);
      error = GetLastError();
      if(n >= 0 && error == 0)
         break;
      Sleep(1000);
     }
   fichero = "F17M_ticks_" + IntegerToString((long)deal) + ".csv";
   int f = FileOpen(fichero, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(f == INVALID_HANDLE)
     {
      fichero = "";
      return -1;
     }
   FileWriteString(f, "time_msc,bid,ask,flags\r\n");
   for(int i = 0; i < n; i++)
      FileWriteString(f, IntegerToString(ticks[i].time_msc) + "," + DoubleToString(ticks[i].bid, g_digits) +
                      "," + DoubleToString(ticks[i].ask, g_digits) + "," + IntegerToString(ticks[i].flags) + "\r\n");
   FileClose(f);
   return n;
  }

// Escribe la fila de un llenado con sus ticks. `clase`: entrada_stop, cierre_stop, cierre_mercado u
// otro_<motivo>; `lado`: el de la ejecucion.
void FilaDeLlenado(const int ciclo, const string clase, const bool compra_ejecuta, const ulong orden,
                   const ulong deal, const ulong posicion, const double nivel, const double lote_d2,
                   const long puesta_msc, const MqlTick &cot, const long desde_ticks_msc)
  {
   HistoryDealSelect(deal);
   long instante = HistoryDealGetInteger(deal, DEAL_TIME_MSC);
   string fichero = "";
   int error = 0;
   int n = GuardarTicks(deal, desde_ticks_msc, instante, fichero, error);
   HistoryDealSelect(deal);
   Fila(ciclo, "llenado", clase, compra_ejecuta ? "compra" : "venta", orden, deal, posicion, nivel,
        HistoryDealGetDouble(deal, DEAL_VOLUME), lote_d2, HistoryDealGetDouble(deal, DEAL_PRICE), instante,
        puesta_msc, cot, NombreMotivo(HistoryDealGetInteger(deal, DEAL_REASON)), 0, fichero, n, error,
        HistoryDealGetDouble(deal, DEAL_COMMISSION), "");
  }

//+------------------------------------------------------------------+
//| Un ciclo                                                         |
//+------------------------------------------------------------------+
// Devuelve false si hay que parar (un tope, o algo que no se pudo leer).
bool Ciclo(const int ciclo, const bool compra)
  {
   MqlTick cot;
   if(!Cotizacion(cot))
      return false;
   double nivel = compra ? cot.ask + DISTANCIA_ENTRADA_PUNTOS * g_point : cot.bid - DISTANCIA_ENTRADA_PUNTOS * g_point;
   nivel = NormalizeDouble(nivel, g_digits);
   double sl = NormalizeDouble(compra ? nivel - STOP_PUNTOS * g_point : nivel + STOP_PUNTOS * g_point, g_digits);
   double lote_d2 = (g_estrato == "bot") ? LoteDelBot(compra, cot) : LOTE_UNO;
   double vol = lote_d2;
   // respuesta a la PARADA, punto 2: si no cabe en el tope (a), se baja el lote hasta que quepa
   double paso = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP);
   while(vol > 0.0)
     {
      double peor = PeorCaso(compra, vol, nivel, sl);
      if(peor >= 0.0 && peor <= TOPE_PEOR_CASO_USD)
         break;
      vol = VolumenHaciaAbajo(vol - paso);
     }
   if(vol <= 0.0)
     {
      Dato("tope", "a_peor_caso", "salta", "ningun lote cabe en el tope con el stop de " + IntegerToString(STOP_PUNTOS));
      return false;
     }
   string tope = "";
   if(!PuedeEmpezarCiclo(ciclo, compra, vol, nivel, sl, tope))
      return false;

   MqlTradeResult res;
   if(!ColocarStop(compra, vol, nivel, ciclo, res))
     {
      // una colocacion rechazada para la ejecucion: no se gastan peticiones rechazadas ciclo tras
      // ciclo (revisor, b6; A-54 no sabe si FTMO las cuenta)
      Dato("ciclo", "colocacion_rechazada", IntegerToString(ciclo), "se para la ejecucion");
      Limpiar("ciclo_" + IntegerToString(ciclo));
      return false;
     }
   ulong orden = res.order;
   long puesta = 0;
   ulong deal = 0;
   // las esperas, por el reloj del ordenador (TimeLocal): TimeCurrent no avanza si no llegan ticks
   datetime limite = TimeLocal() + ESPERA_LLENADO_S;
   while(!IsStopped())
     {
      if(OrderSelect(orden))
        {
         puesta = OrderGetInteger(ORDER_TIME_SETUP_MSC);
         if(TimeLocal() >= limite || HayQueCortar(tope))
           {
            BorrarPendiente(orden, ciclo);
            break;
           }
         Sleep(200);
         continue;
        }
      if(DealDeLaOrden(orden, deal))
         break;
      Sleep(200);
      if(TimeLocal() >= limite)
         break;
     }
   // si se lleno justo al borrarla, el deal puede tardar en llegar al historial (revisor, b7 ii)
   if(deal == 0)
      EsperarDealDeLaOrden(orden, deal);
   if(deal == 0)
     {
      Dato("ciclo", "sin_llenado", IntegerToString(ciclo), "no se lleno en " + IntegerToString(ESPERA_LLENADO_S) + " s");
      return (Limpiar("ciclo_" + IntegerToString(ciclo)) == 0 && tope == "");
     }
   if(puesta == 0 && HistoryOrderSelect(orden))
      puesta = HistoryOrderGetInteger(orden, ORDER_TIME_SETUP_MSC);
   HistoryDealSelect(deal);
   ulong posicion = (ulong)HistoryDealGetInteger(deal, DEAL_POSITION_ID);
   long entrada_msc = HistoryDealGetInteger(deal, DEAL_TIME_MSC);

   // la salida: por su stop o, a los SALIDA_A_MERCADO_S del llenado, a mercado (revisor, b5: los
   // ticks de la entrada se copian DESPUES de cerrarla, para que la espera no se alargue ni deje de
   // mirar los topes)
   datetime fin = TimeLocal() + SALIDA_A_MERCADO_S;
   ulong salida = 0;
   MqlTick cot_cierre;
   ZeroMemory(cot_cierre);
   ulong orden_cierre = 0;
   while(!IsStopped() && !DealDeSalida(posicion, salida))
     {
      if(TimeLocal() >= fin || HayQueCortar(tope))
        {
         ulong tk = TicketDeLaPosicion(posicion);
         MqlTradeResult rc;
         if(tk != 0 && CerrarPosicion(tk, ciclo, cot_cierre, rc))
            orden_cierre = rc.order;
         // el deal de salida puede tardar en llegar al historial (revisor, b7 i)
         EsperarDealDeSalida(posicion, salida);
         break;
        }
      Sleep(200);
     }
   if(salida == 0)
     {
      // si falta porque se paro el guion, lo dice (revision del consultor, arreglo 4)
      Dato("ciclo", "sin_salida", IntegerToString(ciclo),
           IsStopped() ? "parado por el usuario: Limpiar" : "la posicion no se pudo cerrar: Limpiar");
      return false;
     }
   // los datos de la salida, leidos antes de escribir nada (la seleccion del historial cambia)
   HistoryDealSelect(salida);
   long motivo = HistoryDealGetInteger(salida, DEAL_REASON);
   ulong orden_salida = (ulong)HistoryDealGetInteger(salida, DEAL_ORDER);
   string clase = (motivo == DEAL_REASON_SL) ? "cierre_stop" :
                  ((motivo == DEAL_REASON_EXPERT && orden_cierre != 0) ? "cierre_mercado" : "otro_" + NombreMotivo(motivo));
   long puesta_cierre = 0;
   if(orden_cierre != 0 && HistoryOrderSelect(orden_cierre))
      puesta_cierre = HistoryOrderGetInteger(orden_cierre, ORDER_TIME_SETUP_MSC);

   // la entrada: los ticks desde la cotizacion leida antes de colocarla (para ver si llego ya
   // pasada); sin puesta conocida, desde esa cotizacion, nunca desde 0 (revisor, b7 iii)
   long desde_entrada = (puesta > 0) ? MathMin(cot.time_msc, puesta) : cot.time_msc;
   FilaDeLlenado(ciclo, "entrada_stop", compra, orden, deal, posicion, nivel, lote_d2, puesta, cot, desde_entrada);
   if(clase == "cierre_stop")
     {
      MqlTick vacio;
      ZeroMemory(vacio);
      FilaDeLlenado(ciclo, clase, !compra, orden_salida, salida, posicion, sl, lote_d2, entrada_msc, vacio, entrada_msc);
     }
   else
      FilaDeLlenado(ciclo, clase, !compra, orden_salida, salida, posicion, 0, lote_d2, puesta_cierre, cot_cierre,
                    cot_cierre.time_msc > 0 ? cot_cierre.time_msc : entrada_msc);
   if(Limpiar("ciclo_" + IntegerToString(ciclo)) != 0)
      return false;
   return (tope == "");
  }

//+------------------------------------------------------------------+
//| Arranque                                                         |
//+------------------------------------------------------------------+
bool Comprobaciones(string &motivo)
  {
   if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)
     {
      motivo = "la cuenta NO es DEMO: el script no hace nada";
      return false;
     }
   if(InpEstrato != "uno" && InpEstrato != "bot")
     {
      motivo = "InpEstrato tiene que ser «uno» o «bot»";
      return false;
     }
   if(!SymbolSelect(SIMBOLO, true))
     {
      motivo = "no existe el simbolo EURUSD en esta cuenta";
      return false;
     }
   if(!TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) || !MQLInfoInteger(MQL_TRADE_ALLOWED))
     {
      motivo = "el trading algoritmico esta desactivado: pulsa el boton Algo Trading y vuelve a ejecutar";
      return false;
     }
   if(SymbolInfoInteger(SIMBOLO, SYMBOL_TRADE_MODE) != SYMBOL_TRADE_MODE_FULL)
     {
      motivo = "EURUSD no admite operar ahora (mercado cerrado o simbolo restringido)";
      return false;
     }
   MqlTick t;
   if(!Cotizacion(t))
     {
      motivo = "sin cotizacion de EURUSD";
      return false;
     }
   if(TimeTradeServer() - t.time > 120)
     {
      motivo = "la ultima cotizacion de EURUSD tiene mas de 2 minutos: el mercado parece cerrado";
      return false;
     }
   double capital = CapitalDelHistorial();
   if(MathAbs(capital - CAPITAL_INICIAL) > 0.005)
     {
      motivo = "el capital del historial (" + DoubleToString(capital, 2) + ") no es el de la prueba: no se adivina";
      return false;
     }
   // con un stops level mayor que la distancia de la entrada, cada orden se rechazaria: se niega al
   // empezar en vez de gastar peticiones (revision del consultor, arreglo 3)
   if(!AdmiteCaducidad())
     {
      motivo = "EURUSD no admite caducidad en las pendientes (SYMBOL_EXPIRATION_SPECIFIED): toda pendiente tiene que llevarla";
      return false;
     }
   long stops = SymbolInfoInteger(SIMBOLO, SYMBOL_TRADE_STOPS_LEVEL);
   if(stops > DISTANCIA_ENTRADA_PUNTOS)
     {
      motivo = "el stops level de EURUSD (" + IntegerToString(stops) + " puntos) es mayor que DISTANCIA_ENTRADA_PUNTOS (" +
               IntegerToString(DISTANCIA_ENTRADA_PUNTOS) + "): cada orden se rechazaria";
      return false;
     }
   return true;
  }

void OnStart()
  {
   string motivo = "";
   if(!Comprobaciones(motivo))
     {
      Alert("MedirOrdenesFTMO: ", motivo);
      return;
     }
   g_estrato = InpEstrato;
   g_digits = (int)SymbolInfoInteger(SIMBOLO, SYMBOL_DIGITS);
   g_point = SymbolInfoDouble(SIMBOLO, SYMBOL_POINT);

   MqlDateTime s;
   TimeToStruct(TimeCurrent(), s);
   string nombre = StringFormat("F17M_%s_%04d%02d%02d_%02d%02d%02d.csv", g_estrato, s.year, s.mon, s.day,
                                s.hour, s.min, s.sec);
   g_rechazadas_previas = RechazadasDeHoy(nombre);
   g_csv = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(g_csv == INVALID_HANDLE)
     {
      Alert("MedirOrdenesFTMO: no se pudo crear ", nombre, " (error ", GetLastError(), ")");
      return;
     }
   EscribirCabecera();
   Dato("contexto", "version_script", VERSION_SCRIPT);
   Dato("contexto", "cuenta_demo", "si");
   Dato("contexto", "servidor", AccountInfoString(ACCOUNT_SERVER));
   Dato("contexto", "time_trade_server_s", IntegerToString((long)TimeTradeServer()));
   Dato("contexto", "time_current_s", IntegerToString((long)TimeCurrent()), "hora del ultimo tick recibido");
   Dato("contexto", "time_gmt_s", IntegerToString((long)TimeGMT()), "sale del reloj del ordenador");
   Dato("contexto", "desfase_servidor_gmt_min", IntegerToString((int)((TimeTradeServer() - TimeGMT()) / 60)));
   Dato("contexto", "digits", IntegerToString(g_digits));
   Dato("contexto", "stops_level", IntegerToString(SymbolInfoInteger(SIMBOLO, SYMBOL_TRADE_STOPS_LEVEL)));
   Dato("contexto", "rechazadas_previas_hoy", IntegerToString(g_rechazadas_previas));
   int quedan = Limpiar("al_empezar");
   bool ok = (quedan == 0);
   int hechos = 0;
   for(int ciclo = 1; ok && ciclo <= InpCiclos && !IsStopped(); ciclo++)
     {
      ok = Ciclo(ciclo, ciclo % 2 == 1); // impares compran, pares venden
      hechos = ciclo;
     }
   quedan = Limpiar("al_terminar");
   Dato("fin", "ciclos", IntegerToString(hechos), ok ? "completo" : "parado");
   FileClose(g_csv);
   g_csv = INVALID_HANDLE;
   string msg = "MedirOrdenesFTMO: terminado (" + IntegerToString(hechos) + " ciclos). Fichero: MQL5\\Files\\" + nombre;
   if(quedan != 0)
      msg += ". ATENCION: quedan " + IntegerToString(quedan) + " ordenes o posiciones del script";
   Alert(msg);
  }
//+------------------------------------------------------------------+
