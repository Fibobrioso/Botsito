# tests/fixtures/ohlc/ — dias reales de M1 EURUSD de Dukascopy (formato bi5, sin tocar)

Descargados el 2026-09-04 desde `datafeed.dukascopy.com` (BID, escala 100000). Cubren los cuatro
cambios de hora (UE: 2025-10-26 y 2026-03-29; EE. UU.: 2025-11-02 y 2026-03-08) con viernes,
domingo y lunes de cada semana, los domingos anteriores para el desplazamiento semanal, y el dia
del caso del trader (2026-07-02). Los tests los decodifican con `botsito.data.dukascopy`.

| Fichero | bytes | sha256 |
|---|---|---|
| EURUSD_2025-10-19.bi5 | 3171 | cc346013a29521203f9db602b0f9c8bbabc67bc50c86610e8bfb9c488498956e |
| EURUSD_2025-10-24.bi5 | 10028 | c176d1386d078a7584b0fbe1b135249ac6e116e75f25166e824f062bf72ddbc3 |
| EURUSD_2025-10-26.bi5 | 3185 | 52910847d6be8b791f5b9cf25c75ada714cc3a9842420cc49378353d4b065a40 |
| EURUSD_2025-10-27.bi5 | 10894 | bf4c2bde1734244b6d2419eb5331aff5695d7b058c7291294f1e649f5a402096 |
| EURUSD_2025-10-31.bi5 | 10123 | 6c5f25374446d57b75fabc3907217e68f692e83b14e09162f4ea97257ad4d2e8 |
| EURUSD_2025-11-02.bi5 | 2885 | 3ed8ec77fe929f1cb06a71a8fdd1021834e9c92fd842d4f007a5d62f3db9cfc5 |
| EURUSD_2025-11-03.bi5 | 11115 | 4b9c5eaeaa98e1747a3f9f7f04929c5afc0b853eae2de48af112fae927036a28 |
| EURUSD_2026-03-01.bi5 | 2890 | 30ea6796fbec3dc8920bb6a23e4ea4560d1721815afa031c36e60e3579129916 |
| EURUSD_2026-03-06.bi5 | 10757 | b4dc6e020b58c7f65673e7a866fca382cc222ec674e36f4927b7e63e36fa4b12 |
| EURUSD_2026-03-08.bi5 | 3277 | bc144703f7c719d2e7272f0aaf9c1b2584be62249d3b90a2dacb5105c033d603 |
| EURUSD_2026-03-09.bi5 | 12022 | 7471a7edcfaae6259a3da67d2438117369c036d73d1308995c9d71725cad2118 |
| EURUSD_2026-03-22.bi5 | 3116 | b1d5c628a7da030c2c82fd822cbdef8d235aa8bd997583318fb90f5760a9f214 |
| EURUSD_2026-03-27.bi5 | 10002 | 9741625c10de1cb6106af1a66ec8472b3b7432c08fb10b4ac27d553dacf51e0c |
| EURUSD_2026-03-29.bi5 | 3053 | 0c01c167344fbf29401c14f3af2ec69a17df4fcdaec93b82ce7632d68948e691 |
| EURUSD_2026-03-30.bi5 | 10547 | 5828a3948cc05439e19c05fb9b223a67e45f560bbff588ee45264b5f05f15010 |
| EURUSD_2026-07-02.bi5 | 11003 | d2cfc67304205577aa5e236e60f81ca097f00d93014d99c0ff982ece07ad1050 |
