"""R37.12 (M83): nutrient profile of every food good, read from the USDA SR Legacy download.

Reads the FoodData Central SR Legacy CSV folder (FoodData_Central_sr_legacy_food_csv_2018-04) and writes
research/economy/data/nutrient_profiles.json: per good, the USDA food (fdc id) and its nutrients per 100 g.
Values the file does not hold are written as null, never guessed.

It also reads the Japanese Standard Tables of Food Composition (MEXT, 8th revised edition, 2023 supplement,
the whole-table workbook 20260327-mxt_kagsei-mext-000029402_02.xlsx) when given, for iodine (which SR Legacy does
not hold for these foods), tea infusions and whale. MEXT marks: "Tr" trace (written 0 with trace=true), "(0)"
estimated zero (written 0), "-" not measured (null).

usage: nutrient_profile.py <sr_legacy_csv_folder> [mext_xlsx] [out.json]
"""
import csv
import json
import os
import sys

NUTRIENTS = {  # USDA nutrient id: (key, unit)
    '1008': ('kcal', 'kcal'), '1003': ('protein', 'g'), '1004': ('fat', 'g'), '1051': ('water', 'g'),
    '1162': ('vit_c', 'mg'), '1106': ('vit_a_rae', 'ug'), '1114': ('vit_d', 'ug'),
    '1165': ('thiamin', 'mg'), '1166': ('riboflavin', 'mg'), '1167': ('niacin', 'mg'),
    '1190': ('folate_dfe', 'ug'), '1178': ('b12', 'ug'),
    '1089': ('iron', 'mg'), '1095': ('zinc', 'mg'), '1087': ('calcium', 'mg'), '1090': ('magnesium', 'mg'),
    '1092': ('potassium', 'mg'), '1093': ('sodium', 'mg'), '1100': ('iodine', 'ug'), '1103': ('selenium', 'ug'),
    # R64 (M112): tryptophan for niacin equivalents (NE = niacin + tryptophan mg / 60); carbohydrate, sugars, fibre and
    # alcohol for the hyper-palatability criteria, Holt's fullness drivers and the alcohol harm term
    '1175': ('vit_b6', 'mg'), '1210': ('tryptophan', 'g'), '1005': ('carbohydrate', 'g'), '2000': ('sugars', 'g'), '1079': ('fiber', 'g'),
    '1018': ('alcohol', 'g'),
}

