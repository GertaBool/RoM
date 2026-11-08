# Audit of the translation of the user's inputs file (R75, M125)

The file: `data/user_inputs_m120.ods`, one sheet, 198 rows (header + U001-U197), 8 columns: id, section, item, unit,
needed_for, nuance, your_value, your_nuance. No cell comments.

## Step 1: ODS to CSV (`plan/tools/ods_audit.py`): faithful

- LibreOffice's independent conversion and `data/user_inputs_m120.csv` agree on rows, columns, header and every cell.
- The only differences are 20 number cells written as shown in the sheet (`10.00kg`, `70.00%`) against LibreOffice's stored value (`10`, `70%`); shown and stored values are equal in all 147 number cells.

## Step 2: CSV to `data/user_inputs.json` (`plan/tools/user_inputs_apply.py`): not fully faithful

### A. The edited template columns were never read
The reader took only `your_value` and `your_nuance`. The user also edited item, unit and nuance (listed by `ods_audit.py`):
- **Nuance column edits not stored:**
  - U122: "an Indian wrote this";
  - U155: "Canadian means 9.8 and 11.2 (June-October)";
  - U169: "estimate for dried fruit".
- **Your-nuance notes not stored:**
  - U129: "2000g = 2L of wine";
  - U132: "Brewed tea in liters";
  - U133: "Brewed coffee in liters".
- **Item and unit edits:** the values were mapped by row, so the numbers land where they belong:
  - PAL by work U157-U160;
  - spoilage classes U168-U172;
  - sodium in g, U174, converted to mg;
  - animal rows U117-U120 as meat, fat, organs.

  The edited labels themselves are not kept.

### B. Values stored faithfully
- **Satiety:** all 88 rows match. The one "(not relevant)" row is stored as no value.
- **Each section, value and text as given:**
  - U089 and U090;
  - dessert goods (29, after the parser fix), share 100 % and order text;
  - U094-U099;
  - U100-U107, verbatim;
  - whale, pig, cow, sheep, deer and horse shares;
  - ceilings U121-U135 (numbers);
  - default forms with text and notes;
  - fish catch (6 regions x 6 categories, sums checked) and herring fat 12 %;
  - PAL;
  - lactase shares and note;
  - not relevant (6 rows);
  - spoilage;
  - athletes' optima (17);
  - U190;
  - contaminants.

### C. Readings added by the tool or the model that the user did not write
1. **U094-U099:** the reader filed these under "rich city" and the model called them a conversion of a rich city. The user: artisanal or industrial processes, independent of wealth (M122). The label is wrong.
2. **U105 strength:** the model put 200 % at its own urea limit (4.06 g/kg, 284 g at 70 kg), not at the user's "roughly 288 g". It also read "capped at 200 %" as reaching 200 % at that limit. "And health" (U103) is left out.
3. **U107 IQ:** the user gives no iodine for the floor of 70. The tool invented 15 ug. The user's note (exponential effect on all yields, subsistence below 70) is stored but not applied.
4. **U117:** the user replaced the cow shares 41.4 / 1.12 / 0.37 / 0.18. The model still split the organs by the old ratio 1.12 : 0.37 : 0.18, taken from those replaced shares.
5. **U121:** "Lemon cider: 1L (equivalent to 30g)". The tool set a 1,000 g ceiling on USDA lemon juice (167747). The user names cider (U147: "Cider in particular") and equates 1 L of it to 30 g of lemon. Neither the form nor the equivalence was carried.
6. **U152 tea:** "depends on the culture, brewed; ... better to group them together" (mountain, thyme, sage teas) was mapped to one USDA record, "tea, herb, other than chamomile" (173232). That form has no satiety row, so the model fell back to black tea's.
7. **Satiety of a bare key:** a bare key's row is the good's first USDA form (wheat grain 157). The R72 model gave wheat's default form, bread, the grain's 157; no bread row exists. `nutrition.json` (uncommitted) uses the grain row for the grain good.
8. **U093:** the tool counted grapes, raisins and dried apple as fruit and red wine (MEXT) with wine. These are readings.
9. **U154:** the record chosen for each fish category (pond smelt, herring, bluefin tuna, cod as eaten, wild salmon, mackerel) is the tool's choice.
10. **U173:** protein 300 g for a 140 kg wrestler, scaled by body weight / 140: a reading.

### D. Contradictions in the file, open (to ask)
- U194 and U196: the item says "tolerable daily intake" and the unit says "per week". The tool took per week.
- U108-U111: the base (live or carcass weight) is not stated.
