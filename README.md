# Botsito

Bot fiel a la estrategia de un trader concreto (EURUSD, H4 → M15 → M1), verificable caso a caso
contra sus decisiones y ejecutable en MetaTrader 5. Sin IA en ejecución.

## Cómo orientarse

1. `PROJECT_STATE.md` — memoria operativa: dónde estamos, qué funciona, qué viene.
2. `docs/plan/MASTER_PLAN.md` — plan de desarrollo: 35 funcionalidades en 8 fases, una rama por funcionalidad.
3. `docs/research/2026-09-03-del-corpus-al-bot.html` — investigación de método que justifica la arquitectura.

## Flujo de trabajo

`main` siempre estable. Cada funcionalidad se desarrolla en `feature/F##-nombre`, termina con un
`FUNCTIONALITY VALIDATION REPORT` y solo se integra tras validación explícita.

## Arranque

```
make sync    # uv sync --locked + instala los hooks de scripts/git-hooks
make check
```

Paquete Python: `botsito` (`src/botsito`). CLI: `uv run botsito --help`
(`state check`, `knowledge validate`, `config validate`, `corpus inventory|check`,
`evidence new|contradictions`, `feedback new|trace|pending`).
