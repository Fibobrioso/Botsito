//+------------------------------------------------------------------+
//| MedirDemoFTMO.mq5                                                |
//| Bot v3 - rama trabajo/demo-ftmo-script (2026-09-28)              |
//|                                                                  |
//| Mide en la cuenta de PRUEBA GRATUITA de FTMO lo que ADR-0057,    |
//| A-27, A-28 y FTMO-REGLAS dejaron pendiente. Escribe un CSV en    |
//| MQL5/Files, una fila por medicion. Lo lee                        |
//| scripts/leer_demo_ftmo.py. Instrucciones: docs/runbooks/         |
//| DEMO-FTMO.md.                                                    |
//|                                                                  |
//| 1.1 (trabajo/demo-ejecucion-1, ADR-0071): el paso 6 abre con     |
//| InpVolumenComision lotes; filas OBSERVACION. 1.2 (trabajo/       |
//| margen-pendiente): paso 8, cuando comprueba MT5 el margen de     |
//| una pendiente stop (ADR-0081, D3); InpMedirMargen.               |
//|                                                                  |
//| SEGURIDAD:                                                       |
//| - se niega a correr si la cuenta no es DEMO;                     |
//| - solo EURUSD, numero magico propio, volumen minimo salvo en     |
//|   los pasos 6 y 8 (el 8: sus lotes, peor caso <= 1000 USD);      |
//| - toda pendiente lleva caducidad (si el simbolo la admite); las  |
//|   de los pasos 3-5 van sin stop a proposito y, si una se llena,  |
//|   se cierra en cuanto se lee; toda otra posicion lleva stop;     |
//| - al empezar, al terminar y si un paso falla, borra pendientes y |
//|   cierra posiciones del numero magico, y comprueba que no queda. |
//+------------------------------------------------------------------+
#property copyright "Bot v3"
#property version   "1.20"
#property description "Mide especificacion, reloj, pendientes mal colocadas, stops level, modificacion, comision y el margen de las pendientes en una cuenta DEMO. Solo EURUSD."
#property script_show_inputs

#define VERSION_SCRIPT "1.2"
#define SIMBOLO        "EURUSD"
#define MAGICO         57057000

input bool InpMedirLlenadoStop = true; // medir el llenado de una orden stop (paso 7)
input int  InpEsperaStopSeg    = 120;  // segundos maximos esperando a que salte la stop del paso 7
input int  InpPausaMs          = 1500; // pausa entre peticiones al servidor
input double InpVolumenComision = 1.00; // lotes de la compra y el cierre del paso 6 (comision)

int    g_csv    = INVALID_HANDLE;
int    g_fila   = 0;
int    g_digits = 5;
double g_point  = 0.00001;
double g_volumen = 0.01;
int    g_stops  = 0;

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

string Hora(const datetime t)
  {
   return TimeToString(t, TIME_DATE | TIME_SECONDS);
  }

string TextoRetcode(const uint r)
  {
   switch(r)
     {
      case 0:     return "SIN_RESPUESTA";
      case 10004: return "REQUOTE";
      case 10006: return "REJECT";
      case 10007: return "CANCEL";
      case 10008: return "PLACED";
      case 10009: return "DONE";
      case 10010: return "DONE_PARTIAL";
      case 10011: return "ERROR";
      case 10012: return "TIMEOUT";
      case 10013: return "INVALID";
      case 10014: return "INVALID_VOLUME";
      case 10015: return "INVALID_PRICE";
      case 10016: return "INVALID_STOPS";
      case 10017: return "TRADE_DISABLED";
      case 10018: return "MARKET_CLOSED";
      case 10019: return "NO_MONEY";
      case 10020: return "PRICE_CHANGED";
      case 10021: return "PRICE_OFF";
      case 10022: return "INVALID_EXPIRATION";
      case 10023: return "ORDER_CHANGED";
      case 10024: return "TOO_MANY_REQUESTS";
      case 10025: return "NO_CHANGES";
      case 10026: return "SERVER_DISABLES_AT";
      case 10027: return "CLIENT_DISABLES_AT";
      case 10028: return "LOCKED";
      case 10029: return "FROZEN";
      case 10030: return "INVALID_FILL";
      case 10031: return "CONNECTION";
      case 10033: return "LIMIT_ORDERS";
      case 10034: return "LIMIT_VOLUME";
      case 10035: return "INVALID_ORDER";
      case 10036: return "POSITION_CLOSED";
     }
   return "OTRO";
  }

//+------------------------------------------------------------------+
//| Una fila del CSV. Columnas en EscribirCabecera.                  |
//+------------------------------------------------------------------+
void Fila(const string medicion, const string responde, const string clave, const string valor,
          const uint retcode, const string colocada, const string tipo, const double pedido,
          const double bid, const double ask, const double resultado, const string distancia,
          const string nota, const bool observacion = false)
  {
   g_fila++;
   string r = (retcode == 0 && StringLen(tipo) == 0) ? "" : IntegerToString(retcode);
   // una observacion no es una peticion: no hay retcode del servidor (1.1; en 1.0, SIN_RESPUESTA)
   string rt = (StringLen(r) == 0) ? "" : (observacion ? "OBSERVACION" : TextoRetcode(retcode));
   string linea = Campo(VERSION_SCRIPT) + "," + IntegerToString(g_fila) + "," + Campo(medicion) + "," +
                  Campo(responde) + "," + Campo(clave) + "," + Campo(valor) + "," + r + "," +
                  Campo(rt) + "," + Campo(colocada) + "," + Campo(tipo) + "," + Precio(pedido) + "," +
                  Precio(bid) + "," + Precio(ask) + "," + Precio(resultado) + "," + Campo(distancia) +
                  "," + Campo(Hora(TimeTradeServer())) + "," + Campo(Hora(TimeGMT())) + "," + Campo(nota);
   FileWriteString(g_csv, linea + "\r\n");
   FileFlush(g_csv);
  }

void Dato(const string medicion, const string responde, const string clave, const string valor,
          const string nota = "")
  {
   Fila(medicion, responde, clave, valor, 0, "", "", 0, 0, 0, 0, "", nota);
  }

void EscribirCabecera()
  {
   FileWriteString(g_csv, "version_script,fila,medicion,responde,clave,valor,retcode,retcode_texto,"
                   "colocada,tipo_orden,precio_pedido,bid,ask,precio_resultado,distancia_puntos,"
                   "hora_servidor,hora_gmt,nota\r\n");
  }

//+------------------------------------------------------------------+
//| Mercado y ordenes                                                |
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

void PonerCaducidad(MqlTradeRequest &req)
  {
   long modos = SymbolInfoInteger(SIMBOLO, SYMBOL_EXPIRATION_MODE);
   if((modos & SYMBOL_EXPIRATION_SPECIFIED) != 0)
     {
      req.type_time = ORDER_TIME_SPECIFIED;
      req.expiration = TimeTradeServer() + 15 * 60;
     }
   else
      req.type_time = ORDER_TIME_GTC;
  }

string NombreTipo(const ENUM_ORDER_TYPE tipo)
  {
   switch(tipo)
     {
      case ORDER_TYPE_BUY:        return "buy";
      case ORDER_TYPE_SELL:       return "sell";
      case ORDER_TYPE_BUY_LIMIT:  return "buy_limit";
      case ORDER_TYPE_SELL_LIMIT: return "sell_limit";
      case ORDER_TYPE_BUY_STOP:   return "buy_stop";
      case ORDER_TYPE_SELL_STOP:  return "sell_stop";
     }
   return EnumToString(tipo);
  }

bool EsCompra(const ENUM_ORDER_TYPE tipo)
  {
   return (tipo == ORDER_TYPE_BUY || tipo == ORDER_TYPE_BUY_LIMIT || tipo == ORDER_TYPE_BUY_STOP);
  }

// Envia una pendiente SIN stop ni objetivo, para que solo se juzgue su precio.
bool EnviarPendiente(const ENUM_ORDER_TYPE tipo, const double precio, MqlTradeResult &res)
  {
   MqlTradeRequest req;
   ZeroMemory(req);
   ZeroMemory(res);
   req.action = TRADE_ACTION_PENDING;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.volume = g_volumen;
   req.type = tipo;
   req.price = NormalizeDouble(precio, g_digits);
   req.type_filling = Llenado();
   req.comment = "MedirDemoFTMO";
   PonerCaducidad(req);
   bool ok = OrderSend(req, res);
   Sleep(InpPausaMs);
   return ok;
  }

bool PendienteViva(const ulong ticket, double &precio)
  {
   precio = 0.0;
   if(ticket == 0 || !OrderSelect(ticket))
      return false;
   precio = OrderGetDouble(ORDER_PRICE_OPEN);
   return true;
  }

