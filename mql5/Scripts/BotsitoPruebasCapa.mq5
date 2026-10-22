//+------------------------------------------------------------------+
//| BotsitoPruebasCapa.mq5 - las pruebas dinamicas de la capa de MT5 |
//| (D4 (2) de trabajo/ea-conexion, R6a.1). No opera.                |
//|                                                                  |
//| Con los mismos include que el EA:                                |
//| - la negativa con DEMO, CONTEST y REAL;                          |
//| - el escritor del journal: escribe en MQL5\Files\Botsito\pruebas\|
//|   las cadenas de tests/golden/journal/ (continua: un reinicio que |
//|   sigue la cadena y un cambio de dia; rota: tras una ultima      |
//|   linea truncada), que se comparan byte a byte con el golden     |
//|   fuera de MT5 (src/botsito/mql5bridge/compilar.py);             |
//| - el cambio de dia con fechas inyectadas;                        |
//| - el SHA-256 y el texto JSON;                                    |
//| - y, sin comparar, la lectura real de la cuenta, el reloj y las  |
//|   sesiones del simbolo del grafico.                              |
//| Resultado: MQL5\Files\Botsito\pruebas\resultado.txt, una linea   |
//| OK|... o FALLO|... por prueba y un RESUMEN al final.             |
//+------------------------------------------------------------------+
#property copyright "Bot v3"
#property version   "1.00"
#property description "Pruebas dinamicas de la capa de MT5 (R6a.1). No opera."

#include <Botsito/Capa/Journal.mqh>
#include <Botsito/Capa/Cuenta.mqh>
#include <Botsito/Capa/Reloj.mqh>
#include <Botsito/Capa/Sesiones.mqh>

int g_res = INVALID_HANDLE;
int g_ok = 0;
int g_fallos = 0;

void Resultado(const string s)
  {
   uchar b[];
   Utf8(s + "\n", b);
   FileWriteArray(g_res, b);
   FileFlush(g_res);
  }

void Comprobar(const bool ok, const string nombre, const string detalle = "")
  {
   if(ok)
      g_ok++;
   else
      g_fallos++;
   Resultado((ok ? "OK|" : "FALLO|") + nombre + (StringLen(detalle) > 0 ? "|" + detalle : ""));
  }

void Borrar(const string carpeta, const string nombre)
  {
   FileDelete(carpeta + "\\" + nombre);
  }

datetime T(const string texto)
  {
   return StringToTime(texto);
  }

//--- los casos del golden (docs/validation/anexos/EA-CONEXION/fase1/generar_golden.py) -----------

string Servidor()
  {
   return "Servidor \"Prueba\" " + ShortToString(241) + "\\" + ShortToString(252);
  }

string ArranqueGolden(const string cadena, const bool conectado)
  {
   return DatosArranque("1.0", 6230, "XYZ.prueba", conectado, cadena);
  }

string CuentaGolden(const string trade_mode)
  {
   return DatosCuenta(trade_mode, "ACCOUNT_MARGIN_MODE_RETAIL_HEDGING", Servidor(), true);
  }

string RelojGolden()
  {
   return DatosReloj(T("2026.10.26 23:51:58"), T("2026.10.26 23:52:00"), T("2026.10.26 21:52:00"),
                     T("2026.10.26 16:52:00"), 18000, 0);
  }

string SesionesGolden()
  {
   string trade[7], quote[7];
   for(int d = 0; d < 7; d++)
     {
      trade[d] = (d >= 1 && d <= 5) ? "[300,86100]" : "";
      quote[d] = trade[d];
     }
   quote[1] = "[0,3600],[3660,86340]";
   return DatosSesiones(JsonSemana(trade), JsonSemana(quote), false);
  }

void E(const string srv, const string gmt, const string ev, const string datos)
  {
   JournalEscribir(T(srv), T(gmt), ev, datos);
  }

