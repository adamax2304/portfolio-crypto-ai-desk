# Paper Trade Frequency and Iran Risk Audit

Дата среза: 2026-07-14, около 14:15 UTC.

## Короткий вывод

Сделок действительно стало существенно меньше. Для crypto это в первую очередь не поломка и не один слишком жесткий guard: за последние 7 дней сам поток кандидатов упал примерно на 65% относительно предыдущих 7 дней. После сильного бычьего импульса 2-7 июля рынок перешел в смешанный/chop режим, поэтому базовая стратегия стала находить намного меньше валидных сетапов.

Дополнительные фильтры также сократили торговлю, но на текущей выборке в основном сделали это полезно: crypto quality overlay, отключенный scalp, risk guard и stocks sector cap вместе отсеяли отрицательные когорты. Исключение -- late-shadow: там были пропущенные победители, но их нельзя честно считать доступными сделками, потому что сигнал уже опоздал.

Обострение конфликта с Ираном попадает в news layer как geopolitical risk, но сейчас **не является глобальным автоматическим блокиратором paper-сделок**. Текущее снижение частоты объясняется главным образом сменой рыночного режима, снижением числа A/B-кандидатов и точечными защитами после серии стопов. При этом в блоке акций обнаружена техническая причина искусственного недобора: stale cache market context в первый час американской сессии.

## Методика

- Реальной paper-сделкой считается только `signal_alerts.alert_type='paper_entry'` с `telegram_status='sent'`.
- `shadow_only`, `shadow_crypto_quality`, `shadow_risk_guard`, `shadow_sector_cap`, `late_shadow` и другие shadow-статусы не включены в paper P&L.
- USD P&L взят из `paper_portfolio_ledger` по активному профилю `bybit_non_vip_usdt_perp`.
- Для незакрытых/еще не записанных в ledger сделок P&L не придумывается.
- Сравнение shadow использует фактические outcomes, а не сигнал в момент создания.

## Частота сделок

### Последние 7 дней против предыдущих 7

| Актив | Метрика | Последние 7 дней | Предыдущие 7 дней | Изменение |
|---|---:|---:|---:|---:|
| Crypto | Все proposed candidates | 150 | 424 | -65% |
| Crypto | Реально отправленные paper entries | 68 | 183 | -63% |
| Stocks | Все proposed candidates | 217 | 236 | -8% |
| Stocks | A/B candidates | 10 | 28 | -64% |
| Stocks | Реально отправленные paper entries | 2 | 2 | без изменения |

За последние 48 часов crypto дала 22 A/B-кандидата и только 6 реальных paper entries против 41 кандидата и 29 entries в предыдущие 48 часов. Это падение entries примерно на 79%, но почти половина снижения начинается еще до guard-слоя: базовая генерация сигналов сократилась на 46%.

### По дням

2-7 июля система создавала много преимущественно long crypto-сигналов на сильном бычьем импульсе. Начиная с 8 июля число сигналов резко сократилось, направления стали смешанными, а режимы чаще определялись как range/chop/weak. 13 июля crypto не отправила ни одной paper-сделки: два кандидата были переведены в `shadow_risk_guard`. 14 июля к моменту среза отправлены SXT intraday и TAO swing.

Это выглядит как естественная адаптация к ухудшившемуся режиму, а не как остановка scheduler: pipeline продолжает создавать отчеты, кандидаты и monitor-записи вплоть до текущего дня.

## Paper P&L

| Окно | Crypto intraday | Crypto swing | Stocks intraday | Итого net |
|---|---:|---:|---:|---:|
| Последние 24ч | 1 alert, еще без ledger close | +$25.45 | +$79.86 | +$105.31 по закрытым |
| Последние 48ч | 5 alerts, 4 closed, -$23.72 | 1 closed, +$25.45 | 1 closed, +$79.86 | +$81.59 |
| Последние 72ч | 8 alerts, 7 closed, +$208.09 | 1 closed, +$25.45 | 1 closed, +$79.86 | +$313.40 |
| Последние 7 дней | 34 alerts, 26 closed, +$93.40 | 34 alerts, 32 closed, +$217.00 | 2 closed, +$89.13 | +$399.53 |
| Предыдущие 7 дней | 101 alerts, 40 closed, +$347.31 | 82 alerts, 75 closed, +$325.62 | 2 closed, -$2.04 | +$670.89 |