uint BorrarPendiente(const ulong ticket)
  {
   MqlTradeRequest req;
   MqlTradeResult res;
   ZeroMemory(req);
   ZeroMemory(res);
   req.action = TRADE_ACTION_REMOVE;
   req.order = ticket;
   if(!OrderSend(req, res))
      Print("No se pudo borrar la pendiente ", ticket, ": ", res.retcode);
   Sleep(InpPausaMs);
   return res.retcode;
  }

// Si la orden se lleno, el precio del deal de entrada; 0 si no.
double PrecioDelLlenado(const ulong orden, ulong &posicion, double &comision)
  {
   posicion = 0;
   comision = 0.0;
   if(orden == 0)
      return 0.0;
   HistorySelect(TimeTradeServer() - 86400, TimeTradeServer() + 3600);
   int n = HistoryDealsTotal();
   for(int i = n - 1; i >= 0; i--)
     {
      ulong deal = HistoryDealGetTicket(i);
      if(deal == 0)
         continue;
      if((ulong)HistoryDealGetInteger(deal, DEAL_ORDER) != orden)
         continue;
      posicion = (ulong)HistoryDealGetInteger(deal, DEAL_POSITION_ID);
      comision = HistoryDealGetDouble(deal, DEAL_COMMISSION);
      return HistoryDealGetDouble(deal, DEAL_PRICE);
     }
   return 0.0;
  }

// Cierra a mercado la posicion con ese identificador. Devuelve el retcode.
uint CerrarPosicion(const ulong ticket, MqlTradeResult &res)
  {
   ZeroMemory(res);
   if(!PositionSelectByTicket(ticket))
      return 0;
   MqlTick t;
   if(!Cotizacion(t))
      return 0;
   MqlTradeRequest req;
   ZeroMemory(req);
   long tipo = PositionGetInteger(POSITION_TYPE);
   req.action = TRADE_ACTION_DEAL;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.position = ticket;
   req.volume = PositionGetDouble(POSITION_VOLUME);
   req.type = (tipo == POSITION_TYPE_BUY) ? ORDER_TYPE_SELL : ORDER_TYPE_BUY;
   req.price = (tipo == POSITION_TYPE_BUY) ? t.bid : t.ask;
   req.deviation = 50;
   req.type_filling = Llenado();
   req.comment = "MedirDemoFTMO cierre";
   if(!OrderSend(req, res))
      Print("No se pudo cerrar la posicion ", ticket, ": ", res.retcode);
   Sleep(InpPausaMs);
   return res.retcode;
  }

//+------------------------------------------------------------------+
//| LIMPIEZA: borra toda pendiente y cierra toda posicion del        |
//| numero magico en EURUSD. Se llama al empezar, al terminar y si   |
//| un paso falla. Reintenta y cuenta lo que quede.                  |
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
            BorrarPendiente(tk);
        }
      for(int i = PositionsTotal() - 1; i >= 0; i--)
        {
         ulong tk = PositionGetTicket(i);
         if(tk != 0 && PositionGetInteger(POSITION_MAGIC) == MAGICO && PositionGetString(POSITION_SYMBOL) == SIMBOLO)
           {
            MqlTradeResult res;
            CerrarPosicion(tk, res);
           }
        }
      if(QuedanAbiertas() == 0)
         break;
      Sleep(2000);
     }
   int quedan = QuedanAbiertas();
   if(g_csv != INVALID_HANDLE)
      Dato("limpieza", "seguridad", "quedan_abiertas_" + cuando, IntegerToString(quedan),
           quedan == 0 ? "" : "QUEDAN ORDENES O POSICIONES DEL SCRIPT: cerrarlas a mano");
   if(quedan != 0)
      Alert("MedirDemoFTMO: quedan ", quedan, " ordenes o posiciones del script (", cuando,
            "). Cierralas a mano en la pestana Trading (Ctrl+T).");
   return quedan;
  }

//+------------------------------------------------------------------+
//| 1. Especificacion del simbolo y de la cuenta                     |
//+------------------------------------------------------------------+
bool MedirEspecificacion()
  {
   string m = "1_especificacion";
   Dato(m, "A-27; ADR-0057 d5", "stops_level_puntos", IntegerToString(SymbolInfoInteger(SIMBOLO, SYMBOL_TRADE_STOPS_LEVEL)));
   Dato(m, "A-27; ADR-0057 d5", "freeze_level_puntos", IntegerToString(SymbolInfoInteger(SIMBOLO, SYMBOL_TRADE_FREEZE_LEVEL)));
   Dato(m, "A-27", "digits", IntegerToString(SymbolInfoInteger(SIMBOLO, SYMBOL_DIGITS)));
   Dato(m, "A-27", "point", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_POINT), 8));
   Dato(m, "A-27", "contrato", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_TRADE_CONTRACT_SIZE), 2));
   Dato(m, "A-27", "volumen_min", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MIN), 2));
   Dato(m, "FTMO-REGLAS R11", "volumen_max", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MAX), 2));
   Dato(m, "A-27", "volumen_paso", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP), 2));
   Dato(m, "FTMO-REGLAS R11", "volumen_limite", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_LIMIT), 2));
   long f = SymbolInfoInteger(SIMBOLO, SYMBOL_FILLING_MODE);
   string modos = "";
   if((f & SYMBOL_FILLING_FOK) != 0)
      modos += "FOK ";
   if((f & SYMBOL_FILLING_IOC) != 0)
      modos += "IOC ";
   modos += "(bits " + IntegerToString(f) + ")";
   Dato(m, "A-27", "modos_llenado", modos);
   Dato(m, "A-27", "modo_ejecucion", EnumToString((ENUM_SYMBOL_TRADE_EXECUTION)SymbolInfoInteger(SIMBOLO, SYMBOL_TRADE_EXEMODE)));
   Dato(m, "A-27", "modos_caducidad_bits", IntegerToString(SymbolInfoInteger(SIMBOLO, SYMBOL_EXPIRATION_MODE)));
   Dato(m, "FTMO-REGLAS R12", "swap_largo", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_SWAP_LONG), 4));
   Dato(m, "FTMO-REGLAS R12", "swap_corto", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_SWAP_SHORT), 4));
   Dato(m, "FTMO-REGLAS R12", "swap_modo", EnumToString((ENUM_SYMBOL_SWAP_MODE)SymbolInfoInteger(SIMBOLO, SYMBOL_SWAP_MODE)));
   Dato(m, "FTMO-REGLAS R12", "swap_triple_dia", EnumToString((ENUM_DAY_OF_WEEK)SymbolInfoInteger(SIMBOLO, SYMBOL_SWAP_ROLLOVER3DAYS)));
   Dato(m, "contexto", "spread_actual_puntos", IntegerToString(SymbolInfoInteger(SIMBOLO, SYMBOL_SPREAD)));
   Dato(m, "contexto", "servidor", AccountInfoString(ACCOUNT_SERVER));
   Dato(m, "contexto", "empresa", AccountInfoString(ACCOUNT_COMPANY));
   Dato(m, "contexto", "moneda", AccountInfoString(ACCOUNT_CURRENCY));
   Dato(m, "contexto", "apalancamiento", IntegerToString(AccountInfoInteger(ACCOUNT_LEVERAGE)));
   Dato(m, "contexto", "modo_margen", EnumToString((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)));
   Dato(m, "contexto", "build_terminal", IntegerToString(TerminalInfoInteger(TERMINAL_BUILD)));
   return true;
  }

//+------------------------------------------------------------------+
//| 2. Reloj                                                         |
//+------------------------------------------------------------------+
bool MedirReloj()
  {
   string m = "2_reloj";
   datetime servidor = TimeTradeServer();
   datetime gmt = TimeGMT();
   Dato(m, "A-28", "time_current", Hora(TimeCurrent()), "hora del ultimo tick recibido");
   Dato(m, "A-28", "time_trade_server", Hora(servidor));
   Dato(m, "A-28", "time_gmt", Hora(gmt), "TimeGMT sale del reloj del ordenador: tiene que estar en hora");
   Dato(m, "A-28", "time_local", Hora(TimeLocal()));
   Dato(m, "A-28", "desfase_servidor_gmt_min", IntegerToString((int)((servidor - gmt) / 60)));
   Dato(m, "contexto", "desfase_local_gmt_min", IntegerToString(-TimeGMTOffset() / 60));
   Dato(m, "contexto", "horario_verano_local_seg", IntegerToString(TimeDaylightSavings()));
   return true;
  }

