# Working method for game analyses

This is the method for every analysis of a user's game and for every AI change built from
one. It exists because earlier analyses failed in the same ways again and again:
- effects were quoted from notes;
- reasons were mixed into descriptions;
- figures were used for the wrong turn;
- tools were built before the questions were known;
- old text was patched when a fresh start was asked for.

Notes and context summaries are lossy, so the rules live here and are read again each time.

## Order of work

No step starts before the previous one is written down.

1. **Questions.** Write the questions the analysis must answer, and for each the source that
   answers it (see Sources).
   - A tool is built or changed only when a question has no source. Say so in one line first:
     the question, the missing source, the cost.
   - The DLL is not rebuilt for an analysis.
2. **Setup first.** In order:
   - the scenario or map, the game options, the players and their starts;
   - then the whole game, for all players;
   - then the human.
3. **Description.** Figures with their source, ordered by turn.
   - No "because", "so" or "to" clauses.
   - Headings are turn ranges or topics, not purposes.
4. **Readings.** In a separate section. Each reading:
   - states the situation at that turn, from data of that turn only;
   - names the options the player had then (from the XML and the techs known);
   - says what was chosen;
   - gives the goal that explains the choice;
   - lists the facts it rests on and what would contradict it.

   This is how the player's thinking is reconstructed. The player is not asked to supply it.
5. **AI comparison.** An evidence tree only after 1–4. Each leaf gives the data, the function
   that produced it, and a status: *traced* (the code path is confirmed) or *open* (with the
   data that would close it).
6. **Self-check** (below), then one commit and one reply.

## Sources, in order of strength

1. **The scenario file** (`.CivBeyondSwordWBSave`, named in the save's init data). It gives:
   - the game options and each team's starting techs;
   - the terrain;
   - each player's starting units.

   The units' plots are the starts. The `StartingX/Y` fields can be stale.
2. **The save**, read with the DLL's own load functions in the headless harness
   (`toolchain/harness/sav2dat.py`, then `harness.exe save`, with `HARNESS_HISTORY_DIAG=1`). The
   state dump holds:
   - cities, with every city tile and its worked flag;
   - units, techs and civics;
   - each player's history series (score, economy, industry, agriculture, power, culture);
   - the units created by type, and the replay messages.

   These are facts at one moment, the save's turn.
3. **The war log** (`WarLog.log`, `WAR_LOG` = 1). Its line types are described in
   `builds/war-log/README.md`. These are facts over time.
4. **The AI decision log** (BBAI log), from turns replayed after the save. It shows which branch
   of the code made each AI choice, for turns after the save.
5. **Headless AI-only games.** These check safety, side effects and turn time. Self-play hides
   weaknesses both sides share, so they are not evidence of how the AI fares against the human.

Effects of civics, buildings, units, techs and improvements come from the XML records
(`tools/xmlread.py`, or its `records.json`).

Neither the save nor the raw log is published. Only derived tables are.

## Hard rules

- **Effects:** looked up in the XML records at the time of writing, never quoted from memory,
  notes or a summary. Quote the field (for example `ImprovementYieldChanges`).
  - Commerce arrays are ordered gold, research, culture, espionage.
  - Yield arrays are ordered food, hammers, commerce.
- **Names:** a name that is both a tech and a civic (Slavery, Priesthood) is checked against
  its field.
- **Turns:** a figure carries its turn. A figure from the save is never used for an earlier
  turn.
- **Cities:** captured and founded cities are kept apart.
- **Labels:** interpretation is labelled and kept in the readings.
- **Fresh starts:** when told to start over, start over. Old text is replaced, not edited.
- **Autonomy:** no mid-way questions. Unknowns are marked *open*. One delivery at the end.

## Data mechanics

- The CSV files have CRLF line endings. Read them with Python's `csv` module, not `awk`.
- The last turn of a log is usually incomplete; use the last full turn.
- In the `M` line, `commerce` is `calculateTotalCommerce` (after modifiers); `hammers` and
  `food` are `calculateTotalYield`.
- Anarchy turns show commerce 1.
- A captured city keeps its original founding turn.
- The `A ORDER` line gives the turn an order was given, not when it was finished.

## Processing

`tools/gamedata.py` turns one game's files into the same tables every time:
- economy, techs, spending, buildings, wars and battles;
- city state during wars, and great people;
- the human's orders, builds, civics, research and commands;
- with the save dump: cities, tiles and civic scores;
- with the scenario file: players, starts, starting techs and room;
- with the decision log: AI production choices by branch.

It also writes `summary.md`, with figures only and no interpretation.

```sh
python3 -I toolchain/harness/initcore.py save.init <src>/Assets/CvGameCoreDLL/CvEnums.h <src>/Assets/XML > init.json
python3 -I tools/gamedata.py WarLog.log games/gameN --human <player> --records <xmldb>/records.json \
    [--state run.jsonl.state0.json] [--scenario <map>.CivBeyondSwordWBSave] [--init init.json] [--bbai logs/BBAI.log]
```

- `initcore.py` reads the save's setup block (written by `sav2dat.py`): the real options and
  victories, custom names and handicaps. The scenario file only gives the defaults.
- Deal and diplomacy lines print game indices. `xmlread.py` writes each record's `_index`
  (load order), and `gamedata.py` uses it for techs and resources.
- `xmlread.py` reads only the mod's Assets. Base-game XML that RoM does not replace (for
  example `CIV4HurryInfo.xml`) is read from the BTS install.
- Run `xmlread.py` on a real directory: `os.walk` does not follow the symlinked folders of a
  harness mod root.

## Layout

```
games/gameN/
  analysis.md   1 the game, 2 the human (description, readings), 3 why the AI lost, 4 missing data
  summary.md    generated figures
  *.csv         generated tables (regenerate rather than edit)
diagnosis-1.md  the ranked gaps across games, linked to the analyses
```

## Self-check before delivering

Each must pass, or the text is fixed first:
- Every figure names its source and turn.
- Every effect was checked against the XML records in this session.
- No reason clause appears in a description.
- Every reading names its facts and what would contradict it.
- Captured and founded cities are not mixed.
- No claim rests on an incomplete turn.

## Sharing

- The reply gives the main figures in a few lines and links the analysis.
- Tables, tools and the analysis are committed together, so every figure can be recomputed.
- An error found later is corrected in the file it belongs to, and noted there.