# game good -> list of (form, fdc id); the first form is the good as eaten by default
GOODS = {
    'BONUS_WHEAT': [('grain', '168890'), ('bread', '172690')],   # R72: bread is the default form (user U136); home recipe, not enriched
    'BONUS_RICE': [('brown', '169703'), ('polished', '169756')],
    'BONUS_CORN': [('grain', '170288')],
    'BONUS_POTATO': [('raw', '170026'), ('boiled', '170438')],
    'BONUS_COW': [('meat', '169430'), ('liver', '169451'), ('heart', '168625'), ('kidneys', '169449'), ('lean', '174760'),
                  ('fat (suet)', '170193')],   # R69 organs; R72 lean and fat for the whole animal (user U117)
    'BONUS_PIG': [('meat', '167818'), ('liver', '167862'), ('heart', '168267'), ('kidneys', '168270'), ('lean', '168220'),
                  ('fat (backfat)', '167811')],
    'BONUS_SHEEP': [('meat', '172545'), ('lean', '174307'), ('liver', '172531'), ('heart', '172527'), ('kidneys', '174354')],
    'BONUS_DEER': [('meat', '173855')],
    'BONUS_HORSE': [('meat', '175086')],
    # R64: roe and liver for the whole cod (Torry Advisory Note 17 part shares); SR Legacy has no raw Atlantic cod liver,
    # so the nearest record, lingcod liver (Alaska Native), stands for it and is named as such
    'BONUS_FISH': [('cod', '171955'), ('herring', '175116'), ('salt cod', '174190'), ('roe', '175132'),
                   ('liver (lingcod)', '169810'), ('Pacific herring', '173669'), ('Atlantic mackerel', '175119'),
                   ('tuna (bluefin)', '173706'), ('salmon (Atlantic, wild)', '173686'), ('anchovy', '174182')],
    'BONUS_CLAM': [('raw', '174214')],
    'BONUS_CRAB': [('raw', '174204')],
    'BONUS_SHRIMP': [('raw', '174210')],
    'BONUS_WHALE': [('meat', '169797'), ('blubber (bowhead)', '167623'), ('liver', '168980'), ('oil (beluga)', '168981')],   # R72 (user U108-U111)
    'BONUS_DAIRY': [('milk', '172217'), ('cheese', '173414'), ('butter', '173410')],
    'BONUS_BANANA': [('raw', '173944')],
    'BONUS_LEMON': [('raw', '167746'), ('juice', '167747')],
    'BONUS_APPLE': [('raw', '171688'), ('dried', '171691')],
    'BONUS_OLIVES': [('olives', '169094'), ('oil', '171413')],
    'BONUS_SUGAR': [('brown', '168833'), ('molasses', '168820')],
    'BONUS_WINE': [('grapes', '174683'), ('raisins', '168165'), ('wine', '173190')],
    'BONUS_ALCOHOL': [('beer', '168746')],
    'BONUS_TEA': [('black, brewed', '173227'), ('green, brewed', '171917'), ('herbal, brewed', '173232')],   # R72: herbal teas grouped (user U152)
    'BONUS_SALT': [('table salt', '173468')],
    # references, not game goods (garden and field foods the city may grow without a resource)
    'REF_EGG': [('raw', '171287')], 'REF_KELP': [('raw', '168457')], 'REF_LENTILS': [('raw', '172420')],
    'REF_CABBAGE': [('raw', '169975')], 'REF_BARLEY': [('hulled', '170283')], 'REF_RYE': [('grain', '168884')],
    'REF_ONION': [('raw', '170000')],
    # references for the intake ceilings (R40.3): fruit as watermelon (M86), pasta, ground beef, oranges
    'REF_WATERMELON': [('raw', '167765')], 'REF_PASTA': [('cooked', '169737')],
    'REF_GROUND_BEEF': [('80/20 raw', '174036')], 'REF_ORANGE': [('raw', '169097')],
    'REF_SUGAR': [('granulated', '169655')],
}


# game good -> list of (form, MEXT food number)
MEXT = {
    'BONUS_WHEAT': [('soft flour', '01015')], 'BONUS_RICE': [('polished', '01083')], 'BONUS_CORN': [('grain', '01131')],
    'BONUS_POTATO': [('raw', '02017')], 'BONUS_COW': [('shoulder', '11030')], 'BONUS_PIG': [('loin', '11123'), ('liver', '11166')],
    # R68: small fish eaten whole (refuse 0-15 %) for rice and river cultures, and a whole dried sardine
    'BONUS_FISH': [('cod', '10205'), ('sardine', '10047'), ('salmon', '10134'), ('bonito', '10086'),
                   ('pond smelt, whole', '10276'), ('loach, whole', '10213'), ('dried sardine, whole (mezashi)', '10053')],
    'BONUS_CLAM': [('asari clam', '10281'), ('oyster', '10292')],
    'BONUS_WHALE': [('red meat', '11110'), ('skin (honkawa)', '11112'), ('belly (unesu)', '11111')],
    'BONUS_DAIRY': [('milk', '13003'), ('processed cheese', '13040')], 'BONUS_LEMON': [('whole fruit', '07155')],
    'BONUS_APPLE': [('with skin', '07176')], 'BONUS_BANANA': [('raw', '07107')],
    'BONUS_WINE': [('grapes', '07116'), ('raisins', '07117'), ('red wine', '16011')],
    'BONUS_TEA': [('sencha infusion', '16037'), ('gyokuro infusion', '16034'), ('kamairi infusion', '16038'),
                  ('bancha infusion', '16039'), ('black tea infusion', '16044'), ('matcha powder', '16035'),
                  ('sencha leaves', '16036')],
    'BONUS_SALT': [('salt', '17012')], 'BONUS_SUGAR': [('white sugar', '03003')],
    'REF_EGG': [('raw', '12004')], 'REF_KELP': [('ma-kombu, dried', '09017')], 'REF_CABBAGE': [('raw', '06061')],
}
MEXT_COLS = {'ENERC_KCAL': 'kcal', 'PROT-': 'protein', 'NA': 'sodium', 'K': 'potassium', 'CA': 'calcium', 'FE': 'iron',
             'ZN': 'zinc', 'ID': 'iodine', 'VITA_RAE': 'vit_a_rae', 'THIA': 'thiamin', 'NIA': 'niacin', 'VITB12': 'b12',
             'FOL': 'folate', 'VITC': 'vit_c',
             # R68: fat, water, magnesium, selenium, riboflavin, B6, carbohydrate, fibre and niacin equivalents (MEXT gives NE)
             'FAT-': 'fat', 'WATER': 'water', 'MG': 'magnesium', 'SE': 'selenium', 'RIBF': 'riboflavin', 'VITB6A': 'vit_b6',
             'CHOCDF-': 'carbohydrate', 'FIB-': 'fiber', 'NE': 'niacin_ne', 'REFUSE': 'refuse_pct'}