//+------------------------------------------------------------------+
//| Una pendiente de prueba: la envia, registra y la quita           |
//+------------------------------------------------------------------+
void ProbarPendiente(const string medicion, const string responde, const string clave,
                     const ENUM_ORDER_TYPE tipo, const double precio, const MqlTick &t,
                     const string distancia)
  {
   MqlTradeResult res;
   EnviarPendiente(tipo, precio, res);
   double vivo = 0.0;
   string colocada = "no";
   double resultado = 0.0;
   string nota = res.comment;
   if(PendienteViva(res.order, vivo))
     {
      colocada = "si";
      resultado = vivo;
      uint rb = BorrarPendiente(res.order);
      nota += "; borrada con retcode " + IntegerToString(rb);
     }
   else
     {
      ulong posicion = 0;
      double comision = 0.0;
      double lleno = PrecioDelLlenado(res.order, posicion, comision);
      if(lleno > 0.0)
        {
         colocada = "llenada";
         resultado = lleno;
         MqlTradeResult rc;
         uint r = CerrarPosicion(posicion, rc);
         nota += "; SE LLENO al instante; posicion cerrada con retcode " + IntegerToString(r);
        }
     }
   Fila(medicion, responde, clave, "", res.retcode, colocada, NombreTipo(tipo), precio, t.bid, t.ask,
        resultado, distancia, nota);
  }

//+------------------------------------------------------------------+
//| 3. Pendientes del lado equivocado                                |
//+------------------------------------------------------------------+
bool MedirLadoEquivocado()
  {
   string m = "3_lado_equivocado";
   string resp = "ADR-0057 d2; ADR-0057 d3; ADR-0057 d4";
   int d = 20 + g_stops; // bien pasado el precio, y mas alla del stops level
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   ProbarPendiente(m, resp, "sell_stop_por_encima_del_bid", ORDER_TYPE_SELL_STOP, t.bid + d * g_point, t, IntegerToString(d));
   if(!Cotizacion(t))
      return false;
   ProbarPendiente(m, resp, "buy_stop_por_debajo_del_ask", ORDER_TYPE_BUY_STOP, t.ask - d * g_point, t, IntegerToString(d));
   if(!Cotizacion(t))
      return false;
   ProbarPendiente(m, resp, "sell_limit_por_debajo_del_bid", ORDER_TYPE_SELL_LIMIT, t.bid - d * g_point, t, IntegerToString(d));
   if(!Cotizacion(t))
      return false;
   ProbarPendiente(m, resp, "buy_limit_por_encima_del_ask", ORDER_TYPE_BUY_LIMIT, t.ask + d * g_point, t, IntegerToString(d));
   return true;
  }

//+------------------------------------------------------------------+
//| 4. En el nivel exacto, a la distancia del stops level y 1 punto  |
//|    dentro, del lado BUENO                                        |
//+------------------------------------------------------------------+
double PrecioBueno(const ENUM_ORDER_TYPE tipo, const MqlTick &t, const int distancia)
  {
   // lado bueno: sell stop y buy limit por debajo; buy stop y sell limit por encima
   double ref = EsCompra(tipo) ? t.ask : t.bid;
   if(tipo == ORDER_TYPE_SELL_STOP || tipo == ORDER_TYPE_BUY_LIMIT)
      return ref - distancia * g_point;
   return ref + distancia * g_point;
  }

bool MedirDistancias()
  {
   string m = "4_distancias";
   ENUM_ORDER_TYPE tipos[4] = {ORDER_TYPE_SELL_STOP, ORDER_TYPE_BUY_STOP, ORDER_TYPE_SELL_LIMIT, ORDER_TYPE_BUY_LIMIT};
   int distancias[3];
   distancias[0] = 0;              // el nivel exacto
   distancias[1] = g_stops;        // justo a la distancia del stops level
   distancias[2] = g_stops - 1;    // 1 punto dentro (con stops level 0: 1 punto del lado equivocado)
   string nombres[3] = {"nivel_exacto", "a_distancia_stops_level", "un_punto_dentro"};
   string resp[3] = {"ADR-0057 d2", "A-27; ADR-0057 d5", "A-27; ADR-0057 d5"};
   for(int k = 0; k < 3; k++)
     {
      if(k == 1 && g_stops == 0)
         continue; // con stops level 0 coincide con el nivel exacto
      for(int i = 0; i < 4; i++)
        {
         MqlTick t;
         if(!Cotizacion(t))
            return false;
         double p = PrecioBueno(tipos[i], t, distancias[k]);
         ProbarPendiente(m, resp[k], nombres[k] + "_" + NombreTipo(tipos[i]), tipos[i], p, t,
                         IntegerToString(distancias[k]));
        }
     }
   return true;
  }

//+------------------------------------------------------------------+
//| 5. Modificacion que cruza                                        |
//+------------------------------------------------------------------+
bool ModificarCruzando(const ENUM_ORDER_TYPE tipo)
  {
   string m = "5_modificacion";
   int d = 50 + g_stops;
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   MqlTradeResult res;
   double valido = PrecioBueno(tipo, t, d);
   EnviarPendiente(tipo, valido, res);
   double vivo = 0.0;
   if(!PendienteViva(res.order, vivo))
     {
      Fila(m, "ADR-0057 d3", "colocar_valida_" + NombreTipo(tipo), "", res.retcode, "no", NombreTipo(tipo),
           valido, t.bid, t.ask, 0, IntegerToString(d), "la pendiente valida no se coloco: no se puede medir la modificacion");
      return true;
     }
   Fila(m, "ADR-0057 d3", "colocar_valida_" + NombreTipo(tipo), "", res.retcode, "si", NombreTipo(tipo),
        valido, t.bid, t.ask, vivo, IntegerToString(d), res.comment);
   // el precio nuevo, 20 puntos (mas el stops level) del lado EQUIVOCADO
   if(!Cotizacion(t))
      return false;
   int e = 20 + g_stops;
   double malo = PrecioBueno(tipo, t, -e);
   MqlTradeRequest req;
   MqlTradeResult rm;
   ZeroMemory(req);
   ZeroMemory(rm);
   req.action = TRADE_ACTION_MODIFY;
   req.order = res.order;
   req.symbol = SIMBOLO;
   req.price = NormalizeDouble(malo, g_digits);
   PonerCaducidad(req);
   if(!OrderSend(req, rm))
      Print("Modificacion no aceptada: ", rm.retcode);
   Sleep(InpPausaMs);
   double despues = 0.0;
   string sigue = "no";
   string nota = rm.comment;
   if(PendienteViva(res.order, despues))
      sigue = (MathAbs(despues - vivo) < g_point / 2.0) ? "si_sin_cambios" : "si_con_precio_nuevo";
   else
     {
      ulong posicion = 0;
      double comision = 0.0;
      double lleno = PrecioDelLlenado(res.order, posicion, comision);
      if(lleno > 0.0)
        {
         sigue = "llenada";
         despues = lleno;
         MqlTradeResult rc;
         uint r = CerrarPosicion(posicion, rc);
         nota += "; SE LLENO al modificar; posicion cerrada con retcode " + IntegerToString(r);
        }
     }
   Fila(m, "ADR-0057 d3", "modificar_al_lado_equivocado_" + NombreTipo(tipo), "", rm.retcode, sigue,
        NombreTipo(tipo), malo, t.bid, t.ask, despues, IntegerToString(-e), nota);
   if(sigue == "si_sin_cambios" || sigue == "si_con_precio_nuevo")
      BorrarPendiente(res.order);
   return true;
  }

bool MedirModificacion()
  {
   if(!ModificarCruzando(ORDER_TYPE_SELL_STOP))
      return false;
   return ModificarCruzando(ORDER_TYPE_BUY_LIMIT);
  }

//+------------------------------------------------------------------+
//| 6. Comision por lado, spread y deslizamiento a mercado           |
//+------------------------------------------------------------------+
// 1.1: el volumen del paso 6 tiene que ser uno que el simbolo admite (minimo, maximo y paso).
bool VolumenAdmitido(const double volumen, string &motivo)
  {
   double minimo = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MIN);
   double maximo = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MAX);
   double paso = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP);
   if(volumen < minimo || volumen > maximo || paso <= 0.0 ||
      MathAbs(volumen / paso - MathRound(volumen / paso)) > 1e-6)
     {
      motivo = "volumen no admitido: minimo " + DoubleToString(minimo, 2) + ", maximo " +
               DoubleToString(maximo, 2) + ", paso " + DoubleToString(paso, 2);
      return false;
     }
   return true;
  }

// 1.1: antes de abrir, el margen que pide la compra frente al margen libre de la cuenta.
bool MargenAlcanza(const double volumen, const MqlTick &t, string &motivo)
  {
   double margen = 0.0;
   if(!OrderCalcMargin(ORDER_TYPE_BUY, SIMBOLO, volumen, t.ask, margen))
     {
      motivo = "no se pudo calcular el margen (error " + IntegerToString(GetLastError()) + ")";
      return false;
     }
   double libre = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   motivo = "margen necesario " + DoubleToString(margen, 2) + "; margen libre " + DoubleToString(libre, 2);
   if(margen > libre)
     {
      motivo = "margen libre insuficiente: " + motivo;
      return false;
     }
   return true;
  }

