"""LQ.F13.T6: pedia text of Timber, Wool, Leather and Dairy lists their roles: what the records do now (looked up in
the XML at the base commit, see the plan task note) and what waits for the goods accounts.
Appends a section to each language line of the four _PEDIA entries; writes minimal unique (old, new) pairs.
usage: lq_f13_pedia.py <mod checkout> <base commit> <pairs.json out>"""
import json, subprocess, sys

mod, base, out = sys.argv[1], sys.argv[2], sys.argv[3]
FILES = {'TIMBER': 'Assets/XML/Text/RoM_GameText_SettlementEconomy.xml',
         'DAIRY': 'Assets/XML/Text/RoM_GameText_SettlementEconomy.xml',
         'LEATHER': 'Assets/XML/Text/RoM_GameText_SettlementEconomy.xml',
         'WOOL': 'Assets/XML/Text/RoM_GameText_Civilopedia_Bonuses.xml'}
HEAD = {  # (now, later)
    'English': ('In the game', 'With the goods accounts (not yet in the game)'),
    'French': ('Dans le jeu', 'Avec les comptes de biens (pas encore dans le jeu)'),
    'German': ('Im Spiel', 'Mit den Güterkonten (noch nicht im Spiel)'),
    'Italian': ('Nel gioco', 'Con i conti delle merci (non ancora nel gioco)'),
    'Spanish': ('En el juego', 'Con las cuentas de bienes (aún no en el juego)'),
}
T = {
 'TIMBER': {
  'English': (["Firewood for cooking and heat: health in every city connected to it.",
               "Building material: faster construction of the buildings and wonders of the ancient, classical and medieval eras.",
               "Faster production of wooden ships, settlers, workers and work boats, and of archer and siege units up to the medieval era.",
               "Charcoal: more production in cities with a Forge or an Iron Forge.",
               "Used by the Carpenters Guild."],
              ["The fuel need of every city from the start, larger with size; coal and then oil take it over. A shortfall costs.",
               "Used up as material in buildings and units, not only a faster build.",
               "Keeps, but is bulky: storage limits the stock. Traded in tonnes."]),
  'French': (["Bois de chauffage pour cuisiner et se chauffer : santé dans chaque ville qui y est reliée.",
              "Matériau de construction : construction plus rapide des bâtiments et merveilles des ères antique, classique et médiévale.",
              "Production plus rapide des navires en bois, colons, ouvriers et bateaux de travail, et des archers et engins de siège jusqu'à l'ère médiévale.",
              "Charbon de bois : plus de production dans les villes dotées d'une forge ou d'une forge à fer.",
              "Ressource de la guilde des charpentiers."],
             ["Le besoin de combustible de chaque ville dès le début, croissant avec sa taille ; le charbon puis le pétrole prennent le relais. Une pénurie coûte.",
              "Consommé comme matériau par les bâtiments et les unités, et pas seulement source de construction plus rapide.",
              "Se conserve, mais est encombrant : le stockage limite les réserves. Échangé en tonnes."]),
  'German': (["Brennholz zum Kochen und Heizen: Gesundheit in jeder damit verbundenen Stadt.",
              "Baustoff: schnellerer Bau der Gebäude und Wunder der Antike, der Klassik und des Mittelalters.",
              "Schnellere Produktion von Holzschiffen, Siedlern, Arbeitern und Arbeitsbooten sowie von Bogenschützen und Belagerungseinheiten bis zum Mittelalter.",
              "Holzkohle: mehr Produktion in Städten mit Schmiede oder Eisenschmiede.",
              "Rohstoff der Zimmermannsgilde."],
             ["Der Brennstoffbedarf jeder Stadt von Anfang an, mit ihrer Größe wachsend; Kohle und dann Öl übernehmen ihn. Ein Mangel kostet.",
              "Als Material von Gebäuden und Einheiten verbraucht, nicht nur ein schnellerer Bau.",
              "Hält sich, ist aber sperrig: der Lagerraum begrenzt den Vorrat. In Tonnen gehandelt."]),
  'Italian': (["Legna da ardere per cucinare e scaldarsi: salute in ogni città collegata.",
               "Materiale da costruzione: costruzione più rapida degli edifici e delle meraviglie delle ere antica, classica e medievale.",
               "Produzione più rapida di navi di legno, coloni, lavoratori e barche da lavoro, e di arcieri e unità d'assedio fino all'era medievale.",
               "Carbone di legna: più produzione nelle città con una fucina o una fucina del ferro.",
               "Risorsa della gilda dei carpentieri."],
              ["Il fabbisogno di combustibile di ogni città fin dall'inizio, crescente con le dimensioni; poi lo coprono il carbone e il petrolio. Una carenza costa.",
               "Consumato come materiale da edifici e unità, non solo una costruzione più rapida.",
               "Si conserva, ma è ingombrante: lo spazio di deposito limita la scorta. Commerciato in tonnellate."]),
  'Spanish': (["Leña para cocinar y calentarse: salud en cada ciudad conectada.",
               "Material de construcción: construcción más rápida de los edificios y maravillas de las eras antigua, clásica y medieval.",
               "Producción más rápida de barcos de madera, colonos, trabajadores y botes de trabajo, y de arqueros y unidades de asedio hasta la era medieval.",
               "Carbón vegetal: más producción en las ciudades con forja o forja de hierro.",
               "Recurso del gremio de carpinteros."],
              ["La necesidad de combustible de cada ciudad desde el principio, mayor con su tamaño; después la cubren el carbón y el petróleo. La escasez cuesta.",
               "Consumida como material por edificios y unidades, no solo una construcción más rápida.",
               "Se conserva, pero es voluminosa: el almacenamiento limita las reservas. Se comercia en toneladas."]),
 },
 'WOOL': {
  'English': (["Clothing: happiness in cities with the essentials buildings (Settlement, Town, City, Metropolitan).",
               "Used by the Drapers Guild and Emperors Clothing."],
              ["The clothing need of every citizen, met by wool, leather, fur or cotton.",
               "Cloth for the textile trade, from household spinning to the textile mills; tents, blankets and sails.",
               "Keeps once shorn. Traded in bales; sheep are the means of producing it."]),
  'French': (["Vêtements : bonheur dans les villes dotées des bâtiments essentiels (colonie, bourg, cité, métropole).",
              "Ressource de la guilde des drapiers et d'Emperors Clothing."],
             ["Le besoin de vêtements de chaque citoyen, couvert par la laine, le cuir, la fourrure ou le coton.",
              "Le drap de l'industrie textile, du filage domestique aux filatures ; tentes, couvertures et voiles.",
              "Se conserve une fois tondue. Échangée en balles ; les moutons sont le moyen de la produire."]),
  'German': (["Kleidung: Zufriedenheit in Städten mit den Grundbauten (Siedlung, Kleinstadt, Stadt, Metropole).",
              "Rohstoff der Tuchmachergilde und von Emperors Clothing."],
             ["Der Kleidungsbedarf jedes Bürgers, gedeckt durch Wolle, Leder, Pelz oder Baumwolle.",
              "Tuch für das Textilgewerbe, vom häuslichen Spinnen bis zur Textilfabrik; Zelte, Decken und Segel.",
              "Hält sich nach der Schur. In Ballen gehandelt; Schafe sind das Mittel, sie zu erzeugen."]),
  'Italian': (["Vestiario: felicità nelle città con gli edifici essenziali (insediamento, borgo, città, metropoli).",
               "Risorsa della gilda dei drappieri e di Emperors Clothing."],
              ["Il fabbisogno di vestiario di ogni cittadino, coperto da lana, cuoio, pelliccia o cotone.",
               "Panno per l'industria tessile, dalla filatura domestica alle filande; tende, coperte e vele.",
               "Si conserva una volta tosata. Commerciata in balle; le pecore sono il mezzo per produrla."]),
  'Spanish': (["Vestido: felicidad en las ciudades con los edificios esenciales (asentamiento, villa, ciudad, metrópoli).",
               "Recurso del gremio de pañeros y de Emperors Clothing."],
              ["La necesidad de vestido de cada ciudadano, cubierta por lana, cuero, piel o algodón.",
               "Paño para la industria textil, del hilado doméstico a las fábricas textiles; tiendas, mantas y velas.",
               "Se conserva una vez esquilada. Se comercia en balas; las ovejas son el medio de producirla."]),
 },
 'LEATHER': {
  'English': (["Clothing: happiness in cities with the essentials buildings (Settlement, Town, City, Metropolitan).",
               "Harness and carts: faster production of settlers and workers.",
               "Saddles, shields and jerkins: faster production of mounted units and of melee and archer units of the ancient and classical eras.",
               "Used by the Drapers Guild, the Equestrians Guild and Emperors Clothing."],
              ["Part of the clothing need, with wool, fur and cotton.",
               "Used up as material: harness that puts draught animals to work, forge bellows, parchment and bookbinding, and the equipment of units.",
               "Keeps once tanned. Traded in bales of hides."]),
  'French': (["Vêtements : bonheur dans les villes dotées des bâtiments essentiels (colonie, bourg, cité, métropole).",
              "Harnais et charrettes : production plus rapide des colons et des ouvriers.",
              "Selles, boucliers et pourpoints : production plus rapide des unités montées et des fantassins et archers des ères antique et classique.",
              "Ressource de la guilde des drapiers, de la guilde des écuyers et d'Emperors Clothing."],
             ["Une part du besoin de vêtements, avec la laine, la fourrure et le coton.",
              "Consommé comme matériau : harnais qui mettent les bêtes de trait au travail, soufflets de forge, parchemin et reliure, équipement des unités.",
              "Se conserve une fois tanné. Échangé en balles de peaux."]),
  'German': (["Kleidung: Zufriedenheit in Städten mit den Grundbauten (Siedlung, Kleinstadt, Stadt, Metropole).",
              "Geschirr und Karren: schnellere Produktion von Siedlern und Arbeitern.",
              "Sättel, Schilde und Wamse: schnellere Produktion berittener Einheiten sowie der Nahkämpfer und Bogenschützen der Antike und der Klassik.",
              "Rohstoff der Tuchmachergilde, der Reitergilde und von Emperors Clothing."],
             ["Ein Teil des Kleidungsbedarfs, mit Wolle, Pelz und Baumwolle.",
              "Als Material verbraucht: Geschirr, das Zugtiere an die Arbeit bringt, Blasebalge der Schmiede, Pergament und Bucheinbände, die Ausrüstung der Einheiten.",
              "Hält sich, einmal gegerbt. In Ballen von Häuten gehandelt."]),
  'Italian': (["Vestiario: felicità nelle città con gli edifici essenziali (insediamento, borgo, città, metropoli).",
               "Finimenti e carri: produzione più rapida di coloni e lavoratori.",
               "Selle, scudi e giubbe: produzione più rapida delle unità a cavallo e dei fanti e arcieri delle ere antica e classica.",
               "Risorsa della gilda dei drappieri, della gilda dei cavalieri e di Emperors Clothing."],
              ["Una parte del fabbisogno di vestiario, con lana, pelliccia e cotone.",
               "Consumato come materiale: finimenti che mettono al lavoro gli animali da tiro, mantici delle fucine, pergamena e legatoria, equipaggiamento delle unità.",
               "Si conserva una volta conciato. Commerciato in balle di pelli."]),
  'Spanish': (["Vestido: felicidad en las ciudades con los edificios esenciales (asentamiento, villa, ciudad, metrópoli).",
               "Arreos y carros: producción más rápida de colonos y trabajadores.",
               "Sillas, escudos y jubones: producción más rápida de las unidades montadas y de la infantería y los arqueros de las eras antigua y clásica.",
               "Recurso del gremio de pañeros, del gremio de jinetes y de Emperors Clothing."],
              ["Una parte de la necesidad de vestido, con lana, piel y algodón.",
               "Consumido como material: arreos que ponen a trabajar a los animales de tiro, fuelles de forja, pergamino y encuadernación, equipo de las unidades.",
               "Se conserva una vez curtido. Se comercia en balas de pieles."]),
 },
 'DAIRY': {
  'English': (["Health in every city connected to it.",
               "More food in cities with the essentials buildings (Settlement, Town, City, Metropolitan), the Cannery, the Commodity Market and the Commercial Center.",
               "Used by the Grocers Guild and Big McDowells."],
              ["Part of the variety need, with meat, fish, fruit and oil; larger with size.",
               "Spoils unless preserved: salt, then canning, then refrigeration. Cheese and butter keep.",
               "Cheese as rations for armies in the field and provisions for ships. Traded in tonnes; fresh dairy only to near partners."]),
  'French': (["Santé dans chaque ville qui y est reliée.",
              "Plus de nourriture dans les villes dotées des bâtiments essentiels (colonie, bourg, cité, métropole), de la conserverie, du marché des matières premières et du centre commercial.",
              "Ressource de la guilde des épiciers et de Big McDowells."],
             ["Une part du besoin de variété, avec la viande, le poisson, les fruits et l'huile ; croissant avec la taille.",
              "Se gâte s'il n'est pas conservé : sel, puis conserve, puis réfrigération. Le fromage et le beurre se gardent.",
              "Le fromage comme ration des armées en campagne et provision des navires. Échangé en tonnes ; le frais seulement avec des partenaires proches."]),
  'German': (["Gesundheit in jeder damit verbundenen Stadt.",
              "Mehr Nahrung in Städten mit den Grundbauten (Siedlung, Kleinstadt, Stadt, Metropole), der Konservenfabrik, dem Warenmarkt und dem Handelszentrum.",
              "Rohstoff der Krämergilde und von Big McDowells."],
             ["Ein Teil des Bedarfs an Abwechslung, mit Fleisch, Fisch, Obst und Öl; mit der Größe wachsend.",
              "Verdirbt, wenn es nicht haltbar gemacht wird: Salz, dann Konserven, dann Kühlung. Käse und Butter halten sich.",
              "Käse als Ration für Armeen im Feld und Proviant für Schiffe. In Tonnen gehandelt; Frisches nur an nahe Partner."]),
  'Italian': (["Salute in ogni città collegata.",
               "Più cibo nelle città con gli edifici essenziali (insediamento, borgo, città, metropoli), il conservificio, il mercato delle materie prime e il centro commerciale.",
               "Risorsa della gilda dei droghieri e di Big McDowells."],
              ["Una parte del fabbisogno di varietà, con carne, pesce, frutta e olio; crescente con le dimensioni.",
               "Si guastano se non conservati: sale, poi inscatolamento, poi refrigerazione. Formaggio e burro si conservano.",
               "Il formaggio come razione per gli eserciti in campo e provvista per le navi. Commerciati in tonnellate; i freschi solo con partner vicini."]),
  'Spanish': (["Salud en cada ciudad conectada.",
               "Más alimento en las ciudades con los edificios esenciales (asentamiento, villa, ciudad, metrópoli), la conservera, el mercado de materias primas y el centro comercial.",
               "Recurso del gremio de tenderos y de Big McDowells."],
              ["Una parte de la necesidad de variedad, con carne, pescado, fruta y aceite; mayor con el tamaño.",
               "Se estropean si no se conservan: sal, luego conservas, luego refrigeración. El queso y la mantequilla se conservan.",
               "El queso como ración de los ejércitos en campaña y provisión de los barcos. Se comercian en toneladas; los frescos solo con socios cercanos."]),
 },
}

