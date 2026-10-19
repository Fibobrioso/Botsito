//+------------------------------------------------------------------+
//| MedirFase0b.mq5 - fase 0 de trabajo/ea-conexion: valores enteros |
//| de ENUM_ACCOUNT_TRADE_MODE y que se lee de la cuenta ANTES de    |
//| conectar. Fuera del repositorio. No opera. No escribe el login:  |
//| solo si es distinto de cero.                                     |
//+------------------------------------------------------------------+
int g_out = INVALID_HANDLE;

void Linea(const string s)
  {
   uchar b[];
   int n = StringToCharArray(s + "\n", b, 0, -1, CP_UTF8);
   if(n > 0 && b[n - 1] == 0)
      ArrayResize(b, n - 1);
   FileWriteArray(g_out, b);
   FileFlush(g_out);
  }

void Estado(const string cuando)
  {
   ResetLastError();
   long modo = AccountInfoInteger(ACCOUNT_TRADE_MODE);
   int e1 = GetLastError();
   ResetLastError();
   long login = AccountInfoInteger(ACCOUNT_LOGIN);
   int e2 = GetLastError();
   Linea(StringFormat("%s|connected=%d|trade_mode=%d|error_trade_mode=%d|login_distinto_de_cero=%s|error_login=%d|servidor_vacio=%s|margin_mode=%d",
                      cuando, (int)TerminalInfoInteger(TERMINAL_CONNECTED), (int)modo, e1,
                      login != 0 ? "si" : "no", e2, AccountInfoString(ACCOUNT_SERVER) == "" ? "si" : "no",
                      (int)AccountInfoInteger(ACCOUNT_MARGIN_MODE)));
  }

void OnStart()
  {
   g_out = FileOpen("Botsito_fase0\\medida_b.txt", FILE_WRITE | FILE_BIN);
   if(g_out == INVALID_HANDLE)
      return;
   Linea(StringFormat("enum|DEMO=%d|CONTEST=%d|REAL=%d", (int)ACCOUNT_TRADE_MODE_DEMO,
                      (int)ACCOUNT_TRADE_MODE_CONTEST, (int)ACCOUNT_TRADE_MODE_REAL));
   Linea(StringFormat("enum_margen|NETTING=%d|EXCHANGE=%d|HEDGING=%d", (int)ACCOUNT_MARGIN_MODE_RETAIL_NETTING,
                      (int)ACCOUNT_MARGIN_MODE_EXCHANGE, (int)ACCOUNT_MARGIN_MODE_RETAIL_HEDGING));
   Linea(StringFormat("init|SUCCEEDED=%d|FAILED=%d", (int)INIT_SUCCEEDED, (int)INIT_FAILED));
   Estado("antes_de_conectar");
   uint t0 = GetTickCount();
   while(!TerminalInfoInteger(TERMINAL_CONNECTED) && GetTickCount() - t0 < 60000 && !IsStopped())
      Sleep(250);
   Sleep(3000);
   Estado("conectado");
   FileClose(g_out);
  }