bool MedirComision()
  {
   string m = "6_comision";
   string resp = "FTMO-REGLAS R12; ADR-0057 d1 (deslizamiento)";
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   double volumen = InpVolumenComision;
   string motivo = "";
   bool admitido = VolumenAdmitido(volumen, motivo) && MargenAlcanza(volumen, t, motivo);
   Dato(m, resp, "volumen_comision", DoubleToString(volumen, 2), motivo);
   if(!admitido)
     {
      // no abre: lo escribe en la fila de la apertura y el paso termina sin error
      Dato(m, resp, "apertura_compra_mercado", "no_abre", motivo);
      return true;
     }
   MqlTradeRequest req;
   MqlTradeResult res;
   ZeroMemory(req);
   ZeroMemory(res);
   int proteccion = 200 + g_stops; // stop de proteccion: 20 pips, por si el script se corta
   req.action = TRADE_ACTION_DEAL;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.volume = volumen;
   req.type = ORDER_TYPE_BUY;
   req.price = t.ask;
   req.sl = NormalizeDouble(t.bid - proteccion * g_point, g_digits);
   req.deviation = 50;
   req.type_filling = Llenado();
   req.comment = "MedirDemoFTMO comision";
   if(!OrderSend(req, res))
      Print("Compra a mercado no aceptada: ", res.retcode);
   Sleep(InpPausaMs);
   ulong posicion = 0;
   double comision = 0.0;
   double lleno = PrecioDelLlenado(res.order, posicion, comision);
   double desl = (lleno > 0.0) ? (lleno - t.ask) / g_point : 0.0;
   Fila(m, resp, "apertura_compra_mercado", DoubleToString(comision, 2), res.retcode,
        lleno > 0.0 ? "llenada" : "no", "buy", t.ask, t.bid, t.ask, lleno,
        DoubleToString(desl, 1), "valor = DEAL_COMMISSION de la apertura; distancia = deslizamiento en puntos (+ en contra); spread " +
        IntegerToString((int)MathRound((t.ask - t.bid) / g_point)) + " puntos");
   if(lleno <= 0.0 || posicion == 0)
      return true;
   Sleep(3000);
   MqlTick c;
   if(!Cotizacion(c))
      return false;
   MqlTradeResult rc;
   uint r = CerrarPosicion(posicion, rc);
   double comision_c = 0.0;
   ulong pos2 = 0;
   double cierre = PrecioDelLlenado(rc.order, pos2, comision_c);
   double desl_c = (cierre > 0.0) ? (c.bid - cierre) / g_point : 0.0;
   Fila(m, resp, "cierre_compra_mercado", DoubleToString(comision_c, 2), r,
        cierre > 0.0 ? "llenada" : "no", "sell", c.bid, c.bid, c.ask, cierre,
        DoubleToString(desl_c, 1), "valor = DEAL_COMMISSION del cierre; distancia = deslizamiento en puntos (+ en contra); spread " +
        IntegerToString((int)MathRound((c.ask - c.bid) / g_point)) + " puntos");
   return true;
  }

//+------------------------------------------------------------------+
//| 7. Llenado de una orden stop de entrada (ADR-0057 d1)            |
//+------------------------------------------------------------------+
bool MedirLlenadoStop()
  {
   string m = "7_llenado_stop";
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   int d = MathMax(g_stops, 1) + 1; // tan cerca como deje el servidor, para que salte pronto
   int proteccion = 200 + g_stops;
   MqlTradeRequest req;
   MqlTradeResult res;
   ZeroMemory(req);
   ZeroMemory(res);
   double nivel = NormalizeDouble(t.ask + d * g_point, g_digits);
   req.action = TRADE_ACTION_PENDING;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.volume = g_volumen;
   req.type = ORDER_TYPE_BUY_STOP;
   req.price = nivel;
   req.sl = NormalizeDouble(nivel - proteccion * g_point, g_digits);
   req.type_filling = Llenado();
   req.comment = "MedirDemoFTMO stop";
   PonerCaducidad(req);
   if(!OrderSend(req, res))
      Print("Buy stop no aceptada: ", res.retcode);
   Sleep(InpPausaMs);
   double vivo = 0.0;
   if(!PendienteViva(res.order, vivo))
     {
      ulong p0 = 0;
      double c0 = 0.0;
      double l0 = PrecioDelLlenado(res.order, p0, c0);
      Fila(m, "ADR-0057 d1", "buy_stop_colocar", "", res.retcode, l0 > 0.0 ? "llenada" : "no", "buy_stop",
           nivel, t.bid, t.ask, l0, IntegerToString(d), res.comment);
      if(l0 > 0.0)
        {
         MqlTradeResult rc0;
         CerrarPosicion(p0, rc0);
        }
      return true;
     }
   Fila(m, "ADR-0057 d1", "buy_stop_colocar", "", res.retcode, "si", "buy_stop", nivel, t.bid, t.ask,
        vivo, IntegerToString(d), res.comment);
   datetime limite = TimeLocal() + InpEsperaStopSeg;
   double lleno = 0.0;
   ulong posicion = 0;
   double comision = 0.0;
   while(TimeLocal() < limite)
     {
      Sleep(500);
      double v;
      if(!PendienteViva(res.order, v))
        {
         lleno = PrecioDelLlenado(res.order, posicion, comision);
         break;
        }
     }
   MqlTick a;
   Cotizacion(a);
   if(lleno > 0.0)
     {
      Fila(m, "ADR-0057 d1", "buy_stop_llenado", DoubleToString((lleno - nivel) / g_point, 1), 0, "llenada",
           "buy_stop", nivel, a.bid, a.ask, lleno, IntegerToString(d),
           "valor = precio del llenado menos el nivel, en puntos (+ en contra)", true);
      MqlTradeResult rc;
      CerrarPosicion(posicion, rc);
     }
   else
     {
      Fila(m, "ADR-0057 d1", "buy_stop_llenado", "no_salto", 0, "no", "buy_stop", nivel, a.bid, a.ask, 0,
           IntegerToString(d), "no salto en " + IntegerToString(InpEsperaStopSeg) + " s; se borra", true);
      BorrarPendiente(res.order);
     }
   return true;
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
   return true;
  }

//+------------------------------------------------------------------+
//| 8. Cuando comprueba MT5 el margen de una pendiente stop          |
//|    (1.2, rama trabajo/margen-pendiente; ADR-0081 D3). Va aqui,   |
//|    tras Comprobaciones, para no mover la linea de la condicion   |
//|    DEMO que citan ADR-0082 y la capa de mql5/.                   |
//|    Todo del MISMO lado (compras). Cada medida calcula sus lotes  |
//|    con OrderCalcMargin y el margen libre del momento, y su stop  |
//|    de proteccion con el tope de perdida de P8_TOPE_USD.          |
//+------------------------------------------------------------------+
#define P8_MED           "8_margen"
#define P8_RESP          "ADR-0081 D3"
#define P8_TOPE_USD      1000.0 // peor caso de todo lo que una medida puede tener a la vez
#define P8_COMISION_LADO 5.00   // USD por lote y lado: supuesto conservador del registro (ADR-0071)
#define P8_DESLIZ        10     // puntos por operacion: 5 veces el mayor medido (DEMO-EJECUCION-1)
#define P8_STOP_MIN      10     // puntos: si el tope no deja este stop, la medida no se hace
#define P8_STOP_MAX      200    // puntos: el stop de proteccion de los pasos 6 y 7
#define P8_LEJOS         1000   // puntos sobre el ask: una pendiente que no salta
#define P8_CERCA         10     // puntos sobre el ask (mas el stops level): la stop S de M4
#define P8_DIF_MIN       20.0   // USD de diferencia entre el margen a la orden y al mercado (M2)
#define P8_CARGA         0.10   // fraccion del margen calculado que tiene que bajar el libre (M2)
#define P8_ESPERA_CUENTA 5000   // ms maximos esperando a que la cuenta refleje una orden

input bool InpMedirMargen     = true; // medir cuando comprueba MT5 el margen de una pendiente (paso 8)
input int  InpEsperaMargenSeg = 120;  // segundos maximos esperando a que salte la stop de M4 (paso 8)

string Usd(const double v)
  {
   return DoubleToString(v, 2);
  }

string Lotes(const double v)
  {
   return DoubleToString(v, 2);
  }

int DecimalesVolumen()
  {
   double paso = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP);
   if(paso <= 0.0)
      return 2;
   return (int)MathMax(0.0, MathRound(-MathLog10(paso)));
  }

// El menor volumen admitido (minimo, maximo y paso del simbolo) que es >= objetivo; 0 si pasa del maximo.
double VolumenHaciaArriba(const double objetivo)
  {
   double minimo = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MIN);
   double maximo = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MAX);
   double paso = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP);
   if(paso <= 0.0 || objetivo <= 0.0)
      return 0.0;
   double v = NormalizeDouble(MathCeil(objetivo / paso - 1e-9) * paso, DecimalesVolumen());
   if(v < minimo)
      v = minimo;
   if(v > maximo + 1e-9)
      return 0.0;
   return v;
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

