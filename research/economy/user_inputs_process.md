# From the user's spreadsheet to data: the process (R76, M126)

| Step | Tool | Output | Stops when |
|---|---|---|---|
| 1. Store | (copy) | `data/user_inputs_m120.ods`, byte-identical to the upload | – |
| 2. Extract, losslessly | `plan/tools/ods_extract.py <ods> <stem> <scratch>` | `<stem>.cells.csv`: every non-empty cell with row, column, header, shown text, stored value and type, number format (data style, decimals, suffix such as `kg` or `%`), note. `<stem>.csv`: the sheet as shown | formulas, merged or hidden cells, more than one sheet, rich text, links or images; a number whose shown text differs from its stored value under its own format; any cell that differs from LibreOffice's conversion, as shown or as stored (exact decimal arithmetic) |
| 3. Sort every row | `plan/tools/user_inputs_questions.py <stem>.cells.csv <stem>` | `<stem>.rows.csv`: each row EXACT (a number in the unit asked, nothing to interpret), VERBATIM (complete text), ANSWERED (answered earlier, with the prompt) or QUESTION; with every edit the user made to the template's columns. `<stem>.questions.csv` and `.ods`: one line per question, quoting the cell, with empty answer columns | – (it never translates) |
| 4. Ask | the questions file | the user's answers | – |
| 5. Translate | a translator that reads only EXACT rows and answers | the data files | a row that is neither EXACT nor answered |

Semantic rules:
- **The user's edits to item, unit or nuance define the row.** They are read, listed and never ignored.
- **A note that gives a source or names a unit keeps the number exact,** and the note is stored with it.
- **Everything else that needs a reading is asked.** No default and no "nearest record" without the user's answer.

Tested on the real file:
- 198 rows, 8 columns, 1,386 cells: 1,239 text, 130 number, 17 percentage. Identical to LibreOffice as shown and as stored.
- A copy with one cell altered stopped the run.
- Rows: 108 exact, 14 verbatim, 11 answered, 64 questions.
