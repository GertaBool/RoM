'use strict';
// Painted diffuse detail: deterministic, entirely local, and retained in DDS exports.
function paintBuildingFacade(ctx,w,h,style,floors,wear){
 if(!['brick','stone','timber'].includes(style)||!Number.isInteger(floors)||floors<2||floors>8||!Number.isFinite(wear)||wear<0||wear>1)throw Error('Choose a façade style, 2–8 floors and weathering from 0–1.');
 ctx.save();ctx.scale(w/384,h/512);let seed=7531;const rand=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/4294967296);
 const rect=(x,y,a,b,color)=>{ctx.fillStyle=color;ctx.fillRect(x,y,a,b);};
 rect(0,0,384,512,style==='brick'?'#574438':style==='stone'?'#817866':'#c7b995');
 const bh=style==='brick'?12:26,bw=style==='brick'?30:62;
 if(style!=='timber')for(let y=0,row=0;y<512;y+=bh,row++)for(let x=-(row%2)*bw/2;x<384;x+=bw){
  const n=rand();ctx.fillStyle=style==='brick'?`rgb(${128+n*32},${72+n*21},${48+n*17})`:`rgb(${163+n*27},${151+n*25},${123+n*24})`;ctx.fillRect(x+1,y+1,bw-2,bh-2);rect(x+2,y+1,bw-4,1,'#ffffff1c');rect(x+bw-2,y+2,1,bh-3,'#0000001c');
 }
 // Subtle plaster/masonry grain, with restrained weathering below the cornice and at ground level.
 for(let i=0;i<16000;i++){const a=.02+rand()*.055;rect(rand()*384,rand()*512,.5+rand()*1.5,.5+rand()*1.5,rand()>.5?`rgba(255,244,218,${a})`:`rgba(35,27,20,${a})`);}
 const dirt=ctx.createLinearGradient(0,0,0,512);dirt.addColorStop(0,`rgba(27,24,18,${wear*.38})`);dirt.addColorStop(.12,'#00000000');dirt.addColorStop(.72,'#00000000');dirt.addColorStop(1,`rgba(34,37,24,${wear*.5})`);rect(0,0,384,512,dirt);
 const step=440/floors,top=37;
 for(let f=0;f<floors;f++){
  const y=top+f*step;
  if(style==='timber'){
   rect(0,y-9,384,11,'#503b29');rect(0,y-9,384,2,'#8c6d48');
   for(const x of [10,126,252,366]){rect(x,y,9,step,'#503b29');rect(x,y,2,step,'#8c6d48');}
  }else{rect(0,y-10,384,8,'#b7a789');rect(0,y-10,384,2,'#e0cbaa');rect(0,y-2,384,3,'#342a2044');}
  for(let c=0;c<3;c++){
   const x=40+c*112,ww=52,hh=Math.min(step*.55,59);
   if(f===floors-1&&c===1){
    const dh=Math.min(step*.80,80);rect(x-8,512-25-dh,68,dh+6,'#c7b58f');rect(x,512-22-dh,52,dh,'#3e2d20');
    for(let k=0;k<4;k++){rect(x+3+k*12,512-20-dh,1,dh-4,'#8c6540');rect(x+5+k*12,512-18-dh,7,dh*.38,'#67492e');}rect(x+38,512-40,3,4,'#b89b52');continue;
   }
   rect(x-5,y+7,ww+10,hh+10,'#41382d88');rect(x-4,y+3,ww+8,hh+9,style==='timber'?'#786047':'#cbbc9d');
   const glass=ctx.createLinearGradient(x,y+7,x+ww,y+hh);glass.addColorStop(0,'#698185');glass.addColorStop(.45,'#34494b');glass.addColorStop(1,'#18272b');rect(x,y+8,ww,hh,glass);
   rect(x+ww/2-1,y+8,3,hh,'#b0a083');rect(x,y+8+hh*.5,ww,3,'#a5967d');rect(x+3,y+11,ww/2-6,2,'#d0d8c088');
   rect(x-7,y+hh+8,ww+14,5,'#d2c19e');rect(x-7,y+hh+13,ww+14,2,'#332c2366');
   if(wear>0){for(let k=0;k<4;k++)rect(x+rand()*ww,y+hh+15,1+rand()*2,rand()*step*.35,`rgba(42,39,28,${wear*.13})`);}
  }
 }
 if(style!=='timber')for(const x of [0,372]){rect(x,0,12,512,'#bfae8e');for(let y=0;y<512;y+=25){rect(x,y,12,2,'#6b5a45');rect(x+1,y+3,2,20,'#e4d1ac');}}
 rect(0,0,384,8,'#ded0ae');rect(0,8,384,9,'#9a896a');rect(0,17,384,4,'#30281e66');rect(0,490,384,22,'#797664');rect(0,490,384,3,'#bdb498');
 ctx.restore();
}
function paintBuildingRoof(ctx,x,y,w,h,color,pattern){
 ctx.fillStyle=color;ctx.fillRect(x,y,w,h);if(pattern==='solid')return;
 ctx.save();ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();const rows=pattern==='copper'?6:12,hh=h/rows,ww=pattern==='copper'?w/3:w/4;
 for(let r=0;r<rows;r++)for(let c=-1;c<5;c++){
  const xx=x+c*ww+(pattern==='copper'?0:r%2)*ww/2,yy=y+r*hh;ctx.fillStyle=`rgba(255,244,219,${.035+((r*7+c*3+20)%9)*.009})`;ctx.fillRect(xx+1,yy+1,ww-2,hh-2);ctx.fillStyle='#17212666';ctx.fillRect(xx,yy,ww,1);ctx.fillRect(xx,yy,1,hh);ctx.fillStyle='#fff1d02b';ctx.fillRect(xx+1,yy+hh-2,ww-2,1);
 }
 ctx.restore();
}