// OrderCalcMargin: el margen de esa orden sola, en la moneda de la cuenta; -1 si no se puede.
double Margen(const ENUM_ORDER_TYPE tipo, const double volumen, const double precio)
  {
   double m = 0.0;
   if(volumen <= 0.0 || !OrderCalcMargin(tipo, SIMBOLO, volumen, precio, m))
      return -1.0;
   return m;
  }

// El peor caso, en USD, de un conjunto de compras (posiciones o buy stops que pueden llenarse): cada
// una hasta un stop comun de `stop` puntos bajo su precio, mas P8_DESLIZ puntos, mas la comision de
// ida y vuelta. OrderCalcProfit no lleva comision: va aparte. -1 si no se puede calcular.
double PeorCaso(const double &vols[], const double &precios[], const int n, const int stop)
  {
   double total = 0.0;
   for(int i = 0; i < n; i++)
     {
      double p = 0.0;
      double cierre = precios[i] - (stop + P8_DESLIZ) * g_point;
      if(!OrderCalcProfit(ORDER_TYPE_BUY, SIMBOLO, vols[i], precios[i], cierre, p))
         return -1.0;
      total += MathAbs(p) + 2.0 * P8_COMISION_LADO * vols[i];
     }
   return total;
  }

// El mayor stop (puntos, de P8_STOP_MAX a P8_STOP_MIN) cuyo peor caso no pasa del tope; 0 si ni el
// minimo cabe o no se puede calcular. Escribe la fila <clave>_peor_caso, se coloque o no.
int StopDelTope(const string clave, const double &vols[], const double &precios[], const int n)
  {
   double lotes = 0.0;
   for(int i = 0; i < n; i++)
      lotes += vols[i];
   double peor = -1.0;
   int elegido = 0;
   for(int s = P8_STOP_MAX; s >= P8_STOP_MIN; s--)
     {
      peor = PeorCaso(vols, precios, n, s);
      if(peor < 0.0)
         break;
      if(peor <= P8_TOPE_USD)
        {
         elegido = s;
         break;
        }
     }
   string nota = "stop " + IntegerToString(elegido) + " puntos; " + Lotes(lotes) + " lotes a la vez; tope " +
                 Usd(P8_TOPE_USD) + " USD; comision " + Usd(P8_COMISION_LADO) + " por lote y lado; deslizamiento " +
                 IntegerToString(P8_DESLIZ) + " puntos";
   if(elegido == 0)
      nota = "SIN STOP QUE QUEPA EN EL TOPE (con " + IntegerToString(P8_STOP_MIN) + " puntos: " + Usd(peor) + " USD); " + nota;
   Dato(P8_MED, P8_RESP, clave + "_peor_caso", Usd(peor), nota);
   return elegido;
  }

// Una buy stop del paso 8: con MAGICO, stop de proteccion y caducidad.
bool ColocarBuyStop(const double volumen, const double precio, const int stop, const string comentario,
                    const bool pausar, MqlTradeResult &res)
  {
   MqlTradeRequest req;
   ZeroMemory(req);
   ZeroMemory(res);
   req.action = TRADE_ACTION_PENDING;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.volume = volumen;
   req.type = ORDER_TYPE_BUY_STOP;
   req.price = NormalizeDouble(precio, g_digits);
   req.sl = NormalizeDouble(precio - stop * g_point, g_digits);
   req.type_filling = Llenado();
   req.comment = comentario;
   PonerCaducidad(req);
   bool ok = OrderSend(req, res);
   if(pausar)
      Sleep(InpPausaMs);
   return ok;
  }

// Una compra a mercado del paso 8: con MAGICO y stop de proteccion.
bool AbrirCompra(const double volumen, const MqlTick &t, const int stop, MqlTradeResult &res)
  {
   MqlTradeRequest req;
   ZeroMemory(req);
   ZeroMemory(res);
   req.action = TRADE_ACTION_DEAL;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.volume = volumen;
   req.type = ORDER_TYPE_BUY;
   req.price = t.ask;
   req.sl = NormalizeDouble(t.ask - stop * g_point, g_digits);
   req.deviation = P8_DESLIZ;
   req.type_filling = Llenado();
   req.comment = "MedirDemoFTMO m4 ocupacion";
   bool ok = OrderSend(req, res);
   Sleep(InpPausaMs);
   return ok;
  }

// Espera (hasta P8_ESPERA_CUENTA ms) a que cambie el margen libre, el usado o el de las pendientes.
int EsperarCuenta(const double libre, const double usado, const double inicial)
  {
   int ms = 0;
   while(ms < P8_ESPERA_CUENTA)
     {
      if(MathAbs(AccountInfoDouble(ACCOUNT_MARGIN_FREE) - libre) > 0.005 ||
         MathAbs(AccountInfoDouble(ACCOUNT_MARGIN) - usado) > 0.005 ||
         MathAbs(AccountInfoDouble(ACCOUNT_MARGIN_INITIAL) - inicial) > 0.005)
        {
         Sleep(250); // una lectura mas, por si la cuenta se actualiza en dos tiempos
         return ms + 250;
        }
      Sleep(250);
      ms += 250;
     }
   return ms;
  }

// Lo que paso con una pendiente del paso 8 recien enviada: "si" (viva, y se borra si borrar), "llenada"
// (y se cierra en cuanto se lee) o "no". En nota, el comentario del servidor y lo que se hizo.
string Desenlace(const ulong orden, const bool borrar, double &resultado, string &nota)
  {
   resultado = 0.0;
   double vivo = 0.0;
   if(PendienteViva(orden, vivo))
     {
      resultado = vivo;
      if(borrar)
         nota += "; borrada con retcode " + IntegerToString(BorrarPendiente(orden));
      return "si";
     }
   ulong posicion = 0;
   double comision = 0.0;
   double lleno = PrecioDelLlenado(orden, posicion, comision);
   if(lleno > 0.0)
     {
      resultado = lleno;
      MqlTradeResult rc;
      nota += "; SE LLENO; posicion cerrada con retcode " + IntegerToString(CerrarPosicion(posicion, rc));
      return "llenada";
     }
   return "no";
  }

// El volumen y el precio de lo que lleno una orden (suma de sus deals) y su posicion; 0 si nada.
double VolumenLlenado(const ulong orden, double &precio, ulong &posicion)
  {
   precio = 0.0;
   posicion = 0;
   double volumen = 0.0;
   if(orden == 0)
      return 0.0;
   HistorySelect(TimeTradeServer() - 86400, TimeTradeServer() + 3600);
   for(int i = HistoryDealsTotal() - 1; i >= 0; i--)
     {
      ulong deal = HistoryDealGetTicket(i);
      if(deal == 0 || (ulong)HistoryDealGetInteger(deal, DEAL_ORDER) != orden)
         continue;
      volumen += HistoryDealGetDouble(deal, DEAL_VOLUME);
      precio = HistoryDealGetDouble(deal, DEAL_PRICE);
      posicion = (ulong)HistoryDealGetInteger(deal, DEAL_POSITION_ID);
     }
   return volumen;
  }

bool PosicionViva(const ulong ticket)
  {
   return ticket != 0 && PositionSelectByTicket(ticket);
  }

//--- contexto del paso 8: lo que dice la cuenta y el simbolo del margen, sin peticiones
void ContextoMargen()
  {
   Dato(P8_MED, "contexto", "p8_modo_margen", EnumToString((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)));
   Dato(P8_MED, "contexto", "p8_margen_hedged", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_MARGIN_HEDGED), 2));
   Dato(P8_MED, "contexto", "p8_hedged_pierna_mayor", SymbolInfoInteger(SIMBOLO, SYMBOL_MARGIN_HEDGED_USE_LEG) != 0 ? "si" : "no");
   Dato(P8_MED, "contexto", "p8_margen_inicial", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_MARGIN_INITIAL), 2));
   Dato(P8_MED, "contexto", "p8_volumen_limite", DoubleToString(SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_LIMIT), 2));
   double ini = 0.0, man = 0.0;
   if(SymbolInfoMarginRate(SIMBOLO, ORDER_TYPE_BUY_STOP, ini, man))
      Dato(P8_MED, "contexto", "p8_tasa_buy_stop", DoubleToString(ini, 4) + ";" + DoubleToString(man, 4), "inicial;mantenimiento");
   else
      Dato(P8_MED, "contexto", "p8_tasa_buy_stop", "sin dato", "SymbolInfoMarginRate fallo (error " + IntegerToString(GetLastError()) + ")");
   if(SymbolInfoMarginRate(SIMBOLO, ORDER_TYPE_BUY, ini, man))
      Dato(P8_MED, "contexto", "p8_tasa_buy", DoubleToString(ini, 4) + ";" + DoubleToString(man, 4), "inicial;mantenimiento");
   else
      Dato(P8_MED, "contexto", "p8_tasa_buy", "sin dato", "SymbolInfoMarginRate fallo (error " + IntegerToString(GetLastError()) + ")");
   Dato(P8_MED, "contexto", "p8_equidad", Usd(AccountInfoDouble(ACCOUNT_EQUITY)));
   Dato(P8_MED, "contexto", "p8_margen_usado", Usd(AccountInfoDouble(ACCOUNT_MARGIN)));
   Dato(P8_MED, "contexto", "p8_margen_libre", Usd(AccountInfoDouble(ACCOUNT_MARGIN_FREE)));
   Dato(P8_MED, "contexto", "p8_margen_pendientes", Usd(AccountInfoDouble(ACCOUNT_MARGIN_INITIAL)), "ACCOUNT_MARGIN_INITIAL");
   Dato(P8_MED, "contexto", "p8_tope_usd", Usd(P8_TOPE_USD));
   Dato(P8_MED, "contexto", "p8_deslizamiento_puntos", IntegerToString(P8_DESLIZ));
   Dato(P8_MED, "contexto", "p8_comision_lado_lote", Usd(P8_COMISION_LADO));
  }

