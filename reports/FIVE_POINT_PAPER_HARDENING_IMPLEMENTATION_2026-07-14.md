# Five-Point Paper Hardening Implementation Report

Дата: 2026-07-14.

## Итог

Реализованы все пять пунктов из аудита:

1. исправлен stale cache рыночного контекста акций;
2. добавлен постоянный audit trail portfolio guard;
3. macro-agent переведен на свежие canonical macro/geopolitical events;
4. сохранены и закреплены текущие CQO/risk/session/sector/scalp safety policies;
5. сокращена entry-detection latency для crypto и stocks без ослабления freshness gate.

Live, auto-live и manual-live не включались. Изменения относятся к paper, monitoring,
read-model/news context и operational audit.

## 1. Stocks market-context cache

### Было

`intraday_gate_context.market_context()` кешировал SPY/QQQ по `(date, hour)`. Если в первые минуты
сессии было недостаточно 15m-свечей, `unknown` сохранялся до конца часа даже после появления свежих
benchmark bars. Это искусственно демоутило новые stock ideas A/B -> C.

### Стало

- cache key теперь содержит UTC minute;
- кандидаты одного scoring batch продолжают использовать общий read;
- следующая минута перечитывает SPY/QQQ и видит новую свечу;
- cache ограничен 180 записями;
- per-symbol freshness и fail-conservative `unknown/stale` не ослаблены.

Runtime-проверка после исправления: обе ноги SPY/QQQ свежие, `status=ok`, regime `trend_up`.

## 2. Portfolio guard audit и исправление состава book

Создана append-only таблица `portfolio_guard_audit`. Для каждого registry batch сохраняются:

- `ALLOW / BLOCK / FAIL_OPEN`;
- timestamp, report id и asset classes;
- candidate count и skipped candidate count;
- combined/crypto/stocks R;
- resolved sample;
- lookback и pause threshold;
- reason, guard version и полный context JSON.

Добавлена CLI-команда:

```powershell
python -m src.cli portfolio-guard-audit --limit 20
```

### Критическая находка при runtime-проверке

Первая audit-запись показала `BLOCK -9.08R`. Разбор обнаружил, что старая `_load_rows()` включала
в combined book все Model F outcomes: C-tier stocks, shadow sector-cap, disabled scalp и
`shadow_risk_guard`. Это не production paper book.

Исправлено:

- используется authoritative `paper_actionability.resolve_paper_actionability()`;
- C-tier/scalp/shadow/late/non-actionable получают 0x и не входят в guard;
- `HALF_SIZE` учитывается как 0.5x R;
- guard version повышена до `portfolio_guard_v3_actionable_sized_r`.

После исправления текущий state: `ALLOW`, 2 resolved actionable trades, `+0.25R`; выборка меньше
минимальных 6, поэтому общий kill-switch не активируется. Ошибочная старая запись сохранена как
историческая v2-запись, новая корректная запись явно помечена v3.

## 3. Macro/geopolitical context

### Было

Macro agent читал только `news_output.top_news` (фактически до 15 generic importance-ranked rows).
Поэтому свежий Iran/Hormuz cluster мог уже находиться в БД, но проигрывать product/company news.
Raw substring matching также считал `war` внутри `Warsh` и мог путать корпоративную метафору
`declares war on buybacks` с геополитикой.

### Стало

- агент независимо читает свежие primary rows из `news_canonical_events`;
- учитывает только последние 12 часов и не берет expired events;
- приоритет: recency, geopolitical/macro event type, source quality, confidence, corroboration;
- generic `top_news` остается fallback;
- differently-worded relays дедуплицируются по semantic family/hour, сохраняется лучшая source version;
- social relay flood ограничен и не может самостоятельно создать высокий risk score;
- keyword matching boundary-safe (`Warsh` больше не `war`);
- `inflation cools/falls/below expectations`, `lowest CPI` и `soft inflation` классифицируются как disinflation, а не risk-off;
- corporate war metaphors, `War College` и рекламный corporate `Oil Day` исключены;
- taxonomy расширена для `airstrike`, `missile`, `blockade`, `Strait of Hormuz`,
  `military strike`, `retaliation`.