void Continua()
  {
   string c = "Botsito\\pruebas\\continua";
   Borrar(c, "journal_20261026.jsonl");
   Borrar(c, "journal_20261027.jsonl");
   string cadena = JournalAbrir(c);
   Comprobar(cadena == "ninguna", "continua: sin journal anterior, cadena ninguna", cadena);
   E("2026.10.26 23:50:00", "2026.10.26 21:50:00", "arranque", ArranqueGolden(cadena, false));
   E("2026.10.26 23:51:00", "2026.10.26 21:51:00", "latido", DatosLatido(false, T("2026.10.23 23:54:59")));
   E("2026.10.26 23:52:00", "2026.10.26 21:52:00", "cuenta", CuentaGolden("ACCOUNT_TRADE_MODE_DEMO"));
   E("2026.10.26 23:52:00", "2026.10.26 21:52:00", "reloj", RelojGolden());
   E("2026.10.26 23:52:00", "2026.10.26 21:52:00", "sesiones", SesionesGolden());
   E("2026.10.26 23:53:00", "2026.10.26 21:53:00", "latido", DatosLatido(true, T("2026.10.26 23:52:59")));
   E("2026.10.26 23:54:00", "2026.10.26 21:54:00", "fin", DatosFin(REASON_REMOVE));
   JournalCerrar();
   // el reinicio: la cadena sigue en el mismo fichero
   cadena = JournalAbrir(c);
   Comprobar(cadena == "sigue", "continua: tras el reinicio, cadena sigue", cadena);
   Comprobar(g_journal_seq == 7, "continua: el seq sigue en 7", JEntero(g_journal_seq));
   E("2026.10.26 23:56:00", "2026.10.26 21:56:00", "arranque", ArranqueGolden(cadena, true));
   E("2026.10.26 23:56:00", "2026.10.26 21:56:00", "cuenta", CuentaGolden("ACCOUNT_TRADE_MODE_DEMO"));
   E("2026.10.26 23:59:00", "2026.10.26 21:59:00", "latido", DatosLatido(true, T("2026.10.26 23:58:59")));
   // el cambio de dia: otro fichero, la misma cadena
   E("2026.10.27 00:00:00", "2026.10.26 22:00:00", "cambio_de_dia",
     DatosCambioDeDia(T("2026.10.26 23:59:00"), T("2026.10.27 00:00:00")));
   E("2026.10.27 00:00:00", "2026.10.26 22:00:00", "sesiones", SesionesGolden());
   E("2026.10.27 00:01:00", "2026.10.26 22:01:00", "fin", DatosFin(REASON_PROGRAM));
   JournalCerrar();
  }

void Rota()
  {
   string c = "Botsito\\pruebas\\rota";
   Borrar(c, "journal_20261027.jsonl");
   Borrar(c, "journal_20261028.jsonl");
   // sin journal: ninguna; con una ultima linea sin LF o que no es del formato: rota
   string cadena = JournalAbrir(c);
   Comprobar(cadena == "ninguna", "rota: carpeta vacia, cadena ninguna", cadena);
   JournalCerrar();
   int h = FileOpen(c + "\\journal_20261027.jsonl", FILE_WRITE | FILE_BIN);
   uchar b[];
   Utf8("{\"v\":1,\"seq\":5,\"srv\":\"2026-10-27T", b);
   FileWriteArray(h, b);
   FileClose(h);
   cadena = JournalAbrir(c);
   Comprobar(cadena == "rota", "rota: ultima linea sin LF, cadena rota", cadena);
   JournalCerrar();
   h = FileOpen(c + "\\journal_20261027.jsonl", FILE_WRITE | FILE_BIN);
   Utf8("{\"v\":1,\"seq\":5,\"prev\":\"no-es-hex\"}\n", b);
   FileWriteArray(h, b);
   FileClose(h);
   cadena = JournalAbrir(c);
   Comprobar(cadena == "rota", "rota: ultima linea fuera del formato, cadena rota", cadena);
   Comprobar(g_journal_seq == 0, "rota: la cadena nueva empieza en 0", JEntero(g_journal_seq));
   string motivo = "la cuenta NO es DEMO: \"el EA\" se quita\ty no hace nada\n" + ShortToString(1);
   E("2026.10.28 09:00:00", "2026.10.28 07:00:00", "arranque", ArranqueGolden(cadena, true));
   E("2026.10.28 09:00:00", "2026.10.28 07:00:00", "cuenta", CuentaGolden("ACCOUNT_TRADE_MODE_REAL"));
   E("2026.10.28 09:00:00", "2026.10.28 07:00:00", "negativa", DatosNegativa("ACCOUNT_TRADE_MODE_REAL", motivo));
   E("2026.10.28 09:00:01", "2026.10.28 07:00:01", "fin", DatosFin(REASON_REMOVE));
   JournalCerrar();
  }