//--- M1: rechaza al COLOCAR una pendiente cuyo margen no cabe en el libre?
bool MedirM1()
  {
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   double libre = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double paso = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP);
   double m1 = Margen(ORDER_TYPE_BUY, 1.0, t.ask);
   if(m1 <= 0.0)
     {
      Dato(P8_MED, P8_RESP, "m1_no_medible", "si", "no se pudo calcular el margen de 1 lote");
      return true;
     }
   // el menor volumen cuyo margen, al ask (el menor de los dos precios), pasa del libre
   double v = VolumenHaciaArriba(libre / m1);
   if(v > 0.0 && Margen(ORDER_TYPE_BUY, v, t.ask) <= libre)
      v = VolumenHaciaArriba(v + paso);
   double precio = NormalizeDouble(t.ask + P8_LEJOS * g_point, g_digits);
   Dato(P8_MED, P8_RESP, "m1_volumen", Lotes(v), "margen al ask " + Usd(Margen(ORDER_TYPE_BUY, v, t.ask)) +
        "; a la orden " + Usd(Margen(ORDER_TYPE_BUY_STOP, v, precio)) + "; margen libre " + Usd(libre));
   if(v <= 0.0)
     {
      Dato(P8_MED, P8_RESP, "m1_no_medible", "si", "el volumen necesario pasa del maximo por orden");
      return true;
     }
   double vols[1];
   double precios[1];
   vols[0] = v;
   precios[0] = precio;
   int stop = StopDelTope("m1", vols, precios, 1);
   if(stop == 0)
     {
      Dato(P8_MED, P8_RESP, "m1_no_medible", "si", "el tope de perdida no deja un stop de proteccion");
      return true;
     }
   MqlTradeResult res;
   ColocarBuyStop(v, precio, stop, "MedirDemoFTMO m1", true, res);
   double resultado = 0.0;
   string nota = res.comment;
   string colocada = Desenlace(res.order, true, resultado, nota);
   Fila(P8_MED, P8_RESP, "m1_colocar", Lotes(v), res.retcode, colocada, "buy_stop", precio, t.bid, t.ask,
        resultado, IntegerToString(P8_LEJOS), nota);
   return true;
  }

//--- M2: carga margen una stop viva, y a que precio? carga: 1 si, 0 no, -1 no concluyente
bool MedirM2(int &carga)
  {
   carga = -1;
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   double precio = NormalizeDouble(t.ask + P8_LEJOS * g_point, g_digits);
   double d1 = Margen(ORDER_TYPE_BUY_STOP, 1.0, precio) - Margen(ORDER_TYPE_BUY, 1.0, t.ask);
   double m1 = Margen(ORDER_TYPE_BUY, 1.0, t.ask);
   if(m1 <= 0.0)
     {
      Dato(P8_MED, P8_RESP, "m2_no_medible", "si", "no se pudo calcular el margen de 1 lote");
      return true;
     }
   // con diferencia por lote, el volumen que la lleva a P8_DIF_MIN; sin ella, unos 2000 de margen
   double v = (d1 > 0.0) ? VolumenHaciaArriba(P8_DIF_MIN / d1) : VolumenHaciaArriba(2000.0 / m1);
   double mo = Margen(ORDER_TYPE_BUY_STOP, v, precio);
   double mm = Margen(ORDER_TYPE_BUY, v, t.ask);
   Dato(P8_MED, P8_RESP, "m2_volumen", Lotes(v), "margen a la orden " + Usd(mo) + "; al mercado " + Usd(mm) +
        "; diferencia " + Usd(mo - mm));
   if(v <= 0.0)
     {
      Dato(P8_MED, P8_RESP, "m2_no_medible", "si", "volumen no admitido");
      return true;
     }
   double vols[1];
   double precios[1];
   vols[0] = v;
   precios[0] = precio;
   int stop = StopDelTope("m2", vols, precios, 1);
   if(stop == 0)
     {
      Dato(P8_MED, P8_RESP, "m2_no_medible", "si", "el tope de perdida no deja un stop de proteccion");
      return true;
     }
   double usado0 = AccountInfoDouble(ACCOUNT_MARGIN);
   double libre0 = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double ini0 = AccountInfoDouble(ACCOUNT_MARGIN_INITIAL);
   MqlTradeResult res;
   ColocarBuyStop(v, precio, stop, "MedirDemoFTMO m2", false, res);
   int espera = EsperarCuenta(libre0, usado0, ini0);
   double usado1 = AccountInfoDouble(ACCOUNT_MARGIN);
   double libre1 = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double ini1 = AccountInfoDouble(ACCOUNT_MARGIN_INITIAL);
   double resultado = 0.0;
   string nota = res.comment;
   string colocada = Desenlace(res.order, true, resultado, nota);
   Fila(P8_MED, P8_RESP, "m2_colocar", Lotes(v), res.retcode, colocada, "buy_stop", precio, t.bid, t.ask,
        resultado, IntegerToString(P8_LEJOS), nota);
   Dato(P8_MED, P8_RESP, "m2_margen_antes", Usd(usado0), "ACCOUNT_MARGIN");
   Dato(P8_MED, P8_RESP, "m2_margen_despues", Usd(usado1), "ACCOUNT_MARGIN");
   Dato(P8_MED, P8_RESP, "m2_libre_antes", Usd(libre0), "ACCOUNT_MARGIN_FREE");
   Dato(P8_MED, P8_RESP, "m2_libre_despues", Usd(libre1), "ACCOUNT_MARGIN_FREE");
   Dato(P8_MED, P8_RESP, "m2_inicial_antes", Usd(ini0), "ACCOUNT_MARGIN_INITIAL");
   Dato(P8_MED, P8_RESP, "m2_inicial_despues", Usd(ini1), "ACCOUNT_MARGIN_INITIAL");
   Dato(P8_MED, P8_RESP, "m2_calculado_orden", Usd(mo), "OrderCalcMargin al precio de la orden");
   Dato(P8_MED, P8_RESP, "m2_calculado_mercado", Usd(mm), "OrderCalcMargin al ask al colocar");
   Dato(P8_MED, P8_RESP, "m2_espera_ms", IntegerToString(espera));
   // la misma regla que el lector (scripts/leer_demo_ftmo.py, M2): por la bajada del margen libre
   if(colocada == "si" && mm > 0.0)
     {
      double baja = libre0 - libre1;
      if(baja >= P8_CARGA * mm)
         carga = 1;
      else
         if(MathAbs(baja) < P8_CARGA * mm)
            carga = 0;
     }
   Dato(P8_MED, P8_RESP, "m2_carga_script", IntegerToString(carga), "1 carga, 0 no carga, -1 no concluyente: elige la ocupacion de M4");
   return true;
  }

