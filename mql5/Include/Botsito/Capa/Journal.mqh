//+------------------------------------------------------------------+
//| Journal.mqh - el escritor del journal v1 de la capa de MT5       |
//| (R6a.1, rama trabajo/ea-conexion, ADR-0082 D7).                  |
//|                                                                  |
//| El formato esta en mql5/JOURNAL.md y lo valida                   |
//| src/botsito/mql5bridge/journal.py sobre los mismos bytes: JSON   |
//| canonico, UTF-8 sin BOM, LF, h(n) = SHA-256 de la linea sin LF y |
//| prev en la siguiente. Se escribe en modo binario: en modo texto  |
//| MT5 pone CRLF (medido, EA-CONEXION.md 0.c).                      |
//+------------------------------------------------------------------+
#define JOURNAL_VERSION 1

string g_journal_carpeta = "";
int    g_journal_h       = INVALID_HANDLE;
string g_journal_dia     = "";
long   g_journal_seq     = 0;
string g_journal_prev    = "";
bool   g_journal_abierto = false;

//--- textos JSON ---------------------------------------------------

// Un texto JSON con el escape de json.dumps(..., ensure_ascii=False).
string JTexto(const string s)
  {
   string r = "\"";
   int n = StringLen(s);
   for(int i = 0; i < n; i++)
     {
      ushort c = StringGetCharacter(s, i);
      if(c == '"')
         r += "\\\"";
      else if(c == '\\')
         r += "\\\\";
      else if(c == '\n')
         r += "\\n";
      else if(c == '\r')
         r += "\\r";
      else if(c == '\t')
         r += "\\t";
      else if(c == 8)
         r += "\\b";
      else if(c == 12)
         r += "\\f";
      else if(c < 32)
         r += StringFormat("\\u%04x", c);
      else
         r += ShortToString(c);
     }
   return r + "\"";
  }

string JLogico(const bool b)
  {
   return b ? "true" : "false";
  }

string JEntero(const long x)
  {
   return IntegerToString(x);
  }

// Un par clave:valor; el valor ya en JSON.
string JPar(const string clave, const string valor)
  {
   return JTexto(clave) + ":" + valor;
  }

// "AAAA-MM-DDTHH:MM:SS", sin huso.
string Iso(const datetime t)
  {
   MqlDateTime s;
   TimeToStruct(t, s);
   return StringFormat("%04d-%02d-%02dT%02d:%02d:%02d", s.year, s.mon, s.day, s.hour, s.min, s.sec);
  }

// "AAAA-MM-DD"
string Dia(const datetime t)
  {
   MqlDateTime s;
   TimeToStruct(t, s);
   return StringFormat("%04d-%02d-%02d", s.year, s.mon, s.day);
  }

//--- bytes y hash ---------------------------------------------------

// Los bytes UTF-8 de un texto, sin el 0 final que copia StringToCharArray.
void Utf8(const string s, uchar &b[])
  {
   int n = StringToCharArray(s, b, 0, -1, CP_UTF8);
   if(n > 0 && b[n - 1] == 0)
      ArrayResize(b, n - 1);
  }

// SHA-256 en hexadecimal en minusculas; "" si CryptEncode falla (con un array vacio falla: 0.c).
string Sha256Hex(const uchar &datos[])
  {
   uchar clave[], h[];
   if(CryptEncode(CRYPT_HASH_SHA256, datos, clave, h) != 32)
      return "";
   string r = "";
   for(int i = 0; i < 32; i++)
      r += StringFormat("%02x", h[i]);
   return r;
  }

string Genesis()
  {
   string r = "";
   for(int i = 0; i < 64; i++)
      r += "0";
   return r;
  }

//--- la linea --------------------------------------------------------

string JournalLinea(const long seq, const datetime srv, const datetime gmt, const string ev,
                    const string datos, const string prev)
  {
   return "{" + JPar("v", JEntero(JOURNAL_VERSION)) + "," + JPar("seq", JEntero(seq)) + "," +
          JPar("srv", JTexto(Iso(srv))) + "," + JPar("gmt", JTexto(Iso(gmt))) + "," +
          JPar("desfase_s", JEntero((long)(srv - gmt))) + "," + JPar("ev", JTexto(ev)) + "," +
          JPar("datos", datos) + "," + JPar("regla", "null") + "," + JPar("condicion", "null") + "," +
          JPar("capa_hash", "null") + "," + JPar("spec_hash", "null") + "," +
          JPar("risk_hash", "null") + "," + JPar("ambiguas", "null") + "," +
          JPar("prev", JTexto(prev)) + "}";
  }

string JournalFichero(const string carpeta, const string dia)
  {
   string d = dia;
   StringReplace(d, "-", "");
   return carpeta + "\\journal_" + d + ".jsonl";
  }

//--- la ultima linea del journal anterior -----------------------------

