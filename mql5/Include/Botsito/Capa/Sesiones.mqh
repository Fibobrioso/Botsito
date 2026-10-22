//+------------------------------------------------------------------+
//| Sesiones.mqh - las sesiones del simbolo (R6a.1, rama             |
//| trabajo/ea-conexion; condicion 2 de RENOVAR-CIERRES.md). Se leen |
//| y se registran; el veto es de R6a.5 (ADR-0068 4, ADR-0082 D6).   |
//|                                                                  |
//| SymbolInfoSessionTrade y SymbolInfoSessionQuote dan segundos     |
//| desde las 00:00 de un dia de la semana del servidor; el indice   |
//| sube hasta que la funcion devuelve false (error 4307,            |
//| ERR_MARKET_SESSION_INDEX). TOPE_SESIONES solo evita un bucle sin |
//| fin; es parte del formato v1 (mql5/JOURNAL.md).                  |
//+------------------------------------------------------------------+
#define TOPE_SESIONES 32

// La semana en JSON a partir de las siete listas ya escritas, de SUNDAY a SATURDAY: cada una es el
// contenido de la lista, p. ej. `[300,86100],[86160,86340]` o vacia.
string JsonSemana(const string &listas[])
  {
   string r = "{";
   for(int d = 0; d < 7; d++)
     {
      if(d > 0)
         r += ",";
      r += JPar(EnumToString((ENUM_DAY_OF_WEEK)d), "[" + listas[d] + "]");
     }
   return r + "}";
  }

// Las sesiones de negociacion (trade = true) o de cotizacion (false) de un simbolo.
string LeerSemana(const string simbolo, const bool trade, bool &tope)
  {
   string listas[7];
   for(int d = 0; d < 7; d++)
     {
      listas[d] = "";
      uint i = 0;
      for(; i < TOPE_SESIONES; i++)
        {
         datetime desde = 0, hasta = 0;
         bool ok = trade ? SymbolInfoSessionTrade(simbolo, (ENUM_DAY_OF_WEEK)d, i, desde, hasta)
                         : SymbolInfoSessionQuote(simbolo, (ENUM_DAY_OF_WEEK)d, i, desde, hasta);
         if(!ok)
            break;
         if(i > 0)
            listas[d] += ",";
         listas[d] += "[" + JEntero((long)desde) + "," + JEntero((long)hasta) + "]";
        }
      if(i == TOPE_SESIONES)
         tope = true;
     }
   return JsonSemana(listas);
  }

string DatosSesiones(const string trade, const string quote, const bool tope)
  {
   return "{" + JPar("trade", trade) + "," + JPar("quote", quote) + "," + JPar("tope_alcanzado", JLogico(tope)) + "}";
  }

string LeerSesiones(const string simbolo)
  {
   bool tope = false;
   string trade = LeerSemana(simbolo, true, tope);
   string quote = LeerSemana(simbolo, false, tope);
   return DatosSesiones(trade, quote, tope);
  }
//+------------------------------------------------------------------+
