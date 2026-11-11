# План Shadow-тестирования крипто-режимов

Последнее обновление: 2026-07-13

Этот файл является постоянной памяткой по тому, что именно тестируется в
shadow, зачем это делается и при каких условиях вариант может перейти в paper.
Он не является торговой конфигурацией и сам по себе ничего не включает.

## Общие правила

- Shadow и counterfactual не размещают ордера и не меняют live-routing.
- Shadow не меняет `proposed_signals`, `signal_outcomes`, `final_r` и scoring.
- Результаты считаются в USD после комиссий/slippage; R используется как
  вспомогательная метрика, а не как округленные значения `+1R/+2R`.
- Для новых crypto intraday-тестов разрешены только forward-строки после
  активации `preentry_v2` с `data_quality=ok`.
- Backfill и старые строки с post-entry классификацией не являются доказательством
  эффективности.
- Asia/off-фильтр нельзя ослаблять ради увеличения выборки.
- Ни один вариант не переводится в paper автоматически. Нужны достаточная
  выборка, resolved-сделки, чистые данные, устойчивость по подгруппам и ручное
  решение оператора.

## Crypto swing

### Что сейчас в paper

Активный production-paper контроль сохраняет установленную native swing-геометрию:

- профиль: `production_legacy_native_targets`;
- версия: `crypto_swing_legacy_native_v1`;
- canonical target override выключен;
- T140 не заменяет текущую paper-логику.

То есть текущий paper swing используется как контрольная линия, с которой
сравниваются shadow-варианты на тех же сигналах, свечах, комиссиях и Model F
profit protection.

### Что тестируется в shadow

Основные варианты в `scripts/crypto_swing_entry_sweep.py`:

| Вариант | Смысл |
|---|---|
| `shadow_legacy_full_clean` | Контроль: текущая native swing-логика, только clean FULL-сделки |
| `shadow_t140_full_clean` | Targets `1.40 / 2.40 / 3.80 ATR`, clean FULL |
| `shadow_t130_full_clean` | Targets `1.30 / 2.30 / 3.60 ATR`, clean FULL |
| `shadow_t140_allow_half_size` | T140 для clean FULL и clean HALF; HALF считается с весом 0.5 |
| `shadow_t140_no_overlay_clean` | Counterfactual без влияния overlay action/cooldown, но с сохранением clean-data gate |

В sweep также есть более широкий диагностический набор зон, стопов, RR-гейтов
и score-гейтов. Он нужен для исследования, но не является списком кандидатов
для автоматического включения.

### Цель swing-теста

Проверить, улучшает ли T140 или T130 реальную net-PnL после costs относительно
текущего native paper-контроля, не ухудшая одновременно:

- winrate;
- максимальную просадку;
- частоту original stop;
- стабильность по символам, направлениям и рыночным режимам;
- качество исполнения и долю late/data-gap сделок.

`no_overlay` используется только для понимания, сколько edge теряется из-за
защитного overlay. Это не предложение отключить overlay в production.

### Правила решения по swing

- Нельзя выбирать T140 только по общей сумме PnL.
- Backfill может сформировать гипотезу, но не может подтвердить переход.
- Forward clean-сделки должны быть resolved и иметь корректную latency/coverage.
- T140/T130 должны сравниваться с тем же контролем и теми же costs.
- Даже хороший результат сначала переводится в отдельный paper-кандидат или
  ограниченный paper-контур, а не сразу в live.

## Crypto intraday

### Что сейчас в paper

Текущая paper-логика проходит через `preentry_v2` и `crypto_quality_overlay`.
Overlay проверяет regime BTC/ETH, score, RVOL, funding, spread, session,
cooldowns, exposure, derivatives и свежесть catalyst.

Entry-mode политика:

- `PULLBACK_LIMIT` — основной режим;
- `BREAKOUT_CONTINUATION` — только при strong confirmation, иначе HALF или shadow;
- `MOMENTUM_TAKER_NOW` — cautious, HALF_SIZE;
- `LIMIT_THEN_TAKER_TIMEOUT` — shadow-only и не является текущим paper-кандидатом;
- crypto scalp — отключён.

Asia/off остаётся защитным фильтром: обычные intraday-сделки там shadow-only;
исключения допускаются только при свежем catalyst или полном market confirmation
и не выше HALF_SIZE.

### Что тестируется в focused shadow-контуре

