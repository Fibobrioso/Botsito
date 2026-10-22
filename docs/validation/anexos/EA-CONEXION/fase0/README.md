# Anexos de la fase 0 de `trabajo/ea-conexion` (2026-10-19)

Medido en la máquina de Aleks, con MetaTrader 5 build 6230 y la cuenta de prueba de FTMO de
octubre, desde el scratchpad de la sesión (fuera del repo). Lo cuenta `docs/validation/EA-CONEXION.md` §0.

## Guiones de medida (no son de la capa; ninguno llama a una función de trading)

- `MedirFase0.mq5`: reloj, cuenta, SHA-256, sesiones (trade y quote) y bytes por modo de apertura.
  Escribe en `MQL5\Files\Botsito_fase0\`. Su salida, versión 2 (espera a `TERMINAL_CONNECTED`):
  `medida.txt`.
- `MedirFase0b.mq5`: los enteros de `ENUM_ACCOUNT_TRADE_MODE`, `ENUM_ACCOUNT_MARGIN_MODE` e
  `INIT_*`, y la cuenta antes y después de conectar (del login solo si es distinto de cero). Salida:
  `medida_b.txt`.
- `TesterFase0.mq5`: un EA que no opera, para el Strategy Tester (`Model=4`): modo de la cuenta,
  sesiones, reloj y recuento de ticks. Salida: `tester.txt` (en `Terminal\Common\Files`).

Las salidas se copiaron byte a byte (UTF-8 sin BOM, LF, escritas en `FILE_BIN`). sha256:

```
2cdc769f1dbe6ceffccc1c0d820d9f199a8e0484cca006508bbe55226969330e  medida.txt
fc696494097ba75e0ea4f39a361b3319c11a78d09cc904530c8d01904199ee16  medida_b.txt
9dbd6449814386519d5b9b9ff8e1558c11948b7a174abab759c41eced082ddb6  tester.txt
```

Los ficheros de bytes de `MedirFase0.mq5` no se commitean (uno lleva CRLF, otro es UTF-16, y
`.gitattributes` los normalizaria); su volcado esta en el informe, §0.c. sha256 de los originales:

```
ef4b5d37d86a2e8e2fb2c60970ff059cf14e301a774baf8afa660d9bfb6df14e  bytes_txt_ansi.txt
d8b0a712bfd95afdcf74d886d615764e3c4cb289a20ba8b48070ece7bcdfbf18  bytes_txt_unicode.txt
6e5a76431e4d6af2c207bc4fa72e9bcee9441aaf4e4686f36858059ea1625219  bytes_bin_utf8.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  bytes_bin_trunca.txt
```

## Logs de compilacion

MetaEditor los escribe en UTF-16LE con BOM y CRLF; aqui van convertidos a UTF-8 sin BOM y LF, linea a
linea, sin cambiar el texto. sha256 del ORIGINAL:

```
ad1e618ee7644640b55234ae9c89b6592d7754fe3f54caf648c9b24c804fd83d  compilar-medirdemoftmo-ok.log   (copia de tools/mql5/MedirDemoFTMO.mq5; 0 errores, 0 avisos; salida 1)
8a9b14a85cd04b0df6340a698512d5f7dd234eaae3650bb7b60efdb6ed547cc2  compilar-error-provocado.log    (la copia con `int x = ;`; 1 error; salida 0)
b5435901f65773f2b92ddea996b6ba364f3d37ba37491e6ca8f30e79d9d21f03  compilar-sin-include.log        (EA minimo con #include <Botsito/...>, sin /include; 1 error; salida 0)
38073236aec628bb7d40bec9395bb18fea68060070f81c00c938894c550c4051  compilar-con-include.log        (el mismo con /include; 0 errores; salida 1)
```

Los logs del terminal y del agente del tester llevan el login y la IP de la conexion: no se copian.
