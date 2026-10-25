const assert=require('assert'),fs=require('fs'),path=require('path'),M=require('../app/mesh.js')();
const sample='v 0 0 0\nv 2 0 0\nv 0 0 2\nvt 0 0\nvt 1 0\nvt 0 1\nf 1/1 2/2 3/3\n';
const m=M.obj(sample);assert.equal(m.faces.length,1);assert.deepEqual(m.uv[0],[0,1]);assert.deepEqual(M.obj(sample.replace('1/1 2/2 3/3','-3/-3 -2/-2 -1/-1')).vertices,m.vertices);
assert.throws(()=>M.obj(sample.replace('f 1/1 2/2 3/3','f 1 2 3')),/Missing/);
assert.throws(()=>M.obj(sample.replace('f 1/1 2/2 3/3','f 1/1 2/2 3/3 1/1')),/triangulated/);
assert.throws(()=>M.obj(sample+'usemtl first\nusemtl second'),/Multiple materials/);
assert.throws(()=>M.obj(sample.replace('v 2 0 0','v NaN 0 0')),/Invalid/);
assert.throws(()=>M.obj(sample.replace('3/3','9/3')),/range/);
const box=M.box();assert.equal(box.faces.length,12);for(const n of box.normals)assert(Math.abs(Math.hypot(...n)-1)<1e-6);
for(const f of box.faces){const a=box.vertices[f[0]],b=box.vertices[f[1]],c=box.vertices[f[2]],u=b.map((v,i)=>v-a[i]),v=c.map((x,i)=>x-a[i]),cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],n=box.normals[f[0]];assert(cross.reduce((s,x,i)=>s+x*n[i],0)>0);}
assert.throws(()=>M.nif(box,'../../bad.dds'),/Invalid/);
const out=path.join(__dirname,'output');fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'mesh-box.nif'),M.nif(box,'Art/Structures/Buildings/Studio/Test/diffuse.dds'));
fs.writeFileSync(path.join(out,'mesh-obj.nif'),M.nif(m,'Art/Structures/Buildings/Studio/Test/diffuse.dds'));
if(process.argv[2]){const prepared=M.obj(fs.readFileSync(process.argv[2],'utf8'));fs.writeFileSync(path.join(out,'mesh-blender.nif'),M.nif(prepared,'Art/Structures/Buildings/Studio/Test/diffuse.dds'));assert(prepared.faces.length>0);}
console.log('Mesh tests passed: OBJ indices, axes/UVs, invalid geometry/material rejection, box winding, NIF export.');
