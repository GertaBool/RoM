# Recording games with city defence against staged forces (change S2)

This DLL is the one in `builds/war-log` (the war log with turn-start lines, the four war-AI fixes
on), build `a1d2e324699d`, plus one AI change, S2 (`fixes/staging-defence.patch`), build
`c2e0b0aa630e`. Games you play with it count for prediction P4 and not for P2; games played with
`builds/war-log` count for P2 and not for P4.

## What S2 changes

In every game so far you opened each war yourself: you moved an army next to an AI city while at
peace, declared, and took the city the same turn (`research/ai-warfare/study/staging.md`). The AI
could not see it coming. A city's danger counted only units of a civilization already at war with
it, and only on its own landmass, so an army at peace next door, or aboard ships, counted nothing.

With S2, each AI city looks at the land units of other civilizations that could reach it this turn,
on land by their moves and aboard ships by the ship's moves. It computes the exact chance that they
would take it if they attacked now. When that chance reaches the leader's threshold, the city counts
as in danger: it builds defenders before workers, settlers and buildings, and it wants one defender
more than it has. Your units always count; another AI's units count only when the city's owner could
imagine a war with it.

| Switch in `GlobalDefinesAlt.xml` | Default | Meaning |
|---|---|---|
| `AI_STAGED_FORECAST` | 250 | The capture chance, per mille, at which a city acts: 250 is a quarter. Each leader adds ten per point of its attack-odds trait, so bold leaders wait longer. 0 switches S2 off |

## Setup

As for `builds/war-log` (see its README): copy `CvGameCoreDLL.dll` over `Assets/CvGameCoreDLL.dll`
and `GlobalDefinesAlt.xml` over `Assets/XML/GlobalDefinesAlt.xml` (`WAR_LOG` = 1, `WAR_LOG_SEAT` = 0),
set `LoggingEnabled = 1` in `CivilizationIV.ini`, and start each game from turn 0. After each game,
send the `WarLog.log` (renamed) and, if you like, the autosaves.

The war log's `H` line names this build, `c2e0b0aa630e`; P4 counts a game only if it does.
