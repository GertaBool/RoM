"""Civ IV Shape Lab: run in Blender 4.x with --python, or Run Script in its Text Editor.
Procedural original geometry; deliberately no downloaded/game meshes or AI service.
"""
import math,json,sys
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent))
from surface_textures import texture
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
from bpy.props import FloatProperty,FloatVectorProperty,EnumProperty,StringProperty,PointerProperty
COLLECTION='Civ IV Shape Lab'

def material(name,color,metal=0,detail=.7,wear=.25):
 m=bpy.data.materials.get('Studio '+name) or bpy.data.materials.new('Studio '+name);m.use_nodes=True;m.node_tree.nodes.clear()
 nodes=m.node_tree.nodes;links=m.node_tree.links;p=nodes.new('ShaderNodeBsdfPrincipled');out=nodes.new('ShaderNodeOutputMaterial');links.new(p.outputs['BSDF'],out.inputs['Surface']);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.68;m.diffuse_color=(*color,1)
 if name not in ('Backdrop','Face detail'):
  key='Studio painted '+name;image=bpy.data.images.get(key)
  if image:bpy.data.images.remove(image)
  image=bpy.data.images.new(key,width=512,height=512,alpha=False);pixels=texture(name,color,512,detail,wear);rgb=pixels[:,:,:3];pixels[:,:,:3]=__import__('numpy').where(rgb<=.0031308,12.92*rgb,1.055*rgb**(1/2.4)-.055);image.pixels.foreach_set(pixels.ravel());image.update();image.pack()
  node=nodes.new('ShaderNodeTexImage');node.image=image;node.interpolation='Linear';links.new(node.outputs['Color'],p.inputs['Base Color'])
 else:p.inputs['Base Color'].default_value=(*color,1)
 return m

