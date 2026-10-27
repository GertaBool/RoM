"""M44: CvPlayerAI::AI_baseBonusVal on GitLab claude/settlement-economy at cf43846b. In the building loop every step
after the bonus-dependent terms multiplies, divides or zeroes iTempValue, so a building whose terms are 0 adds exactly
0; the loop skipped nothing and called canConstruct (a const test) for every building class of the civilization on
every recalculation of every good. The gate skips those buildings; the value is unchanged.
usage: bonusval_edits.py <mod checkout> <pairs.json out>"""
import json, os, sys
mod, out = sys.argv[1], sys.argv[2]
f = 'Assets/CvGameCoreDLL/CvPlayerAI.cpp'
old = """					}
					
					{
						// determine whether we have the tech for this building
"""
new = """					}
					
					// Every step below multiplies, divides or zeroes iTempValue: a building none of whose terms depend on
					// eBonus adds exactly 0, so it is skipped (and canConstruct is not asked for it)
					if (iTempValue != 0)
					{
						// determine whether we have the tech for this building
"""
p = os.path.join(mod, f); s = open(p, 'rb').read().decode('latin-1'); nl = '\r\n' if '\r\n' in s else '\n'
o, n = old.replace('\n', nl), new.replace('\n', nl)
assert s.count(o) == 1, s.count(o)
open(p, 'wb').write(s.replace(o, n).encode('latin-1'))
json.dump([{'file': f, 'old': o, 'new': n}], open(out, 'w'), indent=0)
print('1 pair')