bool EsHex64(const string s)
  {
   if(StringLen(s) != 64)
      return false;
   for(int i = 0; i < 64; i++)
     {
      ushort c = StringGetCharacter(s, i);
      if(!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f')))
         return false;
     }
   return true;
  }

// Valida la ultima linea de un journal (JOURNAL.md, «Los ficheros»): acaba en LF, empieza por
// {"v":1,"seq":<n>, y acaba en "prev":"<64 hex>"}. Devuelve su seq y su hash.
bool UltimaLinea(const uchar &todo[], long &seq, string &hash)
  {
   int n = ArraySize(todo);
   if(n < 2 || todo[n - 1] != '\n')
      return false;
   int a = n - 2;
   while(a >= 0 && todo[a] != '\n')
      a--;
   uchar linea[];
   ArrayCopy(linea, todo, 0, a + 1, n - 2 - a);
   string s = CharArrayToString(linea, 0, WHOLE_ARRAY, CP_UTF8);
   string cabeza = "{\"v\":" + JEntero(JOURNAL_VERSION) + ",\"seq\":";
   string cola_prev = ",\"prev\":\"";
   if(StringFind(s, cabeza) != 0)
      return false;
   int coma = StringFind(s, ",", StringLen(cabeza));
   if(coma < 0)
      return false;
   string num = StringSubstr(s, StringLen(cabeza), coma - StringLen(cabeza));
   if(StringLen(num) == 0 || IntegerToString(StringToInteger(num)) != num)
      return false;
   int largo = StringLen(s);
   int p = largo - 66 - StringLen(cola_prev);
   if(p < 0 || StringSubstr(s, p, StringLen(cola_prev)) != cola_prev ||
      StringSubstr(s, largo - 2) != "\"}" || !EsHex64(StringSubstr(s, largo - 66, 64)))
      return false;
   seq = StringToInteger(num);
   hash = Sha256Hex(linea);
   return StringLen(hash) == 64;
  }

//--- abrir, escribir, cerrar -------------------------------------------

// Al arrancar: busca el journal mas reciente de la carpeta y sigue su cadena. Devuelve
// "ninguna", "sigue" o "rota" (cadena_anterior del arranque).
string JournalAbrir(const string carpeta)
  {
   g_journal_carpeta = carpeta;
   g_journal_h = INVALID_HANDLE;
   g_journal_dia = "";
   g_journal_seq = 0;
   g_journal_prev = Genesis();
   g_journal_abierto = true;
   string nombre = "", ultimo = "";
   long busca = FileFindFirst(carpeta + "\\journal_*.jsonl", nombre);
   if(busca != INVALID_HANDLE)
     {
      do
        {
         if(nombre > ultimo)
            ultimo = nombre;
        }
      while(FileFindNext(busca, nombre));
      FileFindClose(busca);
     }
   if(ultimo == "")
      return "ninguna";
   int h = FileOpen(carpeta + "\\" + ultimo, FILE_READ | FILE_BIN | FILE_SHARE_READ | FILE_SHARE_WRITE);
   if(h == INVALID_HANDLE)
      return "rota";
   uchar todo[];
   ulong tam = FileSize(h);
   if(tam > 0)
      FileReadArray(h, todo, 0, (int)tam);
   FileClose(h);
   long seq = 0;
   string hash = "";
   if(!UltimaLinea(todo, seq, hash))
      return "rota";
   g_journal_seq = seq;
   g_journal_prev = hash;
   return "sigue";
  }

bool JournalEscribir(const datetime srv, const datetime gmt, const string ev, const string datos)
  {
   if(!g_journal_abierto)
      return false;
   string dia = Dia(srv);
   if(dia != g_journal_dia)
     {
      if(g_journal_h != INVALID_HANDLE)
         FileClose(g_journal_h);
      g_journal_h = FileOpen(JournalFichero(g_journal_carpeta, dia),
                             FILE_READ | FILE_WRITE | FILE_BIN | FILE_SHARE_READ);
      if(g_journal_h == INVALID_HANDLE)
        {
         Print("Botsito: no se pudo abrir el journal de ", dia, " (error ", GetLastError(), ")");
         g_journal_dia = "";
         return false;
        }
      FileSeek(g_journal_h, 0, SEEK_END);
      g_journal_dia = dia;
     }
   uchar b[];
   Utf8(JournalLinea(g_journal_seq + 1, srv, gmt, ev, datos, g_journal_prev), b);
   string h = Sha256Hex(b);
   int n = ArraySize(b);
   ArrayResize(b, n + 1);
   b[n] = '\n';
   if(StringLen(h) != 64 || FileWriteArray(g_journal_h, b) != (uint)(n + 1))
     {
      Print("Botsito: no se pudo escribir en el journal (error ", GetLastError(), ")");
      return false;
     }
   FileFlush(g_journal_h);
   g_journal_seq++;
   g_journal_prev = h;
   return true;
  }

void JournalCerrar()
  {
   if(g_journal_h != INVALID_HANDLE)
      FileClose(g_journal_h);
   g_journal_h = INVALID_HANDLE;
   g_journal_dia = "";
   g_journal_abierto = false;
  }
//+------------------------------------------------------------------+
