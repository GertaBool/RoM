"""Audit loose unit art referenced by mod XML, including optional modules. No game rendering."""
import sys,json,hashlib,collections,statistics
from pathlib import Path
from unit_model_studio import catalog
from unit_model_convert import load_nif,dependencies

def audit(mod):
 root=Path(mod).resolve();rows=catalog(root);files={p.relative_to(root).as_posix().lower():p for p in (root/'Assets').rglob('*') if p.is_file()};N,_,Image=dependencies();results=[];errors=[];cache={}
 for filename in sorted(set(r['file'] for r in rows)):
  p=Path(filename)
  try:
   d=load_nif(p);blocks=list(d.get_global_iterator());meshes=[x for x in blocks if isinstance(x,N.NiGeometry) and x.data and hasattr(x.data,'get_triangles')];tex=[]
   for x in blocks:
    if not isinstance(x,N.NiTexturingProperty) or not x.has_base_texture or not x.base_texture.source:continue
    path=x.base_texture.source.file_name.decode('utf-8','replace').replace('\\','/');candidates=[('Assets/'+path).lower(),(p.parent.relative_to(root)/Path(path).name).as_posix().lower()];f=next((files[k] for k in candidates if k in files),None)
    item={'reference':path,'resolved':bool(f)}
    if f:
     if str(f) not in cache:
      try:
       with Image.open(f) as im:
        rgba=im.convert('RGBA');cache[str(f)]={'size':list(im.size),'alphaRange':list(rgba.getchannel('A').getextrema()),'path':f.relative_to(root).as_posix()}
      except Exception as e:cache[str(f)]={'error':str(e),'path':f.relative_to(root).as_posix()}
     item.update(cache[str(f)])
    tex.append(item)
   results.append({'path':p.relative_to(root).as_posix(),'artTypes':[r['type'] for r in rows if r['file']==filename],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'meshes':[{'name':x.name.decode('utf-8','replace'),'vertices':int(x.data.num_vertices),'triangles':len(x.data.get_triangles()),'skinned':bool(x.skin_instance),'uvSets':int(x.data.num_uv_sets)} for x in meshes],'storedTriangles':sum(len(x.data.get_triangles()) for x in meshes),'alphaProperties':sum(isinstance(x,N.NiAlphaProperty) for x in blocks),'diffuseTextures':tex})
  except Exception as e:errors.append({'path':p.relative_to(root).as_posix(),'error':str(e)})
 sizes=collections.Counter(tuple(v['size']) for v in cache.values() if 'size' in v)
 return {'scope':'Distinct loose NIFs with a KFM string referenced by UnitArtInfo, including optional modules; base-game/FPK-only assets excluded. Stored geometry includes possible alternate meshes/LODs and is not an active draw-call budget.','artDefinitions':len(rows),'models':results,'errors':errors,'summary':{'parsedModels':len(results),'modelsWithAlphaProperties':sum(bool(r['alphaProperties']) for r in results),'resolvedUniqueDiffuseTextures':len(cache),'textureSizes':{f'{w}x{h}':n for (w,h),n in sorted(sizes.items())},'texturesWithNonOpaqueAlpha':sum(v.get('alphaRange',[255,255])[0]<255 for v in cache.values()),'storedTriangleMedian':statistics.median(r['storedTriangles'] for r in results)}}
if __name__=='__main__':
 r=audit(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['summary'],indent=2));print('Parse failures:',len(r['errors']))
