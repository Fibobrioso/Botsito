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
//| SEGURIDAD:                                                       |
//| - se niega a correr si la cuenta no es DEMO;                     |
//| - solo EURUSD, solo el volumen minimo, numero magico propio;     |
//| - toda pendiente lleva caducidad (si el simbolo la admite) y     |
//|   toda posicion lleva stop de proteccion;                        |
//| - al empezar y al terminar, y tambien si un paso falla, borra    |
//|   toda pendiente y cierra toda posicion con su numero magico, y  |
//|   comprueba que no queda ninguna.                                |
//+------------------------------------------------------------------+
#property copyright "Bot v3"
#property version   "1.00"
#property description "Mide especificacion, reloj, pendientes mal colocadas, stops level, modificacion y comision en una cuenta DEMO. Solo EURUSD."
#property script_show_inputs

#define VERSION_SCRIPT "1.0"
#define SIMBOLO        "EURUSD"
#define MAGICO         57057000

input bool InpMedirLlenadoStop = true; // medir el llenado de una orden stop (paso 7)
input int  InpEsperaStopSeg    = 120;  // segundos maximos esperando a que salte la stop del paso 7
input int  InpPausaMs          = 1500; // pausa entre peticiones al servidor

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
          const string nota)
  {
   g_fila++;
   string r = (retcode == 0 && StringLen(tipo) == 0) ? "" : IntegerToString(retcode);
   string rt = (StringLen(r) == 0) ? "" : TextoRetcode(retcode);
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
bool MedirComision()
  {
   string m = "6_comision";
   string resp = "FTMO-REGLAS R12; ADR-0057 d1 (deslizamiento)";
   MqlTick t;
   if(!Cotizacion(t))
      return false;
   MqlTradeRequest req;
   MqlTradeResult res;
   ZeroMemory(req);
   ZeroMemory(res);
   int proteccion = 200 + g_stops; // stop de proteccion: 20 pips, por si el script se corta
   req.action = TRADE_ACTION_DEAL;
   req.symbol = SIMBOLO;
   req.magic = MAGICO;
   req.volume = g_volumen;
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
           "valor = precio del llenado menos el nivel, en puntos (+ en contra)");
      MqlTradeResult rc;
      CerrarPosicion(posicion, rc);
     }
   else
     {
      Fila(m, "ADR-0057 d1", "buy_stop_llenado", "no_salto", 0, "no", "buy_stop", nivel, a.bid, a.ask, 0,
           IntegerToString(d), "no salto en " + IntegerToString(InpEsperaStopSeg) + " s; se borra");
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
