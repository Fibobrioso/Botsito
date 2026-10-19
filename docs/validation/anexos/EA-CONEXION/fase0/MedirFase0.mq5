//+------------------------------------------------------------------+
//| MedirFase0.mq5 - medida de la fase 0 de trabajo/ea-conexion.     |
//| Fuera del repositorio. No llama a ninguna funcion de trading.    |
//| Escribe MQL5/Files/Botsito_fase0/*.                              |
//+------------------------------------------------------------------+
#property script_show_inputs false

int g_out = INVALID_HANDLE;

void Linea(const string s)
  {
   uchar b[];
   int n = StringToCharArray(s + "\n", b, 0, -1, CP_UTF8);
   if(n > 0 && b[n - 1] == 0)
      ArrayResize(b, n - 1);
   FileWriteArray(g_out, b);
   FileFlush(g_out);
   Print(s);
  }

string Hex(const uchar &h[])
  {
   string r = "";
   for(int i = 0; i < ArraySize(h); i++)
      r += StringFormat("%02x", h[i]);
   return r;
  }

string Sha(const string s)
  {
   uchar d[], k[], h[];
   int n = StringToCharArray(s, d, 0, -1, CP_UTF8);
   if(n > 0 && d[n - 1] == 0)
      ArrayResize(d, n - 1);
   int r = CryptEncode(CRYPT_HASH_SHA256, d, k, h);
   return IntegerToString(r) + ":" + Hex(h);
  }

string Dia(const int d)
  {
   return EnumToString((ENUM_DAY_OF_WEEK)d);
  }

void Sesiones(const string tipo)
  {
   for(int d = 0; d < 7; d++)
     {
      for(uint i = 0; i < 12; i++)
        {
         datetime a = 0, z = 0;
         ResetLastError();
         bool ok = (tipo == "trade") ? SymbolInfoSessionTrade(_Symbol, (ENUM_DAY_OF_WEEK)d, i, a, z)
                                     : SymbolInfoSessionQuote(_Symbol, (ENUM_DAY_OF_WEEK)d, i, a, z);
         if(!ok)
           {
            Linea(StringFormat("sesion_%s|%s|%u|fin|error=%d", tipo, Dia(d), i, GetLastError()));
            break;
           }
         Linea(StringFormat("sesion_%s|%s|%u|%s|%s|from_seg=%d|to_seg=%d", tipo, Dia(d), i,
                            TimeToString(a, TIME_MINUTES), TimeToString(z, TIME_MINUTES), (int)a, (int)z));
        }
     }
  }

void Bytes()
  {
   // A: como MedirDemoFTMO (texto ANSI con \r\n), mas una linea con \n suelto y otra sin fin
   int h = FileOpen("Botsito_fase0\\bytes_txt_ansi.txt", FILE_WRITE | FILE_TXT | FILE_ANSI);
   FileWriteString(h, "uno\r\n");
   FileWriteString(h, "dos\n");
   FileWriteString(h, "tres");
   FileClose(h);
   // B: texto UNICODE
   h = FileOpen("Botsito_fase0\\bytes_txt_unicode.txt", FILE_WRITE | FILE_TXT | FILE_UNICODE);
   FileWriteString(h, "uno\r\n");
   FileWriteString(h, "dos\n");
   FileClose(h);
   // C: binario con bytes UTF-8 hechos a mano
   h = FileOpen("Botsito_fase0\\bytes_bin_utf8.txt", FILE_WRITE | FILE_BIN);
   uchar b[];
   int n = StringToCharArray("año|línea\n", b, 0, -1, CP_UTF8);
   Linea(StringFormat("bytes_bin_utf8|StringToCharArray devuelve %d", n));
   if(n > 0 && b[n - 1] == 0)
      ArrayResize(b, n - 1);
   uint w = FileWriteArray(h, b);
   Linea(StringFormat("bytes_bin_utf8|FileWriteArray escribe %u", w));
   FileFlush(h);
   FileClose(h);
   // D: reabrir C para anadir (READ|WRITE|BIN y seek al final)
   h = FileOpen("Botsito_fase0\\bytes_bin_utf8.txt", FILE_READ | FILE_WRITE | FILE_BIN);
   Linea(StringFormat("anadir|tamano_al_abrir=%d", (int)FileSize(h)));
   FileSeek(h, 0, SEEK_END);
   n = StringToCharArray("segunda\n", b, 0, -1, CP_UTF8);
   if(n > 0 && b[n - 1] == 0)
      ArrayResize(b, n - 1);
   FileWriteArray(h, b);
   FileClose(h);
   // E: reabrir con WRITE|BIN sin READ: si trunca
   h = FileOpen("Botsito_fase0\\bytes_bin_trunca.txt", FILE_WRITE | FILE_BIN);
   FileWriteArray(h, b);
   FileClose(h);
   h = FileOpen("Botsito_fase0\\bytes_bin_trunca.txt", FILE_WRITE | FILE_BIN);
   Linea(StringFormat("trunca|tamano_al_reabrir_solo_write=%d", (int)FileSize(h)));
   FileClose(h);
  }

void OnStart()
  {
   g_out = FileOpen("Botsito_fase0\\medida.txt", FILE_WRITE | FILE_BIN | FILE_SHARE_READ);
   if(g_out == INVALID_HANDLE)
     {
      Print("MedirFase0: no se pudo abrir medida.txt, error ", GetLastError());
      return;
     }
   Linea("medida|MedirFase0|2");
   Linea("terminal_build|" + IntegerToString(TerminalInfoInteger(TERMINAL_BUILD)));
   Linea("antes_de_esperar|connected=" + IntegerToString(TerminalInfoInteger(TERMINAL_CONNECTED)) +
         "|margin_mode=" + EnumToString((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)) +
         "|desfase_seg=" + IntegerToString((long)(TimeTradeServer() - TimeGMT())));
   uint t0 = GetTickCount();
   while(!TerminalInfoInteger(TERMINAL_CONNECTED) && GetTickCount() - t0 < 60000 && !IsStopped())
      Sleep(250);
   Sleep(3000);
   Linea("espera_conexion_ms|" + IntegerToString(GetTickCount() - t0));
   Linea("terminal_connected|" + IntegerToString(TerminalInfoInteger(TERMINAL_CONNECTED)));
   Linea("mql_tester|" + IntegerToString(MQLInfoInteger(MQL_TESTER)));
   Linea("account_trade_mode|" + EnumToString((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE)));
   Linea("account_margin_mode|" + EnumToString((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)));
   Linea("account_server|" + AccountInfoString(ACCOUNT_SERVER));
   Linea("symbol|" + _Symbol);
   datetime srv = TimeTradeServer();
   datetime gmt = TimeGMT();
   Linea("time_trade_server|" + TimeToString(srv, TIME_DATE | TIME_SECONDS));
   Linea("time_current|" + TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS));
   Linea("time_gmt|" + TimeToString(gmt, TIME_DATE | TIME_SECONDS));
   Linea("time_local|" + TimeToString(TimeLocal(), TIME_DATE | TIME_SECONDS));
   Linea("desfase_servidor_gmt_seg|" + IntegerToString((long)(srv - gmt)));
   Linea("time_gmt_offset|" + IntegerToString(TimeGMTOffset()));
   Linea("time_daylight_savings|" + IntegerToString(TimeDaylightSavings()));
   Linea("sha256_abc|" + Sha("abc"));
   Linea("sha256_vacio|" + Sha(""));
   Linea("sha256_utf8|" + Sha("año|línea"));
   Sesiones("trade");
   Sesiones("quote");
   Bytes();
   Linea("fin|ok");
   FileClose(g_out);
  }
