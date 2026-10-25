const assert=require('node:assert/strict'),{createCiv4Core}=require('../app/core.js'),C=createCiv4Core();
function image(w,h,fn){const data=new Uint8Array(w*h*4);for(let y=0;y<h;y++)for(let x=0;x<w;x++)data.set(fn(x,y),(y*w+x)*4);return {width:w,height:h,data};}
const uniform=image(91,37,()=>[74,123,181,173]);for(const size of [[64,64],[7,3],[128,99]]){const r=C.resample(uniform,...size);for(let i=0;i<r.data.length;i++)assert.ok(Math.abs(r.data[i]-[74,123,181,173][i%4])<=1);}
const edge=image(128,64,(x)=>x<64?[255,0,0,0]:[0,0,255,255]),small=C.resample(edge,16,8);for(let p=0;p<small.data.length;p+=4)if(small.data[p+3]){assert.equal(small.data[p],0);assert.equal(small.data[p+2],255);}
const check=C.resample(image(64,64,(x,y)=>(x+y)%2?[255,255,255,255]:[0,0,0,255]),1,1);assert.ok(Math.abs(check.data[0]-188)<=1,'Average must be in linear light');
assert.deepEqual(C.resample(edge,128,64).data,edge.data);assert.throws(()=>C.resample(edge,0,5));assert.throws(()=>C.resample(edge,5,NaN));
console.log('Resampling: constant colors, alpha-edge isolation, linear-light average, identity and validation passed');
