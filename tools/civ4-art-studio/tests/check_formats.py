"""Independent format checks with Pillow and Python's ZIP implementation."""
from pathlib import Path
from PIL import Image
import struct,json,zipfile,sys
out=Path(__file__).parent/'output'; checks=[]
for f in out.glob('red-*.dds'):
 im=Image.open(f).convert('RGBA'); assert im.size==(16,8)
 expected=(out/'dds-expected.bin').read_bytes(); actual=im.tobytes()
 for p in range(0,len(actual),4):
  assert actual[p:p+3]==expected[p:p+3],(f,p)
  assert abs(actual[p+3]-expected[p+3])<=8
 if 'RGBA' in f.name: assert actual==expected
 checks.append(f.name+': decoded with correct orientation, color and alpha')
assert Image.open(out/'contrast.dds').convert('RGBA').tobytes()==(out/'contrast-expected.bin').read_bytes()
checks.append('Complementary red/green DXT3 block preserves both endpoints')
im=Image.open(out/'gradient.dds').convert('RGBA');a=im.tobytes();b=(out/'gradient-expected.bin').read_bytes();mae=sum(abs(x-y) for x,y in zip(a,b))/len(a);assert mae<8,mae
checks.append(f'DXT3 gradient mean channel error {mae:.3f}/255')
assert Image.open(out/'tga-fixture.tga').convert('RGBA').tobytes()==(out/'tga-expected.bin').read_bytes()
assert Image.open(out/'rle-fixture.tga').convert('RGBA').getpixel((2,1))==(7,8,9,10)
checks.append('Uncompressed and RLE TGA decoded independently')
with zipfile.ZipFile(out/'bundle.zip') as z:
 assert z.testzip() is None
 assert z.read('édition.json')==b'{"ok":true}'
checks.append('ZIP CRC, binary payload and Unicode filename verified')
if len(sys.argv)>1:
 for n in ['GameFont.tga','GameFont_75.tga']:
  before=Image.open(Path(sys.argv[1])/n).convert('RGBA');after=Image.open(out/('edited-'+n)).convert('RGBA');assert before.size==after.size
  c=json.loads((out/('cell-'+n+'.json')).read_text());old=before.tobytes();new=after.tobytes();changed=0
  for i in range(before.width*before.height):
   p=i*4;x=i%before.width;y=i//before.width;inside=c['x']<=x<c['x']+c['width'] and c['y']<=y<c['y']+c['height']
   if not inside or old[p:p+3] in [b'\xff\x00\xff',b'\x00\xff\xff']:assert old[p:p+4]==new[p:p+4]
   if old[p:p+4]!=new[p:p+4]:changed+=1
  assert changed>0
  checks.append(n+': all external and marker RGBA pixels unchanged (Pillow check)')
(out/'independent-validation.json').write_text(json.dumps({'passed':checks,'in_game_tested':False},indent=2)+'\n')
print('\n'.join(checks))