//--- M3: suma las pendientes al colocar otra? suma: 1 si, 0 no, -1 no concluyente
bool MedirM3(int &suma)
  {
   suma = -1;
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   double libre = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double paso = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_STEP);
   double precio = NormalizeDouble(t.ask + P8_LEJOS * g_point, g_digits);
   double m1 = Margen(ORDER_TYPE_BUY, 1.0, t.ask);
   if(m1 <= 0.0)
     {
      Dato(P8_MED, P8_RESP, "m3_no_medible", "si", "no se pudo calcular el margen de 1 lote");
      return true;
     }
   // dos que caben solas (a cualquiera de los dos precios) y no juntas
   double v = VolumenHaciaArriba(1.10 * libre / (2.0 * m1));
   if(v > 0.0 && 2.0 * Margen(ORDER_TYPE_BUY, v, t.ask) < 1.10 * libre)
      v = VolumenHaciaArriba(v + paso);
   double mo = Margen(ORDER_TYPE_BUY_STOP, v, precio);
   Dato(P8_MED, P8_RESP, "m3_volumen", Lotes(v), "cada una; margen al ask " + Usd(Margen(ORDER_TYPE_BUY, v, t.ask)) +
        "; a la orden " + Usd(mo) + "; margen libre " + Usd(libre));
   double limite = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_LIMIT);
   if(v <= 0.0 || mo < 0.0 || mo > 0.90 * libre)
     {
      Dato(P8_MED, P8_RESP, "m3_no_medible", "si", "no hay un volumen que quepa solo y no junto");
      return true;
     }
   if(limite > 0.0 && 2.0 * v > limite + 1e-9)
     {
      Dato(P8_MED, P8_RESP, "m3_no_medible", "si", "las dos pasan del tope agregado de volumen (" + Lotes(limite) + ")");
      return true;
     }
   double vols[2];
   double precios[2];
   vols[0] = v;
   vols[1] = v;
   precios[0] = precio;
   precios[1] = precio;
   int stop = StopDelTope("m3", vols, precios, 2);
   if(stop == 0)
     {
      Dato(P8_MED, P8_RESP, "m3_no_medible", "si", "el tope de perdida no deja un stop de proteccion");
      return true;
     }
   MqlTradeResult r1;
   ColocarBuyStop(v, precio, stop, "MedirDemoFTMO m3 1", true, r1);
   double vivo1 = 0.0;
   bool viva1 = PendienteViva(r1.order, vivo1);
   Fila(P8_MED, P8_RESP, "m3_colocar_1", Lotes(v), r1.retcode, viva1 ? "si" : "no", "buy_stop", precio, t.bid, t.ask,
        vivo1, IntegerToString(P8_LEJOS), r1.comment);
   Dato(P8_MED, P8_RESP, "m3_margen_tras_1", Usd(AccountInfoDouble(ACCOUNT_MARGIN)), "ACCOUNT_MARGIN");
   Dato(P8_MED, P8_RESP, "m3_libre_tras_1", Usd(AccountInfoDouble(ACCOUNT_MARGIN_FREE)), "ACCOUNT_MARGIN_FREE");
   if(!viva1)
      return true; // la primera no esta viva: no concluyente; Limpiar quita lo que haya
   MqlTradeResult r2;
   ColocarBuyStop(v, precio, stop, "MedirDemoFTMO m3 2", true, r2);
   double vivo2 = 0.0;
   bool viva2 = PendienteViva(r2.order, vivo2);
   Fila(P8_MED, P8_RESP, "m3_colocar_2", Lotes(v), r2.retcode, viva2 ? "si" : "no", "buy_stop", precio, t.bid, t.ask,
        vivo2, IntegerToString(P8_LEJOS), r2.comment);
   if(viva2)
      suma = 0;
   else
      if(r2.retcode == 10019)
         suma = 1;
   return true;
  }

//--- M4: comprueba al LLENAR? Una stop S que cabe al colocarla; se ocupa el margen hasta que no
//--- cabe; se espera a que salte. La ocupacion la decide lo medido en M2 y M3 (MARGEN-PENDIENTE.md).
bool MedirM4(const int carga, const int suma)
  {
   string m = P8_MED;
   if(carga < 0)
     {
      Dato(m, P8_RESP, "m4_ocupacion", "no_medible", "M2 no concluyente: no se sabe si una pendiente ocupa margen");
      return true;
     }
   if(carga == 1 && suma != 0)
     {
      Dato(m, P8_RESP, "m4_ocupacion", "no_medible", suma == 1 ?
           "las pendientes cargan su margen y MT5 las suma al colocar: una stop que cupo al colocarla sigue cabiendo al saltar, salvo por perdida flotante" :
           "M3 no concluyente: no se sabe si se puede ocupar el margen con pendientes");
      return true;
     }
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   bool posicion = (carga == 0);
   double libre0 = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double precioS = NormalizeDouble(t.ask + (MathMax(g_stops, 1) + P8_CERCA) * g_point, g_digits);
   double precioO = posicion ? t.ask : NormalizeDouble(t.ask + P8_LEJOS * g_point, g_digits);
   double mS1 = Margen(ORDER_TYPE_BUY, 1.0, precioS);
   double mO1 = Margen(posicion ? ORDER_TYPE_BUY : ORDER_TYPE_BUY_STOP, 1.0, precioO);
   if(mS1 <= 0.0 || mO1 <= 0.0)
     {
      Dato(m, P8_RESP, "m4_ocupacion", "no_medible", "no se pudo calcular el margen de 1 lote");
      return true;
     }
   double vS, vO;
   if(posicion)
     {
      vS = VolumenHaciaAbajo(0.80 * libre0 / mS1); // S grande, que cabe sola
      vO = VolumenHaciaArriba(0.25 * libre0 / mO1); // y una compra pequena que deja el libre por debajo
     }
   else
     {
      vS = VolumenHaciaAbajo(0.20 * libre0 / mS1); // S pequena
      vO = VolumenHaciaArriba((libre0 - 0.5 * Margen(ORDER_TYPE_BUY, vS, precioS)) / mO1); // pendientes lejos
     }
   Dato(m, P8_RESP, "m4_ocupacion", posicion ? "posicion" : "pendientes",
        posicion ? "M2: la pendiente no carga margen; se ocupa con una compra a mercado del mismo lado" :
        "M2: la pendiente carga margen y M3: no las suma al colocar; se ocupa con buy stops lejos");
   Dato(m, P8_RESP, "m4_volumen_stop", Lotes(vS), "margen al llenar " + Usd(Margen(ORDER_TYPE_BUY, vS, precioS)) +
        "; margen libre " + Usd(libre0));
   Dato(m, P8_RESP, "m4_volumen_ocupacion", Lotes(vO));
   double limite = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_LIMIT);
   if(vS <= 0.0 || vO <= 0.0)
     {
      Dato(m, P8_RESP, "m4_no_medible", "si", "volumen no admitido (minimo o maximo por orden)");
      return true;
     }
   if(limite > 0.0 && vS + vO > limite + 1e-9)
     {
      Dato(m, P8_RESP, "m4_no_medible", "si", "S y la ocupacion pasan del tope agregado de volumen (" + Lotes(limite) + ")");
      return true;
     }
   double vols[2];
   double precios[2];
   vols[0] = vS;
   vols[1] = vO;
   precios[0] = precioS;
   precios[1] = precioO;
   int stop = StopDelTope("m4", vols, precios, 2);
   if(stop == 0)
     {
      Dato(m, P8_RESP, "m4_no_medible", "si", "el tope de perdida no deja un stop de proteccion");
      return true;
     }
   // S, sin pausa: la ocupacion va enseguida, antes de que el precio llegue a S
   double usadoA = AccountInfoDouble(ACCOUNT_MARGIN);
   double libreA = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double iniA = AccountInfoDouble(ACCOUNT_MARGIN_INITIAL);
   MqlTradeResult rs;
   ColocarBuyStop(vS, precioS, stop, "MedirDemoFTMO m4 S", false, rs);
   double vivoS = 0.0;
   bool vivaS = PendienteViva(rs.order, vivoS);
   Fila(m, P8_RESP, "m4_colocar_stop", Lotes(vS), rs.retcode, vivaS ? "si" : "no", "buy_stop", precioS, t.bid, t.ask,
        vivoS, IntegerToString((int)MathRound((precioS - t.ask) / g_point)), rs.comment);
   if(!vivaS)
     {
      double pl = 0.0;
      ulong ps = 0;
      double vl = VolumenLlenado(rs.order, pl, ps);
      Dato(m, P8_RESP, "m4_resultado", vl > 0.0 ? "salto_antes_de_ocupar" : "no_colocada",
           vl > 0.0 ? "S se lleno antes de ocupar el margen" : "S no se coloco");
      return true;
     }
   // el libre tras S: si la pendiente carga (M2), se espera a que la cuenta lo refleje; si no, se lee
   // enseguida, para no dar tiempo a que salte
   if(carga == 1)
      EsperarCuenta(libreA, usadoA, iniA);
   double libreS = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double usadoS = AccountInfoDouble(ACCOUNT_MARGIN);
   double iniS = AccountInfoDouble(ACCOUNT_MARGIN_INITIAL);
   // la ocupacion
   MqlTick o;
   if(!Cotizacion(o))
      return false;
   MqlTradeResult ro;
   if(posicion)
      AbrirCompra(vO, o, stop, ro);
   else
      ColocarBuyStop(vO, precioO, stop, "MedirDemoFTMO m4 ocupacion", true, ro);
   ulong ticketO = 0;
   string estadoO = "no";
   double resO = 0.0;
   if(posicion)
     {
      double pv = 0.0;
      if(VolumenLlenado(ro.order, pv, ticketO) > 0.0 && PosicionViva(ticketO))
        {
         estadoO = "llenada";
         resO = pv;
        }
     }
   else
     {
      double pv = 0.0;
      if(PendienteViva(ro.order, pv))
        {
         ticketO = ro.order;
         estadoO = "si";
         resO = pv;
        }
     }
   Fila(m, P8_RESP, "m4_ocupar", Lotes(vO), ro.retcode, estadoO, posicion ? "buy" : "buy_stop", posicion ? o.ask : precioO,
        o.bid, o.ask, resO, posicion ? "0" : IntegerToString(P8_LEJOS), ro.comment + "; ticket " + IntegerToString((long)ticketO));
   if(ticketO == 0)
     {
      Dato(m, P8_RESP, "m4_no_medible", "si", "la ocupacion no quedo puesta");
      return true;
     }
   double ignora = 0.0;
   if(!PendienteViva(rs.order, ignora))
     {
      double pl = 0.0;
      ulong ps = 0;
      Dato(m, P8_RESP, "m4_resultado", "salto_antes_de_ocupar",
           VolumenLlenado(rs.order, pl, ps) > 0.0 ? "S se lleno mientras se ocupaba el margen" : "S desaparecio mientras se ocupaba el margen");
      return true;
     }
   EsperarCuenta(libreS, usadoS, iniS);
   double libreO = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double margenS = Margen(ORDER_TYPE_BUY, vS, precioS);
   // lo que reservo S, medido: el libre antes de colocarla menos el libre con ella puesta
   double reservado = libreA - libreS;
   Dato(m, P8_RESP, "m4_libre_antes_stop", Usd(libreA), "ACCOUNT_MARGIN_FREE antes de colocar S");
   Dato(m, P8_RESP, "m4_libre_tras_stop", Usd(libreS), "ACCOUNT_MARGIN_FREE con S puesta, antes de ocupar");
   Dato(m, P8_RESP, "m4_libre_tras_ocupar", Usd(libreO), "ACCOUNT_MARGIN_FREE con S y la ocupacion puestas");
   Dato(m, P8_RESP, "m4_margen_stop", Usd(margenS), "OrderCalcMargin de S al llenar, a su precio");
   if(!(libreO + reservado < margenS))
     {
      Dato(m, P8_RESP, "m4_no_medible", "si", "con la ocupacion puesta, S todavia cabe al llenar");
      return true;
     }
   // la espera: en cada vuelta, el libre y si la ocupacion sigue viva, y despues si S sigue viva
   datetime limite_t = TimeLocal() + InpEsperaMargenSeg;
   bool resuelta = false;
   bool viva_siempre = true;
   double libre_lectura = libreO;
   while(TimeLocal() < limite_t)
     {
      Sleep(500);
      libre_lectura = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
      double pv = 0.0;
      bool vivaO = posicion ? PosicionViva(ticketO) : PendienteViva(ticketO, pv);
      if(!vivaO)
         viva_siempre = false;
      if(!PendienteViva(rs.order, pv))
        {
         resuelta = true;
         break;
        }
     }
   Dato(m, P8_RESP, "m4_ocupacion_viva", viva_siempre ? "si" : "no", "ticket " + IntegerToString((long)ticketO));
   Dato(m, P8_RESP, "m4_libre_al_resolver", Usd(libre_lectura), "ACCOUNT_MARGIN_FREE justo antes de leer S");
   MqlTick a;
   Cotizacion(a);
   if(!resuelta)
     {
      Fila(m, P8_RESP, "m4_resultado", "no_salto", 0, "no", "buy_stop", precioS, a.bid, a.ask, 0, "",
           "no salto en " + IntegerToString(InpEsperaMargenSeg) + " s", true);
      return true;
     }
   double pl = 0.0;
   ulong ps = 0;
   double vl = VolumenLlenado(rs.order, pl, ps);
   if(vl > 0.0)
     {
      Fila(m, P8_RESP, "m4_resultado", "llenada", 0, "llenada", "buy_stop", precioS, a.bid, a.ask, pl, "",
           "volumen del deal " + Lotes(vl) + " de " + Lotes(vS), true);
      Dato(m, P8_RESP, "m4_volumen_deal", Lotes(vl));
      return true;
     }
   // sin deal: lo que guarda el historial de la orden
   string estado = "sin historial";
   string comentario = "";
   string motivo = "";
   HistorySelect(TimeTradeServer() - 86400, TimeTradeServer() + 3600);
   if(HistoryOrderSelect(rs.order))
     {
      estado = EnumToString((ENUM_ORDER_STATE)HistoryOrderGetInteger(rs.order, ORDER_STATE));
      comentario = HistoryOrderGetString(rs.order, ORDER_COMMENT);
      motivo = EnumToString((ENUM_ORDER_REASON)HistoryOrderGetInteger(rs.order, ORDER_REASON));
     }
   Fila(m, P8_RESP, "m4_resultado", "sin_deal", 0, "no", "buy_stop", precioS, a.bid, a.ask, 0, "",
        "S desaparecio sin deal", true);
   Dato(m, P8_RESP, "m4_estado", estado, "ORDER_STATE del historial");
   Dato(m, P8_RESP, "m4_comentario", comentario, "ORDER_COMMENT del historial, literal");
   Dato(m, P8_RESP, "m4_motivo", motivo, "ORDER_REASON del historial");
   return true;
  }