def build(s):
 # Only replace our generated collection, leaving unrelated scene work alone.
 old=bpy.data.collections.get(COLLECTION)
 if old:
  for ob in list(old.objects):bpy.data.objects.remove(ob,do_unlink=True)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(COLLECTION);bpy.context.scene.collection.children.link(col)
 def painted(name,color,metal=0):return material(name,color,metal,s.detail,s.weathering)
 mats={'cuirass':painted('Cuirass',s.armor,.65),'cloth':painted('Cloth',s.cloth),'metal':painted('Armor',s.armor,.65),'skin':painted('Skin',s.skin),'leather':painted('Leather',(.095,.042,.022)),'trim':painted('Trim',(.58,.37,.10),.5),'wood':painted('Wood',(.23,.115,.045)),'dark':painted('Face detail',(.025,.018,.013))}
 def own(ob,name,mat):
  ob.name=name
  for c in list(ob.users_collection):c.objects.unlink(ob)
  col.objects.link(ob);ob.data.materials.clear();ob.data.materials.append(mats[mat]);return ob

 def ell(name,loc,scale,mat,segments=12,rings=8):
  bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc);o=own(bpy.context.object,name,mat);o.scale=scale;return o
 def bar(name,a,b,r1,r2,mat,vertices=10):
  a,b=Vector(a),Vector(b);bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=r1,radius2=r2,depth=(b-a).length,location=(a+b)/2);o=own(bpy.context.object,name,mat);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
 def box(name,loc,scale,mat,bevel=.025):
  bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=own(bpy.context.object,name,mat);o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  if bevel:
   m=o.modifiers.new('Soft edges','BEVEL');m.width=bevel;m.segments=1
  return o
 def torso(name,profiles,mat):
  verts=[];faces=[];count=12
  for z,rx,ry in profiles:
   for i in range(count):
    a=2*math.pi*i/count;verts.append((rx*math.cos(a),ry*math.sin(a),z))
  for j in range(len(profiles)-1):
   for i in range(count):a=j*count+i;b=j*count+(i+1)%count;faces.append((a,b,b+count,a+count))
  faces.extend([tuple(reversed(range(count))),tuple((len(profiles)-1)*count+i for i in range(count))]);mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);col.objects.link(ob);ob.data.materials.append(mats[mat]);uv=mesh.uv_layers.new(name='StudioUV')
  for polygon in mesh.polygons:
   ids=[mesh.loops[i].vertex_index for i in polygon.loop_indices];side=len(ids)==4
   for li,idx in zip(polygon.loop_indices,ids):
    point=mesh.vertices[idx].co
    if side:
     u=(idx%count)/count
     if 0 in [i%count for i in ids] and count-1 in [i%count for i in ids] and idx%count==0:u=1
     v=(point.z-profiles[0][0])/(profiles[-1][0]-profiles[0][0])
    else:u=.5+point.x/(2*max(p[1] for p in profiles));v=.5+point.y/(2*max(p[2] for p in profiles))
    uv.data[li].uv=(u,v)
  return ob
 bulk=s.bulk;h=s.height;head=s.head
 torso('Tailored tunic',[(.84,.21*bulk,.14),(1.00,.18*bulk,.13),(1.20,.22*bulk,.14),(1.42,.29*bulk,.16),(1.49,.22*bulk,.13)],'cloth')
 torso('Leather belt',[(1.035,.188*bulk,.142),(1.09,.19*bulk,.143)],'leather');box('Belt clasp',(0,-.15,1.064),(.065,.025,.055),'trim',.006)
 if s.style!='CLOTH':
  torso('Breastplate',[(1.10,.20*bulk,.15),(1.25,.24*bulk,.18),(1.43,.30*bulk,.185),(1.48,.23*bulk,.15)],'cuirass')
  torso('Armor lower rim',[(1.10,.204*bulk,.154),(1.125,.21*bulk,.158)],'trim')
  for side in [-1,1]:
   for j in range(3):box('Articulated skirt plate',(side*(.115+j*.018)*bulk,-.151,.99-j*.065),(.17*bulk,.036,.085),'metal',.012)
 bar('Neck',(0,0,1.46),(0,0,1.60),.075,.08,'skin')
 ell('Head',(0,-.008,1.70),(.13*head,.115*head,.165*head),'skin',16,12)
 ell('Nose',(0,-.118,1.695),(.025,.041,.036),'skin',8,6)
 for side in [-1,1]:
  box('Brow',(side*.052,-.113,1.738),(.065,.016,.016),'dark',.004)
  ell('Ear',(side*.132,-.005,1.70),(.022,.022,.045),'skin',8,6)
 if s.helmet!='NONE':
  ell('Helmet shell',(0,.005,1.79),(.146*head,.129*head,.105*head),'metal',16,8)
  torso('Helmet band',[(1.75,.146*head,.131*head),(1.777,.147*head,.132*head)],'trim')
  for side in [-1,1]:box('Cheek guard',(side*.118,-.041,1.683),(.035,.12,.135),'metal',.012)
  if s.helmet=='CREST':box('Helmet crest',(0,.008,1.91),(.045,.25,.16),'cloth',.025)
 a=math.radians(s.arm_angle)
 for side in [-1,1]:
  shoulder=(side*.27*bulk,0,1.425);elbow=(side*(.27*bulk+.29*math.cos(a)),0,1.425-.29*math.sin(a));hand=(side*(.27*bulk+.54*math.cos(a)),0,1.425-.54*math.sin(a))
  bar('Upper sleeve',shoulder,elbow,.103*bulk,.075*bulk,'cloth');ell('Elbow',elbow,(.077,.077,.077),'cloth');bar('Forearm',elbow,hand,.074*bulk,.047,'skin' if s.style=='CLOTH' else 'metal');ell('Hand',hand,(.055,.045,.079),'skin')
  if s.style!='CLOTH':ell('Shoulder plate',shoulder,(.145*bulk,.145,.11),'metal');ell('Shoulder rivet',(shoulder[0],-.139,shoulder[2]),(.018,.012,.018),'trim',8,6)
  hip=(side*.123,0,.94);knee=(side*(.13+s.stance*.08),0,.53);ankle=(side*(.14+s.stance*.16),0,.14)
  bar('Trouser thigh',knee,hip,.082*bulk,.112*bulk,'cloth');ell('Knee',knee,(.083,.083,.083),'cloth');bar('Boot shaft',ankle,knee,.065,.08,'leather');ell('Boot',(ankle[0],-.075,.085),(.088,.18,.085),'leather')
  if s.style=='PLATE':box('Shin plate',(ankle[0],-.065,.31),(.12,.045,.28),'metal',.018);ell('Knee guard',(knee[0],-.07,.53),(.09,.055,.085),'metal')
  if side==1 and s.weapon!='NONE':
   x,y,z=hand
   if s.weapon=='SPEAR':bar('Spear shaft',(x,y,z-.55),(x,y,z+.67),.016,.016,'wood',8);bar('Spear head',(x,y,z+.65),(x,y,z+.89),.055,0,'metal',4)
   else:
    bar('Sword grip',(x,y,z-.08),(x,y,z+.07),.025,.025,'leather',8);box('Sword guard',(x,y,z+.07),(.19,.045,.035),'trim',.008);bar('Sword blade',(x,y,z+.08),(x,y,z+.62),.045,.006,'metal',4)
  if side==-1 and s.shield:
   x,y,z=hand;shield=bar('Shield',(x,-.10,z),(x,-.15,z),.27,.27,'wood',16);bar('Shield face',(x,-.151,z),(x,-.164,z),.245,.245,'cloth',16);ell('Shield boss',(x,-.17,z),(.065,.034,.065),'metal')
 # Preserve rest pose; no false claim that this generic stance matches every donor.
 bpy.context.view_layer.update()
 for ob in col.objects:
  ob.data.transform(Matrix.Diagonal((1,1,h,1)) @ ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
  ob['civ4_original_procedural']=True
 bpy.ops.object.select_all(action='DESELECT')
 for ob in col.objects:ob.select_set(True)
 bpy.context.view_layer.objects.active=next(iter(col.objects))
 return col

class StudioShapeSettings(bpy.types.PropertyGroup):
 detail:FloatProperty(name='Painted material detail',default=.85,min=0,max=1)
 weathering:FloatProperty(name='Weathering',default=.25,min=0,max=1)
 height:FloatProperty(name='Height',default=1,min=.75,max=1.3)
 bulk:FloatProperty(name='Build',default=1,min=.7,max=1.4)
 head:FloatProperty(name='Head size',default=1,min=.85,max=1.2)
 arm_angle:FloatProperty(name='Arm rest angle',default=25,min=0,max=75,description='Match donor rest pose before transferring weights')
 stance:FloatProperty(name='Stance width',default=.1,min=0,max=1)
 style:EnumProperty(name='Armor',items=[('CLOTH','Cloth',''),('MAIL','Breastplate',''),('PLATE','Full plate','')],default='PLATE')
 helmet:EnumProperty(name='Helmet',items=[('NONE','None',''),('CAP','Cap and cheek guards',''),('CREST','Crested','')],default='CAP')
 weapon:EnumProperty(name='Weapon',items=[('NONE','None',''),('SWORD','Sword',''),('SPEAR','Spear','')],default='NONE')
 shield:bpy.props.BoolProperty(name='Shield',default=False)
 cloth:FloatVectorProperty(name='Cloth',subtype='COLOR',size=3,min=0,max=1,default=(.055,.13,.23))
 armor:FloatVectorProperty(name='Armor',subtype='COLOR',size=3,min=0,max=1,default=(.16,.205,.25))
 skin:FloatVectorProperty(name='Skin',subtype='COLOR',size=3,min=0,max=1,default=(.48,.28,.17))
 output:StringProperty(name='Output GLB',subtype='FILE_PATH',default='//studio-soldier.glb')

class STUDIO_OT_shape(bpy.types.Operator):
 bl_idname='studio.build_shape';bl_label='Build / rebuild soldier';bl_options={'REGISTER','UNDO'}
 def execute(self,context):build(context.scene.studio_shape);return {'FINISHED'}

class STUDIO_OT_export_shape(bpy.types.Operator):
 bl_idname='studio.export_shape';bl_label='Export neutral model for Art Studio'
 def execute(self,context):
  col=bpy.data.collections.get(COLLECTION);out=Path(bpy.path.abspath(context.scene.studio_shape.output))
  if not col or out.suffix.lower()!='.glb':self.report({'ERROR'},'Build a model and choose a .glb output path.');return {'CANCELLED'}
  if out.exists():self.report({'ERROR'},'Output exists. Choose a new filename.');return {'CANCELLED'}
  if not out.parent.is_dir():self.report({'ERROR'},'Output directory does not exist.');return {'CANCELLED'}
  bpy.ops.object.select_all(action='DESELECT')
  for ob in col.objects:ob.select_set(True)
  bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
  self.report({'INFO'},'Neutral GLB exported. Use Unit Model Studio with a matching donor.');return {'FINISHED'}

class STUDIO_PT_shape(bpy.types.Panel):
 bl_label='Civ IV Shape Lab';bl_idname='STUDIO_PT_shape';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='Civ IV'
 def draw(self,context):
  l=self.layout;s=context.scene.studio_shape;l.label(text='Original procedural foot-soldier geometry')
  for n in ['height','bulk','head','arm_angle','stance','style','helmet','weapon','shield','cloth','armor','skin','detail','weathering']:l.prop(s,n)
  l.operator('studio.build_shape');l.label(text='Rebuild replaces generated parts; save edits first.');l.prop(s,'output');l.operator('studio.export_shape');l.label(text='Match rest pose; automatic rig transfer is experimental.')

classes=[StudioShapeSettings,STUDIO_OT_shape,STUDIO_OT_export_shape,STUDIO_PT_shape]
def register():
 for c in classes:bpy.utils.register_class(c)
 bpy.types.Scene.studio_shape=PointerProperty(type=StudioShapeSettings)
if __name__=='__main__':
 register()
 if not bpy.app.background:
  # A fresh scene avoids the startup cube obscuring the model and preserves existing scenes.
  bpy.context.window.scene=bpy.data.scenes.new('Civ IV Shape Lab workspace')
  build(bpy.context.scene.studio_shape)
  for area in bpy.context.screen.areas:
   if area.type=='VIEW_3D':
    space=area.spaces.active;space.show_region_ui=True;space.shading.color_type='MATERIAL';space.region_3d.view_location=(0,0,1);space.region_3d.view_distance=3;space.region_3d.view_rotation=Vector((3,-5,1.6)).to_track_quat('Z','Y')