Контур запускается командой `crypto-intraday-idea-sweep` и после paper-shadow
refresh добавлен в routine schedule. Он записывает только собственные
read-model таблицы и отчёт `reports/CRYPTO_INTRADAY_IDEA_SWEEP.md`.

#### PULLBACK_LIMIT

Тестируется один параметр за раз:

- `current` — baseline;
- `shallow` — более мелкая pullback-зона;
- `deeper` — более глубокая pullback-зона;
- `level_hold_1bar` — после первого touch нужна одна полностью закрытая свеча,
  удерживающая уровень; симуляция начинается только со следующей свечи;
- `vwap_hold_1bar` — после touch нужна закрытая свеча, удерживающая session VWAP;
  при отсутствии volume вариант не считается валидным.

Комбинации этих изменений между собой не тестируются, чтобы не потерять
причинность результата.

#### BREAKOUT_CONTINUATION

Тестируется только вариант `strong_confirmation_only`.

- Strong confirmation должен быть зафиксирован в point-in-time snapshot на момент
  entry decision.
- Текущий market context задним числом не используется.
- Размер в эксперименте — HALF_SIZE.
- При отсутствии point-in-time подтверждения вариант получает статус
  `BLOCKED_STRONG_CONFIRMATION_EVIDENCE`, а не нулевой прибыльный результат.

#### MOMENTUM_TAKER_NOW

Тестируется только текущий контроль `current_half_size`.

- Новый набор параметров для momentum пока не подбирается.
- HALF_SIZE сохраняется до минимум 30 resolved forward-сделок.
- До этого момента результат имеет статус `INSUFFICIENT_FORWARD_SAMPLE` и не может
  служить основанием для усиления режима.

#### LIMIT_THEN_TAKER_TIMEOUT

В focused-тестах полностью отключён и только отображается как
`DISABLED_BY_TEST_PLAN`. Ни глубина зоны, ни timeout для него сейчас не
оптимизируются.

### Цель intraday-теста

Понять, можно ли улучшить качество входа и net-PnL через точечную настройку
PULLBACK, не ухудшая winrate, fill realism, costs и защиту капитала. Отдельно
проверяется, дают ли удержание уровня и VWAP полезный фильтр, а не просто
уменьшают количество сделок.

## Как читать статусы

- `INSUFFICIENT_FORWARD_SAMPLE` — данных недостаточно; вывод о прибыльности
  запрещён.
- `BLOCKED_STRONG_CONFIRMATION_EVIDENCE` — нет допустимого point-in-time
  подтверждения; это не отрицательный PnL-результат.
- `DISABLED_BY_TEST_PLAN` — режим намеренно не тестируется.
- `FORWARD_REVIEW_ELIGIBLE` — минимальная resolved-выборка набрана, но это ещё
  не promotion; нужны проверки устойчивости и ручное решение.
- `guard_excluded` / `production_asia_off_guard` — сделка исключена действующим
  защитным фильтром и не используется для ослабления этого фильтра.

## Минимальный порядок дальнейших действий

1. Набрать чистую forward-выборку после `preentry_v2`.
2. Сначала оценить PULLBACK baseline против shallow/deeper.
3. Затем отдельно оценить level hold и VWAP hold.
4. BREAKOUT анализировать только при накоплении point-in-time strong-confirmation.
5. MOMENTUM не усиливать до 30 resolved forward-сделок.
6. LIMIT_THEN_TAKER не возвращать в тестовый набор без отдельного решения.
7. Перед любым paper-переходом проверить net USD, winrate, PF, drawdown, costs,
   latency, coverage и подгруппы по session/regime/symbol.

## Источники истины в проекте

- `config/crypto_swing_paper_policy.yaml`
- `scripts/crypto_swing_entry_sweep.py`
- `config/crypto_quality_overlay.yaml`
- `src/execution/crypto_intraday_idea_sweep.py`
- `src/execution/paper_shadow_engine.py`
- `src/execution/profit_protection.py`
- `reports/CRYPTO_INTRADAY_IDEA_SWEEP.md`

## Отложенный вопрос по Shadow Mode — 2026-07-30

После проверки Paper вернуться к полному аудиту всех активных Shadow lanes:
проверить, что кандидаты и outcomes продолжают записываться, оценить свежую
forward-статистику по каждому варианту и определить, какие режимы или настройки
уже заслуживают ручного рассмотрения для перевода в Paper.