bool MedirMargen()
  {
   Limpiar("antes_paso_8");
   ContextoMargen();
   int carga = -1;
   int suma = -1;
   bool ok = MedirM1();
   Limpiar("tras_m1");
   if(ok)
      ok = MedirM2(carga);
   Limpiar("tras_m2");
   if(ok)
      ok = MedirM3(suma);
   Limpiar("tras_m3");
   if(ok)
      ok = MedirM4(carga, suma);
   Limpiar("tras_m4");
   Dato(P8_MED, "contexto", "p8_fin", ok ? "hecho" : "incompleto");
   return ok;
  }

void OnStart()
  {
   string motivo = "";
   if(!Comprobaciones(motivo))
     {
      Alert("MedirDemoFTMO: ", motivo);
      return;
     }
   g_digits = (int)SymbolInfoInteger(SIMBOLO, SYMBOL_DIGITS);
   g_point = SymbolInfoDouble(SIMBOLO, SYMBOL_POINT);
   g_volumen = SymbolInfoDouble(SIMBOLO, SYMBOL_VOLUME_MIN);
   g_stops = (int)SymbolInfoInteger(SIMBOLO, SYMBOL_TRADE_STOPS_LEVEL);

   MqlDateTime s;
   TimeToStruct(TimeTradeServer(), s);
   string nombre = StringFormat("MedirDemoFTMO_%04d%02d%02d_%02d%02d%02d.csv", s.year, s.mon, s.day, s.hour, s.min, s.sec);
   g_csv = FileOpen(nombre, FILE_WRITE | FILE_TXT | FILE_ANSI);
   if(g_csv == INVALID_HANDLE)
     {
      Alert("MedirDemoFTMO: no se pudo crear ", nombre, " (error ", GetLastError(), ")");
      return;
     }
   EscribirCabecera();
   Dato("0_arranque", "contexto", "version_script", VERSION_SCRIPT);
   Dato("0_arranque", "contexto", "cuenta_demo", "si");
   Limpiar("al_empezar");

   bool ok = MedirEspecificacion();
   if(ok) ok = MedirReloj();
   if(ok) ok = MedirLadoEquivocado();
   if(ok) Limpiar("tras_paso_3");
   if(ok) ok = MedirDistancias();
   if(ok) Limpiar("tras_paso_4");
   if(ok) ok = MedirModificacion();
   if(ok) Limpiar("tras_paso_5");
   if(ok) ok = MedirComision();
   if(ok) Limpiar("tras_paso_6");
   if(ok && InpMedirLlenadoStop) ok = MedirLlenadoStop();
   if(ok && InpMedirMargen)
      ok = MedirMargen();
   else
      if(ok)
         Dato(P8_MED, "contexto", "p8_fin", "desactivado");
   if(!ok)
      Dato("error", "seguridad", "paso_fallido", "si", "un paso no pudo leer la cotizacion; se limpia y se termina");
   int quedan = Limpiar("al_terminar");
   Dato("9_fin", "contexto", "terminado", ok ? "completo" : "incompleto");
   FileClose(g_csv);
   g_csv = INVALID_HANDLE;
   string msg = "MedirDemoFTMO: terminado (" + (ok ? "completo" : "INCOMPLETO") + "). Fichero: MQL5\\Files\\" + nombre;
   if(quedan != 0)
      msg += ". ATENCION: quedan " + IntegerToString(quedan) + " ordenes o posiciones del script";
   Alert(msg);
  }
//+------------------------------------------------------------------+
