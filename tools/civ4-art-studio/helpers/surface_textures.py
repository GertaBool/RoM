"""Deterministic painted diffuse materials. NumPy only; usable inside Blender.
Features are in diffuse color so the Civ IV bake retains them without PBR shaders.
"""
import numpy as np

def texture(kind,color,size=512,detail=.7,wear=.25):
 if size not in (128,256,512,1024):raise ValueError('Use a power-of-two texture size from 128 to 1024.')
 if not 0<=detail<=1 or not 0<=wear<=1:raise ValueError('Detail and weathering must be 0–1.')
 color=np.asarray(color,dtype=float)
 if color.shape!=(3,) or not np.all(np.isfinite(color)) or np.any(color<0) or np.any(color>1):raise ValueError('Use three finite color values in 0–1.')
 y,x=np.mgrid[0:size,0:size];u=x/size;v=y/size
 rng=np.random.default_rng(431)
 def noise(grid):
  a=rng.random((grid,grid));gx=u*grid;gy=v*grid;ix=gx.astype(int);iy=gy.astype(int);fx=gx-ix;fy=gy-iy;fx=fx*fx*(3-2*fx);fy=fy*fy*(3-2*fy)
  return (a[iy%grid,ix%grid]*(1-fx)*(1-fy)+a[iy%grid,(ix+1)%grid]*fx*(1-fy)+a[(iy+1)%grid,ix%grid]*(1-fx)*fy+a[(iy+1)%grid,(ix+1)%grid]*fx*fy)-.5
 broad=noise(8);grain=noise(64);fine=rng.random((size,size))-.5
 tone=1+detail*(.22*broad+.07*grain+.018*fine);tint=np.zeros((size,size,3))
 edge=np.minimum.reduce([u,1-u,v,1-v]);border=np.exp(-edge*110)
 k=kind.lower()
 if k=='cloth':
  weave=(np.sin(u*2*np.pi*64)*np.sin(v*2*np.pi*64))*.055
  folds=.18*np.cos(u*2*np.pi*4)+.065*np.sin(v*2*np.pi*3)
  stitch=(np.abs(v-.06)<.0025)|(np.abs(v-.94)<.0025)
  stitch=stitch & ((u*100%1)<.55)
  tone+=detail*(weave+folds-.18*border+.20*stitch)
 elif k in ('armor','trim','cuirass'):
  tone+=detail*(.18*np.sin(u*2*np.pi)+.10*np.sin(u*2*np.pi*3)+.04*np.sin(u*2*np.pi*123)+.28*border)
  # Thin, sparse wear marks, with broad tarnish so detail survives downsampling.
  scratches=(fine>.493)&(grain>.02);tone+=wear*(scratches*.5-.32*np.maximum(0,broad*2))
  tint[:,:,0]+=wear*np.maximum(0,broad)*.07;tint[:,:,2]-=wear*np.maximum(0,broad)*.05
 elif k=='leather':
  pores=np.maximum(0,grain-.12)*.45;tone+=detail*(-pores+.16*border+.05*np.sin(v*2*np.pi*9))
  stitches=((np.abs(u-.07)<.003)|(np.abs(u-.93)<.003))&((v*45%1)<.48);tone+=detail*stitches*.5
 elif k=='wood':
  lines=np.sin((u*26+broad*.6)*2*np.pi);tone+=detail*(lines*.13+.07*np.sin((u*51+grain*.1)*2*np.pi))
 elif k=='skin':
  tone=1+detail*(.06*broad+.018*grain);tint[:,:,0]=detail*broad*.025
 elif k=='face detail':tone=np.ones_like(u)
 else:tone+=detail*.08*broad
 tone-=wear*(.15*np.maximum(0,grain)+.08*(1-v))
 rgb=np.clip(color[None,None,:]*tone[:,:,None]+tint,0,1)
 if k=='cloth':
  band=((np.abs(v-.085)<.012)|(np.abs(v-.915)<.012)).astype(float)*detail*.8
  rgb=rgb*(1-band[:,:,None])+np.array([.43,.30,.13])[None,None,:]*band[:,:,None]
 if k=='cuirass':
  diamond=np.abs(u-.75)/.065+np.abs(v-.61)/.16
  border=(diamond>.78)&(diamond<1)
  stem=(np.abs(u-.75)<.006)&(np.abs(v-.61)<.11)
  emblem=(border|stem).astype(float)*detail
  rgb=rgb*(1-emblem[:,:,None])+np.array([.64,.43,.15])[None,None,:]*emblem[:,:,None]
 result=np.ones((size,size,4),dtype=np.float32);result[:,:,:3]=rgb;return result
