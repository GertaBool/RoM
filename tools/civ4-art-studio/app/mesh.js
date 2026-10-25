'use strict';
function createBuildingMeshCore() {
  const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const sub=(a,b)=>a.map((v,i)=>v-b[i]);
  const normal=a=>{const len=Math.hypot(...a);if(len<1e-10)throw Error('Degenerate triangle or zero normal in the mesh.');return a.map(v=>v/len);};
  function obj(text,{up='z',flipV=true}={}) {
    if(text.length>20000000)throw Error('OBJ exceeds 20 MB. Simplify the model first.');
    const positions=[],uvs=[],normals=[],vertices=[],uv=[],ns=[],faces=[],materials=new Set();
    const index=(s,list)=>{const n=Number(s);if(!Number.isInteger(n)||!n||!s)throw Error('Missing or invalid OBJ index.');const k=n<0?list.length+n:n-1;if(k<0||k>=list.length)throw Error('OBJ index is out of range.');return list[k];};
    const rotate=p=>up==='y'?[p[0],-p[2],p[1]]:p;
    for(const raw of text.split(/\r?\n/)) {
      const line=raw.split('#')[0].trim();if(!line)continue;const [tag,...args]=line.split(/\s+/);
      if(['v','vt','vn'].includes(tag)){const count=tag==='vt'?2:3;if(args.length<count)throw Error('Incomplete OBJ coordinate.');const a=args.slice(0,count).map(Number);if(a.some(v=>!Number.isFinite(v)||Math.abs(v)>1e9))throw Error('Invalid OBJ coordinate.');(tag==='v'?positions:tag==='vt'?uvs:normals).push(a);}
      else if(tag==='usemtl')materials.add(args.join(' '));
      else if(tag==='f'){
        if(args.length!==3)throw Error('OBJ must be triangulated. Use the included Blender preparation script or triangulate before export.');
        if(faces.length>=20000)throw Error('Limit: 20,000 triangles. Simplify architectural detail for city-scale rendering.');
        const refs=args.map(a=>a.split('/')),ps=refs.map(r=>rotate(index(r[0],positions))),faceNormal=normal(cross(sub(ps[1],ps[0]),sub(ps[2],ps[0]))),base=vertices.length;
        refs.forEach((r,i)=>{const t=index(r[1],uvs);vertices.push(ps[i]);uv.push([t[0],flipV?1-t[1]:t[1]]);ns.push(r[2]?normal(rotate(index(r[2],normals))):faceNormal);});faces.push([base,base+1,base+2]);
      }
    }
    if(!faces.length)throw Error('No triangles found in the OBJ.');if(materials.size>1)throw Error('Multiple materials found. Bake them into one diffuse texture/UV atlas before import.');
    const mins=[Infinity,Infinity,Infinity],maxs=[-Infinity,-Infinity,-Infinity];for(const p of vertices)for(let i=0;i<3;i++){mins[i]=Math.min(mins[i],p[i]);maxs[i]=Math.max(maxs[i],p[i]);}
    const span=Math.max(maxs[0]-mins[0],maxs[1]-mins[1]);if(span<1e-9)throw Error('Model has no horizontal footprint. Check its up axis.');const scale=2/span;
    for(const p of vertices){p[0]=(p[0]-(mins[0]+maxs[0])/2)*scale;p[1]=(p[1]-(mins[1]+maxs[1])/2)*scale;p[2]=(p[2]-mins[2])*scale;}
    return {vertices,normals:ns,uv,faces};
  }
  function box(height=1.6) {
    if(!Number.isFinite(height)||height<0.2||height>6)throw Error('Building height must be between 0.2 and 6.');
    const vertices=[],normals=[],uv=[],faces=[];
    const quads=[ [[-1,-1,0],[1,-1,0],[1,-1,height],[-1,-1,height]], [[1,-1,0],[1,1,0],[1,1,height],[1,-1,height]], [[1,1,0],[-1,1,0],[-1,1,height],[1,1,height]], [[-1,1,0],[-1,-1,0],[-1,-1,height],[-1,1,height]], [[-1,-1,height],[1,-1,height],[1,1,height],[-1,1,height]], [[-1,1,0],[1,1,0],[1,-1,0],[-1,-1,0]] ];
    for(const [faceIndex,q] of quads.entries()){const n=normal(cross(sub(q[1],q[0]),sub(q[2],q[0]))),start=vertices.length;vertices.push(...q);normals.push(n,n,n,n);const left=faceIndex<4?0:.75,right=faceIndex<4?.75:1;uv.push([left,1],[right,1],[right,0],[left,0]);faces.push([start,start+1,start+2],[start,start+2,start+3]);}return {vertices,normals,uv,faces};
  }
  function nif(mesh,texturePath) {
    const {vertices,normals,uv,faces}=mesh;if(!vertices.length||vertices.length>65535||faces.length>20000||normals.length!==vertices.length||uv.length!==vertices.length)throw Error('Invalid mesh array sizes.');
    if(!/^Art\/[A-Za-z0-9_./-]+\.dds$/.test(texturePath)||texturePath.includes('..'))throw Error('Invalid game-relative texture path.');
    const chunks=[];const number=(v,size,method)=>{const b=new Uint8Array(size);new DataView(b.buffer)[method](0,v,true);chunks.push(b);};
    const u8=v=>number(v,1,'setUint8'),u16=v=>number(v,2,'setUint16'),u32=v=>number(v,4,'setUint32'),f32=v=>{if(!Number.isFinite(v))throw Error('Non-finite mesh coordinate.');number(v,4,'setFloat32');};
    const str=s=>{const b=new TextEncoder().encode(s);u32(b.length);chunks.push(b);},vec=a=>a.forEach(f32),ref=v=>u32(v<0?0xffffffff:v);
    const net=name=>{str(name);u32(0);ref(-1);};
    const av=(name,flags,props)=>{net(name);u16(flags);vec([0,0,0]);vec([1,0,0,0,1,0,0,0,1]);f32(1);u32(props.length);props.forEach(ref);ref(-1);};
    const types=['NiNode','NiTriShape','NiTriShapeData','NiMaterialProperty','NiTexturingProperty','NiSourceTexture'];
    chunks.push(new TextEncoder().encode('Gamebryo File Format, Version 20.0.0.4\n'));u32(0x14000004);u8(1);u32(0);u32(6);u16(6);types.forEach(str);for(let i=0;i<6;i++)u16(i);u32(0);
    av('Scene Root',8,[]);u32(1);ref(1);u32(0);
    av('Studio Building',2,[3,4]);ref(2);ref(-1);u8(0);
    u32(0);u16(vertices.length);u8(0);u8(0);u8(1);vertices.forEach(vec);u8(1);u8(0);u8(1);normals.forEach(vec);
    const center=[0,0,0];for(const p of vertices)for(let i=0;i<3;i++)center[i]+=p[i]/vertices.length;vec(center);f32(Math.max(...vertices.map(p=>Math.hypot(...sub(p,center)))));u8(0);uv.forEach(vec);u16(0x4000);ref(-1);u16(faces.length);u32(faces.length*3);u8(1);for(const face of faces)for(const i of face){if(!Number.isInteger(i)||i<0||i>=vertices.length)throw Error('Invalid triangle index.');u16(i);}u16(0);
    net('Studio Material');vec([1,1,1]);vec([1,1,1]);vec([0,0,0]);vec([0,0,0]);f32(0);f32(1);
    net('');u32(2);u32(7);u8(1);ref(5);u32(3);u32(2);u32(0);u8(0);for(let i=0;i<6;i++)u8(0);u32(0);
    net('');u8(1);str(texturePath);ref(-1);u32(6);u32(1);u32(0);u8(1);u8(1);
    u32(1);ref(0);
    const result=new Uint8Array(chunks.reduce((n,c)=>n+c.length,0));let p=0;for(const c of chunks){result.set(c,p);p+=c.length;}return result;
  }
  return {obj,box,nif};
}
if(typeof module!=='undefined')module.exports=createBuildingMeshCore;
