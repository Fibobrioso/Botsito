//+------------------------------------------------------------------+
//| Cuenta.mqh - la negativa fuera de DEMO y la lectura de la cuenta |
//| (R6a.1, rama trabajo/ea-conexion, ADR-0082 D6).                  |
//|                                                                  |
//| Ni el login ni ninguna cifra de dinero (D2f).                    |
//+------------------------------------------------------------------+

// true = se niega. La condicion es la de tools/mql5/MedirDemoFTMO.mq5:759, con el modo como
// argumento (D2a). ACCOUNT_TRADE_MODE_DEMO vale 0, y antes de conectar una propiedad entera de la
// cuenta puede leerse 0 sin error (EA-CONEXION.md 0.b): por eso el EA la llama dos veces, lo primero
// de OnInit y otra vez al conectar (respuesta a la PARADA, punto 1).
bool NegarFueraDeDemo(const long modo)
  {
   if((ENUM_ACCOUNT_TRADE_MODE)modo != ACCOUNT_TRADE_MODE_DEMO)
      return true;
   return false;
  }

string DatosCuenta(const string trade_mode, const string margin_mode, const string servidor,
                   const bool conectado)
  {
   return "{" + JPar("trade_mode", JTexto(trade_mode)) + "," + JPar("margin_mode", JTexto(margin_mode)) +
          "," + JPar("servidor", JTexto(servidor)) + "," + JPar("conectado", JLogico(conectado)) + "}";
  }

// La cuenta tal como se lee ahora: los nombres de sus enum y el servidor.
string LeerCuenta()
  {
   return DatosCuenta(EnumToString((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE)),
                      EnumToString((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)),
                      AccountInfoString(ACCOUNT_SERVER), TerminalInfoInteger(TERMINAL_CONNECTED) != 0);
  }

string DatosNegativa(const string trade_mode, const string motivo)
  {
   return "{" + JPar("trade_mode", JTexto(trade_mode)) + "," + JPar("motivo", JTexto(motivo)) + "}";
  }
//+------------------------------------------------------------------+
