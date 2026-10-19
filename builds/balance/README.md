# Recording games with the balance against the leader (change B)

This DLL is the one in `builds/staging` (the war log, the four war-AI fixes and S2, build
`c2e0b0aa630e`) plus one AI change, B (`fixes/balance.patch`), build `e57a752b22ae`. Games you play
with it count for prediction P5, and not for P2 or P4.

## What B changes

In every logged game the AIs fought each other but never declared on you, even when you were far
ahead (`research/ai-warfare/study/doctrine.md`, reading R2). At the end of games 3 to 6 the reason is
measured: every AI's war test needs a target weaker than itself alone, and no AI alone was strong
enough. The only way to join a war counted only the civilizations already fighting you.

With B, an AI that has met a hegemon acts on it in three ways. The hegemon is the strongest
civilization it knows, holding more than 11% of the power of all the civilizations it has met.
- **The coalition counts.** When the hegemon is at war, the AI weighing whether to join counts,
  besides those already at war with it, every AI that would join this turn. Each of those decides
  with its own roll; no AI is told to join.
- **Envy matters.** The AI's reluctance to fight the hegemon drops by the leader's envy of
  better-ranked players, a field of each leader's XML record. Leaders without envy, and any leader
  friendly to the hegemon, behave as before.
- **Busy AIs may still join.** An AI whose wars are all against weaker civilizations may still join a
  war against the hegemon.

The hegemon can be you or an AI.

| Switch in `GlobalDefinesAlt.xml` | Default | Meaning |
|---|---|---|
| `AI_BALANCE_SHARE` | 110 | The share of known power, per mille, above which the strongest civilization met is a hegemon. 0 switches B off |
| `AI_STAGED_FORECAST` | 250 | S2, as in `builds/staging` |

## Setup

As for `builds/staging`: copy `CvGameCoreDLL.dll` over `Assets/CvGameCoreDLL.dll` and
`GlobalDefinesAlt.xml` over `Assets/XML/GlobalDefinesAlt.xml` (`WAR_LOG` = 1, `WAR_LOG_SEAT` = 0),
set `LoggingEnabled = 1` in `CivilizationIV.ini`, and start each game from turn 0 at Noble. After each
game, send the `WarLog.log` (renamed) and, if you like, the autosaves.

The war log's `H` line names this build, `e57a752b22ae`; P5 counts a game only if it does.