ref = lambda s: ''.join(c if ord(c) < 128 else '&#%d;' % ord(c) for c in s)
def section(lang, now, later):
    h = HEAD[lang]
    b = lambda xs: ''.join('[NEWLINE][ICON_BULLET]' + ref(x) for x in xs)
    return '[NEWLINE][NEWLINE][BOLD]%s[\\BOLD]%s[NEWLINE][NEWLINE][BOLD]%s[\\BOLD]%s' % (ref(h[0]), b(now), ref(h[1]), b(later))

show = lambda f: subprocess.run(['git', '-C', mod, 'show', '%s:%s' % (base, f)], capture_output=True, check=True).stdout.decode('latin-1')
state, pairs = {}, []
for good in ['TIMBER', 'DAIRY', 'LEATHER', 'WOOL']:
    f = FILES[good]
    if f not in state: state[f] = show(f)
    s = state[f]
    i = s.index('<Tag>TXT_KEY_BONUS_%s_PEDIA</Tag>' % good)
    for lang in HEAD:
        j = s.index('</%s>' % lang, i)
        add = section(lang, *T[good][lang])
        assert '[BOLD]%s' % ref(HEAD[lang][0]) not in s[i:j], (good, lang, 'already there')
        k = 20  # shortest unique window ending at the closing tag
        while s.count(s[j - k:j + len(lang) + 3]) != 1: k += 10
        old = s[j - k:j + len(lang) + 3]
        new = s[j - k:j] + add + '</%s>' % lang
        pairs.append({'file': f, 'old': old, 'new': new})
        s = s[:j - k] + new + s[j + len(lang) + 3:]
        state[f] = s
json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes of JSON')