def read_mext(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)['\u8868\u5168\u4f53']   # the whole-table sheet
    rows = list(ws.iter_rows(values_only=True))
    hdr = [r for r in rows[:20] if r and '\u6210\u5206\u8b58\u5225\u5b50' in [str(c) for c in r if c]][0]  # component ids
    idx = {str(c): i for i, c in enumerate(hdr) if c}
    want = {code for forms in MEXT.values() for _, code in forms}
    out = {}
    for r in rows:
        if len(r) > 3 and r[1] in want:
            d = {'mext_no': r[1], 'mext_name': str(r[3]).replace('\u3000', ' ')}
            for col, key in MEXT_COLS.items():
                v = r[idx[col]]
                t = str(v).strip() if v is not None else '-'
                if t == 'Tr':
                    d[key] = 0
                    d.setdefault('trace', []).append(key)
                elif t in ('-', ''):
                    d[key] = None
                else:
                    d[key] = float(t.strip('()'))
            out[r[1]] = d
    return out


def main(folder, out, mext_path=None):
    desc = {r['fdc_id']: r['description'] for r in csv.DictReader(open(os.path.join(folder, 'food.csv'), encoding='utf-8'))}
    want = {fid for forms in GOODS.values() for _, fid in forms}
    val = {}
    for r in csv.DictReader(open(os.path.join(folder, 'food_nutrient.csv'), encoding='utf-8')):
        if r['fdc_id'] in want and r['nutrient_id'] in NUTRIENTS:
            val.setdefault(r['fdc_id'], {})[NUTRIENTS[r['nutrient_id']][0]] = float(r['amount'])
    res = {'about': 'Nutrients per 100 g from USDA FoodData Central SR Legacy (2018-04); null = not in the file. '
                    'Written by research/economy/plan/tools/nutrient_profile.py (R37.12).',
           'units': {k: u for k, u in NUTRIENTS.values()}, 'goods': {}}
    for good, forms in GOODS.items():
        res['goods'][good] = [dict(form=f, fdc_id=int(fid), usda=desc[fid],
                                   **{k: val.get(fid, {}).get(k) for k, _ in NUTRIENTS.values()}) for f, fid in forms]
    if mext_path:
        m = read_mext(mext_path)
        res['mext_about'] = ('Per 100 g of edible portion, Japanese Standard Tables of Food Composition (MEXT, 8th revised '
                             'edition, 2023 supplement); iodine in ug; trace values written 0 and listed under trace.')
        res['mext'] = {g: [dict(form=f, **m[c]) for f, c in forms if c in m] for g, forms in MEXT.items()}
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    print('wrote', out, len(res['goods']), 'goods')


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    args = sys.argv[1:]
    mext = args.pop(1) if len(args) > 1 and args[1].endswith('.xlsx') else None
    main(args[0], args[1] if len(args) > 1 else os.path.join(here, '..', '..', 'data', 'nutrient_profiles.json'), mext)