Абсолютная прибыль снизилась вместе с количеством сделок, но последние 7 дней остаются прибыльными после fees, slippage и funding. Это не доказательство стабильного edge: выборка короткая, часть свежих сделок еще не закрыта, а прибыль концентрировалась в импульсе 11 июля.

### Последние сделки

- `TAO`, crypto swing short, 14 июля: +0.5R, +$25.45 net. HALF size из-за слабого BTC regime и среднего swing score.
- `SXT`, crypto intraday long, 14 июля: HALF size из-за BTC weakness/direction conflict/cross-venue disagreement; outcome сейчас `expired_flat`, ledger еще не обновлен.
- `XOM`, stocks intraday long, 13 июля: +4.583R, +$79.86 net. Это последняя и очень сильная stock paper-сделка.
- `T`, crypto intraday, 12 июля: +0.5R, +$6.85 net.
- `TLM`, crypto intraday, 12 июля: -1R, -$30.57 net.
- `VANRY` и `ETH`, crypto intraday: около 0R после защитного/fee-aware выхода.

## Что именно режут guards

### Crypto quality overlay

За последние 7 дней реально отправлено 34 intraday и 34 swing entry. Дополнительно overlay отправил в shadow 12 intraday и 6 swing кандидатов.

- Intraday `shadow_crypto_quality`: 11 resolved, суммарно -1.8R.
- Swing `shadow_crypto_quality`: 5 resolved, суммарно -0.5R.

На этой выборке overlay не душит прибыльную когорту, а убирает отрицательную. Частые причины: слабый BTC regime, конфликт направления с BTC, symbol/session cooldown и слабый swing score.

### Scalp

Scalp остается shadow-only. За последние 7 дней: 28 resolved outcomes, суммарно -6R; в предыдущие 7 дней около -9.3R. Отключение scalp в paper сейчас подтверждается данными.

### Circuit/risk guard

13 июля два crypto long-кандидата были переведены в shadow из-за кластера из 5-6 стопов в одном режиме:

- `KITE` swing: затем дал -1R, guard сохранил убыток.
- `ALLO` intraday: затем закрылся около 0R, эффект нейтральный.

Текущий combined portfolio guard не блокирует новые сигналы: около +4.08R по 18 resolved, crypto -0.5R и stocks +4.58R. Текущий BTC intraday risk-off также `false`. Следовательно, прямо сейчас система не находится под общим risk kill-switch.

### Stocks sector cap

За последние 7 дней sector cap оставил 7 stock-кандидатов в shadow; их итог около -0.43R. 13 июля он пропустил XOM (+4.583R), но удержал AAPL (-1R) и AMZN (+0.5R): чистый эффект заблокированной пары -0.5R. Пока cap выглядит полезным.

### Late-shadow

Late intraday shadow за неделю дал около +2.2R. Это единственная заметная отфильтрованная когорта с положительным hindsight-результатом. Однако эти входы были уже просрочены, поэтому включать их в paper задним числом нельзя. Правильная задача -- уменьшать latency и измерять достижимость цены, а не снимать freshness gate.

## Почему мало сделок по акциям

Большинство stock ideas не доходит до A/B:

- из 217 candidates за неделю только 10 получили A/B;
- 45 свежих C-кандидатов были planning-only из-за закрытого рынка;
- частые cap reasons: unknown/stale market context, отсутствие сильного catalyst, низкий RVOL, слабый sector context, отсутствие ORB confirmation и недостаточный RR;
- на 13-14 июля из 73 идей 69 были C, 3 B и 1 A.

### Найденная техническая проблема