Production canonical refresh обработал 1487 свежих news rows. После удаления доказанных corporate false positives
runtime macro output показывает `risk_score=81.5`, `btc_bias=risk-off headwind`; высокий риск поддержан свежими
Iran/Hormuz, attack и sanctions events, а не совпадениями в названиях.
Это advisory context: новый глобальный headline-only hard block не добавлялся.

## 4. Сохраненные safety policies

Конфигурационные и behavioral tests закрепляют:

- CQO enabled для paper и live disabled;
- circuit-breaker paper floor активен;
- crypto scalp остается disabled/shadow-only;
- Asia 00-06 UTC продолжает демоутить crypto scalp/intraday;
- disabled crypto `PULLBACK_LIMIT` / `LIMIT_THEN_TAKER_TIMEOUT` entry modes не промоутятся;
- disabled stocks taker modes не промоутятся;
- freshness cutoffs остались прежними: crypto intraday 15m и stocks intraday 45m hard boundary.

Ни score thresholds, ни TP/SL, ни sizing policy, ни late-shadow actionability не ослаблялись.

## 5. Latency

### Crypto

- fast pending-monitor cadence: 45s -> 30s;
- existing writer mutex, leader election, idempotent alerts и freshness checks сохранены;
- full crypto monitor остается отдельным контуром.

### Stocks

До исправления `stocks-monitor-session` раз в 10 минут перестраивал report, но не вызывал
`track_pending_entries()` для stocks. Реальный fast entry lane отсутствовал.

Теперь:

- lightweight stocks A/B intraday tracker запускается каждую минуту;
- на каждом тике обновляются только pending symbols и только 15m OHLCV;
- pending refresh и tracker выполняются до тяжелого full report, поэтому provider/agent latency не блокирует fast lane;
- full universe/scoring report остается раз в 10 минут;
- tracker scope жестко ограничен `asset_class=stocks`, `modes={intraday}`;
- используется тот же writer mutex, paper-entry notifier, dedup, actionability и risk floors;
- dry-run не запускает outcome/status tracker;
- monitor duration увеличена до 180 минут: это покрывает 2h паузу после завершения цикла и до 60 минут
  работы следующего тяжелого прохода; следующий цикл заменяет предыдущий процесс по scoped PID-lock.

## Проверки

- `py_compile` всех измененных Python-модулей: OK.
- Целевые тесты после основных изменений: 196 passed.
- Финальный полный suite после всех правок: **1550 passed, 0 failed**.
- После финальной scheduler/latency/macro очистки: 139 релевантных tests passed.
- Scheduler dry-run: 66 steps, все CLI surfaces valid, LLM auto-invoke check OK.
- Canonical news refresh: 1487 rows, 1380 clusters updated.
- Portfolio guard CLI и реальная DB audit write: OK.
- Runtime stock market context: fresh/ok.
- Runtime macro context: fresh Iran/Hormuz event selected, risk warning present.

## Production activation

Default scheduler перезапущен после финальных изменений в единственном экземпляре. Команда:

```powershell
python -m scripts.run_default_market_schedule --hours 24 --interval-hours 2 --monitor-minutes 90 --send-telegram
```

Scheduler работает под существующим `scripts/autostart_scheduler.bat`, который автоматически
перезапускает завершившийся процесс. После удаления ручного дубликата остался ровно один scheduler:
PID `12544` на момент финальной проверки. Его cycle plan создает crypto pending monitor с 30s cadence и
stocks monitor с 1m pending / 10m full-report cadence на 180 минут.

## Ожидаемый эффект

- меньше ложных C-tier по акциям в первый час сессии;
- отсутствие ложного portfolio kill-switch от shadow/disabled outcomes;
- полностью восстанавливаемая история причин реального guard block/allow;
- актуальная геополитика попадает в macro context раньше generic news;
- crypto entry detection target сокращен до 30s polling floor;
- stocks pending entries проверяются примерно каждую минуту вместо зависимости от 10m report или
  двухчасового full tracker;
- запоздалые сигналы по-прежнему уходят в late-shadow, поэтому ускорение не превращается в chase.
