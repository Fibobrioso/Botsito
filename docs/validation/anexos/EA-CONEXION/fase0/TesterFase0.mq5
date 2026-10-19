//+------------------------------------------------------------------+
//| TesterFase0.mq5 - medida de la fase 0 de trabajo/ea-conexion en  |
//| el Strategy Tester. Fuera del repositorio. No opera: cuenta los  |
//| ticks y lee el modo de la cuenta y las sesiones. Escribe en      |
//| Terminal/Common/Files/Botsito_fase0/tester.txt (FILE_COMMON).    |
//+------------------------------------------------------------------+
int    g_out = INVALID_HANDLE;
long   g_ticks = 0;
datetime g_primero = 0, g_ultimo = 0;

void Linea(const string s)
  {
   uchar b[];
   int n = StringToCharArray(s + "\n", b, 0, -1, CP_UTF8);
   if(n > 0 && b[n - 1] == 0)
      ArrayResize(b, n - 1);
   FileWriteArray(g_out, b);
   FileFlush(g_out);
  }

int OnInit()
  {
   g_out = FileOpen("Botsito_fase0\\tester.txt", FILE_WRITE | FILE_BIN | FILE_COMMON);
   if(g_out == INVALID_HANDLE)
      return INIT_FAILED;
   Linea("medida|TesterFase0|1");
   Linea("mql_tester|" + IntegerToString(MQLInfoInteger(MQL_TESTER)));
   Linea("terminal_connected|" + IntegerToString(TerminalInfoInteger(TERMINAL_CONNECTED)));
   Linea("account_trade_mode|" + EnumToString((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE)));
   Linea("account_margin_mode|" + EnumToString((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)));
   Linea("account_server|" + AccountInfoString(ACCOUNT_SERVER));
   Linea("time_trade_server|" + TimeToString(TimeTradeServer(), TIME_DATE | TIME_SECONDS));
   Linea("time_current|" + TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS));
   Linea("time_gmt|" + TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS));
   for(int d = 0; d < 7; d++)
     {
      datetime a = 0, z = 0;
      ResetLastError();
      bool ok = SymbolInfoSessionTrade(_Symbol, (ENUM_DAY_OF_WEEK)d, 0, a, z);
      Linea(StringFormat("sesion_trade|%s|0|%s|%s|%s|error=%d", EnumToString((ENUM_DAY_OF_WEEK)d), ok ? "si" : "no",
                         TimeToString(a, TIME_MINUTES), TimeToString(z, TIME_MINUTES), GetLastError()));
     }
   return INIT_SUCCEEDED;
  }

void OnTick()
  {
   MqlTick t;
   if(SymbolInfoTick(_Symbol, t))
     {
      if(g_ticks == 0)
         g_primero = t.time;
      g_ultimo = t.time;
     }
   g_ticks++;
  }

void OnDeinit(const int reason)
  {
   if(g_out == INVALID_HANDLE)
      return;
   Linea("ticks|" + IntegerToString(g_ticks));
   Linea("primer_tick|" + TimeToString(g_primero, TIME_DATE | TIME_SECONDS));
   Linea("ultimo_tick|" + TimeToString(g_ultimo, TIME_DATE | TIME_SECONDS));
   Linea("deinit_reason|" + IntegerToString(reason));
   FileClose(g_out);
  }
