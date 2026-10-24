from pathlib import Path
root=Path(__file__).resolve().parent
html=(root/'app/index.html').read_text()
for name in ['core.js','app.js','resources.js','mesh.js','surfaces.js','buildings.js','units.js']:
 js=(root/'app'/name).read_text().replace('</script','<\\/script')
 html=html.replace(f'<script src="{name}"></script>','<script>\n'+js+'\n</script>')
(root/'dist').mkdir(exist_ok=True)
(root/'dist/Civ4ArtStudio.html').write_text(html)
print('Built standalone HTML:',root/'dist/Civ4ArtStudio.html')
