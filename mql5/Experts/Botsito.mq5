//+------------------------------------------------------------------+
//| Botsito.mq5 - el EA de la capa de MT5 que nunca decide una       |
//| operacion (ADR-0082). R6a.1, rama trabajo/ea-conexion:           |
//| se niega fuera de DEMO, lee el reloj del servidor, la cuenta y   |
//| las sesiones del simbolo del grafico, y lo escribe en el journal |
//| (mql5/JOURNAL.md). Desde R6a.2 (trabajo/capa-generada, 1.1), el  |
//| journal es v2 y cada linea lleva el CAPA_HASH de Generado.mqh.   |
//|                                                                  |
//| NUNCA envia, modifica ni cancela una orden ni cierra una         |
//| posicion: no llama a ninguna funcion de trading                  |
//| (tests/contract/test_capa_mt5.py). Ni login ni dinero en el      |
//| journal. Ninguna cifra de firma, broker, instrumento ni          |
//| ejecucion a mano: llegan generadas en Generado.mqh (ADR-0082 D5).|
//+------------------------------------------------------------------+
#property copyright "Bot v3"
#property version   "1.10"
#property description "Capa de MT5 (R6a.2): conexion, reloj del servidor, sesiones del simbolo y journal v2 con el capa_hash. No opera."

#define VERSION_EA "1.1"
#define LATIDO_SEG 60

#include <Botsito/Capa/Generado.mqh>
#include <Botsito/Capa/Journal.mqh>
#include <Botsito/Capa/Cuenta.mqh>
#include <Botsito/Capa/Reloj.mqh>
#include <Botsito/Capa/Sesiones.mqh>

datetime g_ultimo_srv = 0;
bool     g_cuenta_leida = false;

// Al conectar (la primera vez tras arrancar): la negativa otra vez, con el modo leido conectado, y
// la cuenta, el reloj y las sesiones. Antes de conectar, las propiedades de la cuenta pueden leerse
// 0 sin error, y 0 es DEMO (EA-CONEXION.md 0.b).
void AlConectar()
  {
   if(g_cuenta_leida || !TerminalInfoInteger(TERMINAL_CONNECTED))
      return;
   g_cuenta_leida = true;
   datetime srv = TimeTradeServer();
   datetime gmt = TimeGMT();
   JournalEscribir(srv, gmt, "cuenta", LeerCuenta());
   if(NegarFueraDeDemo(AccountInfoInteger(ACCOUNT_TRADE_MODE)))
     {
      JournalEscribir(srv, gmt, "negativa",
                      DatosNegativa(EnumToString((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE)),
                                    "la cuenta NO es DEMO al conectar: el EA se quita"));
      Print("Botsito: la cuenta NO es DEMO: el EA se quita");
      ExpertRemove();
      return;
     }
   JournalEscribir(srv, gmt, "reloj", LeerReloj());
   JournalEscribir(srv, gmt, "sesiones", LeerSesiones(_Symbol));
  }

int OnInit()
  {
   if(NegarFueraDeDemo(AccountInfoInteger(ACCOUNT_TRADE_MODE)))
     {
      Print("Botsito: la cuenta NO es DEMO: el EA no hace nada");
      return(INIT_FAILED);
     }
   // Al cambiar el simbolo o el marco del grafico el EA no se recarga: OnDeinit y OnInit, pero «values
   // of global variables and static variables are not reset» (docs/runtime/running). Cada global del
   // EA se pone aqui a su valor inicial; las del journal, en JournalAbrir. Medido en la demo del
   // 2026-10-20: sin esto, el arranque tras un cambio de simbolo no leia cuenta, reloj ni sesiones.
   g_cuenta_leida = false;
   g_ultimo_srv = 0;
   string cadena = JournalAbrir("Botsito", CAPA_HASH);
   datetime srv = TimeTradeServer();
   JournalEscribir(srv, TimeGMT(), "arranque",
                   DatosArranque(VERSION_EA, TerminalInfoInteger(TERMINAL_BUILD), _Symbol,
                                 TerminalInfoInteger(TERMINAL_CONNECTED) != 0, cadena));
   g_ultimo_srv = srv;
   EventSetTimer(LATIDO_SEG);
   AlConectar();
   return(INIT_SUCCEEDED);
  }

void OnTimer()
  {
   datetime srv = TimeTradeServer();
   datetime gmt = TimeGMT();
   if(CambioDeDia(g_ultimo_srv, srv))
     {
      JournalEscribir(srv, gmt, "cambio_de_dia", DatosCambioDeDia(g_ultimo_srv, srv));
      JournalEscribir(srv, gmt, "sesiones", LeerSesiones(_Symbol));
     }
   g_ultimo_srv = srv;
   JournalEscribir(srv, gmt, "latido", DatosLatido(TerminalInfoInteger(TERMINAL_CONNECTED) != 0, TimeCurrent()));
   AlConectar();
  }

void OnTick()
  {
   AlConectar();
  }

void OnDeinit(const int reason)
  {
   EventKillTimer();
   JournalEscribir(TimeTradeServer(), TimeGMT(), "fin", DatosFin(reason));
   JournalCerrar();
  }
//+------------------------------------------------------------------+