//--- el resto ---------------------------------------------------------------------------------

void Negativa()
  {
   Comprobar(!NegarFueraDeDemo(ACCOUNT_TRADE_MODE_DEMO), "negativa: DEMO pasa");
   Comprobar(NegarFueraDeDemo(ACCOUNT_TRADE_MODE_CONTEST), "negativa: CONTEST se niega");
   Comprobar(NegarFueraDeDemo(ACCOUNT_TRADE_MODE_REAL), "negativa: REAL se niega");
  }

void CambioDeDiaInyectado()
  {
   Comprobar(CambioDeDia(T("2026.10.26 23:59:00"), T("2026.10.27 00:00:00")), "dia: 23:59 -> 00:00 cambia");
   Comprobar(!CambioDeDia(T("2026.10.26 00:00:00"), T("2026.10.26 23:59:59")), "dia: el mismo dia no cambia");
   Comprobar(CambioDeDia(T("2026.12.31 23:59:00"), T("2027.01.01 00:00:00")), "dia: cambio de anio");
   Comprobar(!CambioDeDia(0, T("2026.10.26 23:59:00")), "dia: sin dia anterior no cambia");
   Comprobar(DatosCambioDeDia(T("2026.10.26 23:59:00"), T("2026.10.27 00:00:00")) ==
             "{\"dia_anterior\":\"2026-10-26\",\"dia_nuevo\":\"2026-10-27\"}", "dia: los datos del cambio");
  }

void HashYTexto()
  {
   uchar b[];
   Utf8("abc", b);
   Comprobar(Sha256Hex(b) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", "sha256: abc");
   ArrayResize(b, 0);
   Comprobar(Sha256Hex(b) == "", "sha256: vacio falla y devuelve texto vacio");
   Comprobar(JTexto("a\"b\\c\n" + ShortToString(31) + ShortToString(127)) ==
             "\"a\\\"b\\\\c\\n\\u001f" + ShortToString(127) + "\"", "json: escapes");
  }

// Espera a estar conectado (como mucho un minuto) y unos segundos mas: antes de conectar, la
// cuenta se lee con ceros (EA-CONEXION.md 0.b).
void LecturaReal()
  {
   Resultado("LECTURA|conectado_al_empezar=" + JLogico(TerminalInfoInteger(TERMINAL_CONNECTED) != 0));
   uint t0 = GetTickCount();
   while(!TerminalInfoInteger(TERMINAL_CONNECTED) && GetTickCount() - t0 < 60000 && !IsStopped())
      Sleep(250);
   Sleep(3000);
   Resultado("LECTURA|conectado=" + JLogico(TerminalInfoInteger(TERMINAL_CONNECTED) != 0));
   Resultado("LECTURA|cuenta=" + LeerCuenta());
   Resultado("LECTURA|reloj=" + LeerReloj());
   Resultado("LECTURA|sesiones=" + LeerSesiones(_Symbol));
  }

void OnStart()
  {
   g_res = FileOpen("Botsito\\pruebas\\resultado.txt", FILE_WRITE | FILE_BIN);
   if(g_res == INVALID_HANDLE)
     {
      Print("BotsitoPruebasCapa: no se pudo abrir resultado.txt (error ", GetLastError(), ")");
      return;
     }
   Resultado("PRUEBAS|BotsitoPruebasCapa|build=" + JEntero(TerminalInfoInteger(TERMINAL_BUILD)));
   Negativa();
   CambioDeDiaInyectado();
   HashYTexto();
   Continua();
   Rota();
   LecturaReal();
   Resultado("RESUMEN|ok=" + JEntero(g_ok) + "|fallos=" + JEntero(g_fallos));
   FileClose(g_res);
  }
//+------------------------------------------------------------------+
