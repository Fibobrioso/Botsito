//+------------------------------------------------------------------+
//| Reloj.mqh - el reloj del servidor y el cambio de dia             |
//| (R6a.1, rama trabajo/ea-conexion). Lee, no decide A-28 (D6).     |
//|                                                                  |
//| Las lecturas son las del paso 2 de tools/mql5/MedirDemoFTMO.mq5  |
//| (MedirReloj, :386-399). TimeGMT sale del reloj del ordenador,    |
//| que tiene que estar en hora.                                     |
//+------------------------------------------------------------------+

// true si el dia de `ahora` no es el de `antes`. `antes` = 0: todavia no hay dia anterior.
bool CambioDeDia(const datetime antes, const datetime ahora)
  {
   if(antes == 0)
      return false;
   return Dia(antes) != Dia(ahora);
  }

string DatosCambioDeDia(const datetime antes, const datetime ahora)
  {
   return "{" + JPar("dia_anterior", JTexto(Dia(antes))) + "," + JPar("dia_nuevo", JTexto(Dia(ahora))) + "}";
  }

string DatosReloj(const datetime current, const datetime servidor, const datetime gmt,
                  const datetime local, const long offset_seg, const long verano_seg)
  {
   return "{" + JPar("time_current", JTexto(Iso(current))) + "," +
          JPar("time_trade_server", JTexto(Iso(servidor))) + "," + JPar("time_gmt", JTexto(Iso(gmt))) + "," +
          JPar("time_local", JTexto(Iso(local))) + "," +
          JPar("desfase_servidor_gmt_min", JEntero((long)((servidor - gmt) / 60))) + "," +
          JPar("desfase_local_gmt_min", JEntero(-offset_seg / 60)) + "," +
          JPar("time_gmt_offset_seg", JEntero(offset_seg)) + "," +
          JPar("horario_verano_local_seg", JEntero(verano_seg)) + "}";
  }

// Las siete lecturas de MedirReloj, mas TimeGMTOffset, de donde sale el desfase local - GMT.
string LeerReloj()
  {
   datetime servidor = TimeTradeServer();
   datetime gmt = TimeGMT();
   return DatosReloj(TimeCurrent(), servidor, gmt, TimeLocal(), TimeGMTOffset(), TimeDaylightSavings());
  }

string DatosLatido(const bool conectado, const datetime current)
  {
   return "{" + JPar("conectado", JLogico(conectado)) + "," + JPar("time_current", JTexto(Iso(current))) + "}";
  }

// El nombre de la constante del motivo de OnDeinit.
string TextoMotivo(const int motivo)
  {
   switch(motivo)
     {
      case REASON_PROGRAM:     return "REASON_PROGRAM";
      case REASON_REMOVE:      return "REASON_REMOVE";
      case REASON_RECOMPILE:   return "REASON_RECOMPILE";
      case REASON_CHARTCHANGE: return "REASON_CHARTCHANGE";
      case REASON_CHARTCLOSE:  return "REASON_CHARTCLOSE";
      case REASON_PARAMETERS:  return "REASON_PARAMETERS";
      case REASON_ACCOUNT:     return "REASON_ACCOUNT";
      case REASON_TEMPLATE:    return "REASON_TEMPLATE";
      case REASON_INITFAILED:  return "REASON_INITFAILED";
      case REASON_CLOSE:       return "REASON_CLOSE";
     }
   return "OTRO";
  }

string DatosFin(const int motivo)
  {
   return "{" + JPar("motivo", JEntero(motivo)) + "," + JPar("motivo_texto", JTexto(TextoMotivo(motivo))) + "}";
  }

string DatosArranque(const string version_ea, const long build, const string simbolo, const bool conectado,
                     const string cadena_anterior)
  {
   return "{" + JPar("version_ea", JTexto(version_ea)) + "," + JPar("build", JEntero(build)) + "," +
          JPar("simbolo", JTexto(simbolo)) + "," + JPar("conectado", JLogico(conectado)) + "," +
          JPar("cadena_anterior", JTexto(cadena_anterior)) + "}";
  }
//+------------------------------------------------------------------+
