"""After LQ.F10 and LQ.F11: the pedia of Timber, Wool, Dairy and Leather names where each comes from, as the first
item of its "In the game" list (added by lq_f13_pedia.py). Applies to a checkout, writes minimal unique pairs.
usage: lq_f11_pedia.py <mod checkout> <pairs.json out>"""
import json, os, sys

mod, out = sys.argv[1], sys.argv[2]
FILES = {'TIMBER': 'Assets/XML/Text/RoM_GameText_SettlementEconomy.xml', 'DAIRY': 'Assets/XML/Text/RoM_GameText_SettlementEconomy.xml',
         'LEATHER': 'Assets/XML/Text/RoM_GameText_SettlementEconomy.xml', 'WOOL': 'Assets/XML/Text/RoM_GameText_Civilopedia_Bonuses.xml'}
HEAD = {'English': 'In the game', 'French': 'Dans le jeu', 'German': 'Im Spiel', 'Italian': 'Nel gioco', 'Spanish': 'En el juego'}
SRC = {
 'TIMBER': {'English': 'From lumber camps (Metal Casting) and lumbermills on forest, for every city on the trade network.',
            'French': 'Fourni par les camps de bûcherons (fonte des métaux) et les scieries en forêt, à chaque ville du réseau commercial.',
            'German': 'Aus Holzfällerlagern (Metallguss) und Sägewerken im Wald, für jede Stadt im Handelsnetz.',
            'Italian': 'Dai campi di taglialegna (fusione dei metalli) e dalle segherie in foresta, per ogni città della rete commerciale.',
            'Spanish': 'De los campamentos madereros (fundición) y los aserraderos en el bosque, para cada ciudad de la red comercial.'},
 'WOOL': {'English': 'From pastures and latifundia on sheep.', 'French': 'Fournie par les pâturages et les latifundia sur les moutons.',
          'German': 'Aus Weiden und Latifundien auf Schafen.', 'Italian': 'Dai pascoli e dai latifondi sulle pecore.', 'Spanish': 'De los pastos y latifundios sobre ovejas.'},
 'DAIRY': {'English': 'From pastures and latifundia on sheep and cows.', 'French': 'Fournis par les pâturages et les latifundia sur les moutons et les vaches.',
           'German': 'Aus Weiden und Latifundien auf Schafen und Rindern.', 'Italian': 'Dai pascoli e dai latifondi su pecore e mucche.', 'Spanish': 'De los pastos y latifundios sobre ovejas y vacas.'},
 'LEATHER': {'English': 'From pastures and latifundia on sheep, cows and horses.', 'French': 'Fourni par les pâturages et les latifundia sur les moutons, les vaches et les chevaux.',
             'German': 'Aus Weiden und Latifundien auf Schafen, Rindern und Pferden.', 'Italian': 'Dai pascoli e dai latifondi su pecore, mucche e cavalli.', 'Spanish': 'De los pastos y latifundios sobre ovejas, vacas y caballos.'},
}
ref = lambda x: ''.join(c if ord(c) < 128 else '&#%d;' % ord(c) for c in x)
state, pairs = {}, []
for good in ['TIMBER', 'DAIRY', 'LEATHER', 'WOOL']:
    f = FILES[good]
    if f not in state: state[f] = open(os.path.join(mod, f), 'rb').read().decode('latin-1')
    s = state[f]
    i = s.index('<Tag>TXT_KEY_BONUS_%s_PEDIA</Tag>' % good)
    for lang, h in HEAD.items():
        j = s.index('</%s>' % lang, i)
        mark = '[BOLD]%s[\\BOLD]' % ref(h)
        k = s.index(mark, i, j) + len(mark)
        add = '[NEWLINE][ICON_BULLET]' + ref(SRC[good][lang])
        assert add not in s[i:j]
        n = 30
        while s.count(s[k - n:k + 30]) != 1: n += 20
        old = s[k - n:k + 30]; new = s[k - n:k] + add + s[k:k + 30]
        pairs.append({'file': f, 'old': old, 'new': new})
        s = s[:k - n] + new + s[k + 30:]
        state[f] = s
for f, s in state.items(): open(os.path.join(mod, f), 'wb').write(s.encode('latin-1'))
json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(x)) for x in pairs), 'bytes of JSON')