`intraday_gate_context.market_context()` кеширует результат по `(date, hour)`. В 13:35 UTC, когда была доступна только первая 15m свеча, контекст сохранился как `unknown`. В 13:48 уже существовали свежие SPY/QQQ свечи 13:45 и новый расчет возвращал корректный `ok/chop`, но production process продолжал использовать закешированный `unknown` до конца часа.

Из-за этого, например, JPM со score 90.93 был демоутнут A -> C по `market_context_unknown_or_stale` плюс отсутствию catalyst. Это реальный искусственный недобор first-hour stock entries. Исправление должно инвалидировать cache при появлении новой benchmark-свечи либо кешировать только fresh/ok состояние на короткий TTL. Снижать score/RVOL/RR thresholds для компенсации не нужно.

## Иран и геополитический риск

Эскалация реальна: 14 июля AP сообщало о новых ударах США и ответных действиях Ирана, а Reuters -- о росте нефти к четырехнедельному максимуму и ухудшении risk appetite на фоне угроз потокам энергии ([AP](https://apnews.com/article/abd060c55feea216625689e57d8f76be), [Reuters/Euronext](https://live.euronext.com/en/financial-news/oil-hits-four-week-high-us-iran-conflict-escalates)).

Система принимает соответствующие сообщения из CNBC, MarketWatch, Yahoo, CryptoBriefing, ClashReport, WalterBloomberg и BWEtradfi. Они создают canonical geopolitical-risk events и risk warnings, в том числе для BTC и отдельных акций. Но `risk_advisory` по архитектуре не меняет actionability, поэтому эти headlines не являются причиной автоматической остановки торговли.

Есть слабое место: свежий macro-agent report в момент проверки использовал устаревшие/нерелевантные top headlines и не поднял текущий Iran cluster, хотя новости уже были в базе. Значит, ingestion работает лучше, чем выборка контекста macro agent. Геополитика могла косвенно ухудшить market regime и вызвать серию стопов, после которой сработал circuit-breaker, но утверждать, что именно Iran guard напрямую сократил поток, нельзя.

## Приоритеты

1. **P0: исправить cache market context акций.** Это подтвержденная техническая потеря валидных first-hour candidates.
2. **P0: материализовать audit trail portfolio guard.** На каждый batch сохранять timestamp, состояние, combined/asset R, причины и число заблокированных candidates. Сейчас исторический вклад глобального guard нельзя восстановить надежно.
3. **P1: починить выборку macro/geopolitical context.** Macro agent должен читать свежие canonical clusters с recency, source confidence, deduplication и impact rank, а не случайные последние заголовки.
4. **P1: сохранить текущие crypto quality, risk guard, sector cap и scalp disabled.** Их shadow-когорты сейчас отрицательны.
5. **P1: отдельно улучшать latency.** Считать signal -> decision -> alert -> first fill, attainable-price и missed-edge; freshness gate не ослаблять.
6. **P2: добавить UI funnel.** Показывать `candidates -> A/B -> actionable -> sent -> filled -> resolved` и причины shadow. Иначе визуально трудно отличить здоровую селективность от поломки.
7. **Не вводить глобальный hard block только по числу военных заголовков.** Для автоматического paper risk-down нужны как минимум подтвержденный canonical event из независимых источников плюс рыночное подтверждение через volatility/oil/BTC/SPY. Сначала это следует считать как counterfactual shadow policy.

## Финальный вердикт

Снижение количества crypto-сделок в основном здоровое: рынок перестал давать прежний поток трендовых long-сетапов, а отфильтрованные guard-когорты преимущественно убыточны. Ослаблять crypto-фильтры для восстановления старой частоты сейчас не следует.

По акциям малая частота частично оправдана качеством сетапов и закрытыми сессиями, но частично вызвана ошибкой кеша market context. Ее нужно исправить до выводов о том, что stock entry logic слишком строгая.

Paper остается прибыльным на последней неделе, но 68 crypto и 2 stock entries недостаточно для заявления о надежной долгосрочной доходности. Правильный следующий шаг -- устранить подтвержденные пробелы наблюдаемости и stock cache, не меняя доказавшие полезность guards.
