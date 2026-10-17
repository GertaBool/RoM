# How game data is gathered and shared

## Sources, in order of strength

1. **The save** (`.CivBeyondSwordSave`). It holds the complete game state: every tile, city,
   unit and civic. It is read with the DLL's own load functions in the headless harness
   (`toolchain/harness/sav2dat.py`, then `harness.exe save`). The harness then writes a
   state dump: cities, every city tile with a worked flag, units with their missions,
   civics, and each AI's own civic and building scores. These are facts at one moment.
2. **The war log** (`WarLog.log`, `WAR_LOG` = 1). Each line type is described in
   `builds/war-log/README.md`. These are facts over time: events, each turn's economy, and
   every command the human gives.
3. **The AI decision log** (BBAI log). Turns are replayed from the save in a harness build
   with logging on. It shows which branch of the code made each AI choice. These are
   causes, but for turns after the save, played by the same AI.
4. **Headless AI-only games.** These check safety, side effects and turn time. Self-play
   hides weaknesses both sides share, so they are not evidence of how the AI fares
   against the human.

Neither the save nor the raw log is published. Only derived tables are.

## Processing

`tools/gamedata.py` turns one game's files into the same tables every time:
- economy, techs, spending, buildings, wars, battles;
- city state during wars, great people;
- the human's orders, builds, civics, research and commands;
- with the save dump: cities, tiles and civic scores;
- with the decision log: AI production choices by branch.

It also writes `summary.md`, with figures only and no interpretation.

```sh
python3 tools/gamedata.py WarLog.log games/gameN --human <player> --records <xmldb>/records.json \
    [--state run.jsonl.state0.json] [--bbai logs/BBAI.log]
```

## Layout

```
games/gameN/
  analysis.md   the written analysis: the human's play reconstructed, the evidence tree
  summary.md    generated figures
  *.csv         generated tables (regenerate rather than edit)
diagnosis-1.md  the ranked gaps across games, linked to the analyses
```

## Evidence rules

- Every claim names its source: a table and column, or a log line type and field.
- A name that is both a tech and a civic (Slavery, Priesthood) is checked against its
  field before use.
- Effects of a civic, building or unit are taken from the XML (`tools/xmlread.py`
  records), not from memory of other mods or standard Civ4.
- A figure from one moment (the save) is not used for another moment (a war 60 turns
  earlier).
- Captured cities are kept apart from founded ones whenever improvements or buildings are
  attributed.
- Each leaf of an evidence tree is marked *traced*, when the code path is confirmed, or
  *open*, when more data is needed. Open leaves name the data that would close them.
- Interpretation is labelled as such and kept separate from the figures.

## Sharing

- Per game, the answer gives the main figures and points to `games/gameN/analysis.md`.
- Tables and the analysis are committed together, so every figure can be recomputed.
- A correction is made in the file it belongs to, and noted there.
