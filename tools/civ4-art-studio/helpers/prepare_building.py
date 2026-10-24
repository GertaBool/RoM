"""Run with Blender 4.x: blender --background --python prepare_building.py -- input.glb output_dir.
Creates a new triangulated OBJ and one baked diffuse PNG. Never saves the source file.
"""
import argparse, math, sys, json
from pathlib import Path
import bpy

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source');parser.add_argument('output');parser.add_argument('--size',type=int,choices=[256,512,1024],default=512);parser.add_argument('--triangles',type=int,default=8000)
    parser.add_argument('--simplify',action='store_true',help='Explicitly reduce geometry to the triangle budget; default preserves source geometry.')
    parser.add_argument('--allow-alpha-flatten',action='store_true',help='Explicitly accept losing cutout/transparency detail in this opaque export.')
    parser.add_argument('--allow-normal-loss',action='store_true',help='Explicitly accept omitting linked normal/bump detail from the base-color bake.')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    source=Path(args.source).resolve();out=Path(args.output).resolve()
    if not source.is_file():raise RuntimeError('Source model does not exist.')
    if not 12<=args.triangles<=20000:raise RuntimeError('Triangle target must be between 12 and 20,000.')
    out.mkdir(parents=True,exist_ok=True)
    if any((out/name).exists() for name in ['building.obj','diffuse.png','preparation.json']):raise RuntimeError('Output files already exist. Choose an empty output directory.')
    ext=source.suffix.lower()
    if ext=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        if ext in ['.glb','.gltf']:bpy.ops.import_scene.gltf(filepath=str(source))
        elif ext=='.fbx':bpy.ops.import_scene.fbx(filepath=str(source))
        elif ext=='.obj':bpy.ops.wm.obj_import(filepath=str(source),forward_axis='Y',up_axis='Z')
        else:raise RuntimeError('Supported inputs: BLEND, FBX, GLB, GLTF, OBJ. Tessellate CAD models first.')
    scene=bpy.context.scene;original=list(scene.objects);depsgraph=bpy.context.evaluated_depsgraph_get();copies=[];material_losses=[];source_parts=[]
    for ob in original:
        if ob.type!='MESH' or ob.hide_render:continue
        mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(depsgraph),preserve_all_data_layers=True,depsgraph=depsgraph)
        if not mesh.polygons:bpy.data.meshes.remove(mesh);continue
        copy=bpy.data.objects.new('Studio_'+ob.name,mesh);scene.collection.objects.link(copy);copy.matrix_world=ob.matrix_world.copy();copies.append(copy)
        old_uv=mesh.uv_layers.active.name if mesh.uv_layers.active else None
        if old_uv:mesh.uv_layers.active.name='STUDIO_SOURCE'
        if not mesh.materials:mesh.materials.append(bpy.data.materials.new('StudioDefault'))
        for i,mat in enumerate(list(mesh.materials)):
            mat=mat.copy() if mat else bpy.data.materials.new('StudioDefault');had_nodes=mat.use_nodes;mat.use_nodes=True;mesh.materials[i]=mat
            if not had_nodes:mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=mat.diffuse_color
            for shader in list(mat.node_tree.nodes):
                if shader.type=='BSDF_PRINCIPLED':
                    alpha=shader.inputs.get('Alpha');normal=shader.inputs.get('Normal')
                    if alpha and (alpha.is_linked or alpha.default_value<.999):
                        if not args.allow_alpha_flatten:raise RuntimeError('Material '+mat.name+' has alpha/transparency. This opaque exporter would lose cutout detail. Prepare an opaque source deliberately, or explicitly allow alpha flattening.')
                        material_losses.append(mat.name+': alpha flattened')
                    if normal and normal.is_linked:
                        if not args.allow_normal_loss:raise RuntimeError('Material '+mat.name+' uses a normal/bump input. A color-only bake would lose that detail. Bake the intended appearance manually, or explicitly allow normal-detail loss.')
                        material_losses.append(mat.name+': linked normal/bump detail omitted')
            for node in list(mat.node_tree.nodes):
                if node.type=='UVMAP' and old_uv and node.uv_map==old_uv:node.uv_map='STUDIO_SOURCE'
                if node.type=='TEX_IMAGE' and not node.inputs['Vector'].is_linked and old_uv:
                    uv=mat.node_tree.nodes.new('ShaderNodeUVMap');uv.uv_map='STUDIO_SOURCE';mat.node_tree.links.new(uv.outputs['UV'],node.inputs['Vector'])
    if not copies:raise RuntimeError('No visible mesh geometry was found.')
    for ob in original:bpy.data.objects.remove(ob,do_unlink=True)
    # Preserve source geometry by default. Budget reduction is opt-in and keeps small parts.
    counts=[sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in copies];source_triangles=sum(counts)
    floors=[min(n,64) for n in counts]
    if args.simplify and source_triangles>args.triangles and sum(floors)>args.triangles:raise RuntimeError('Triangle budget cannot retain the small mesh parts. Increase it or preserve the source mesh.')
    remaining=max(0,args.triangles-sum(floors));variable=sum(n-f for n,f in zip(counts,floors))
    for ob,count,floor in zip(copies,counts,floors):
        bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
        if args.simplify and source_triangles>args.triangles:
            target=floor+(count-floor)*remaining/max(1,variable)
            if target<count:
                mod=ob.modifiers.new('Explicit budget simplification','DECIMATE');mod.ratio=target/count;bpy.ops.object.modifier_apply(modifier=mod.name)
        after=sum(len(p.vertices)-2 for p in ob.data.polygons)
        if not after:raise RuntimeError('Simplification removed a whole part: '+ob.name)
        source_parts.append({'name':ob.name,'beforeTriangles':count,'afterTriangles':after})
    bpy.ops.object.select_all(action='DESELECT')
    for ob in copies:ob.select_set(True)
    bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();obj=bpy.context.object;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    mod=obj.modifiers.new('Studio triangles','TRIANGULATE');bpy.ops.object.modifier_apply(modifier=mod.name)
    if len(obj.data.polygons)>20000:raise RuntimeError('Still over 20,000 triangles; simplify further before converting.')
    bake_uv=obj.data.uv_layers.new(name='STUDIO_BAKE');obj.data.uv_layers.active_index=len(obj.data.uv_layers)-1
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.025);bpy.ops.object.mode_set(mode='OBJECT')
    image=bpy.data.images.new('StudioDiffuse',args.size,args.size,alpha=False)
    for mat in obj.data.materials:
        output=next((n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output),None)
        if not output or not output.inputs['Surface'].links:raise RuntimeError('A material has no surface shader. Bake a diffuse atlas manually.')
        shader=output.inputs['Surface'].links[0].from_node
        color=shader.inputs.get('Base Color') if shader.type=='BSDF_PRINCIPLED' else shader.inputs.get('Color') if shader.type in ['BSDF_DIFFUSE','EMISSION'] else None
        if color is None:raise RuntimeError('Mixed/group/custom surface shaders need manual base-color baking before import.')
        emission=mat.node_tree.nodes.new('ShaderNodeEmission')
        if color.links:mat.node_tree.links.new(color.links[0].from_socket,emission.inputs['Color'])
        else:emission.inputs['Color'].default_value=color.default_value
        mat.node_tree.links.new(emission.outputs[0],output.inputs['Surface'])
        node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;mat.node_tree.nodes.active=node;node.select=True
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=1;scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False;scene.render.bake.use_pass_color=True;scene.render.bake.margin=8
    bpy.ops.object.bake(type='EMIT')
    image.filepath_raw=str(out/'diffuse.png');image.file_format='PNG';image.save()
    # Export the baked UV set only, and one neutral material. Source textures are already baked.
    for layer in list(obj.data.uv_layers):
        if layer.name!='STUDIO_BAKE':obj.data.uv_layers.remove(layer)
    obj.data.uv_layers.active_index=0;obj.data.uv_layers[0].active_render=True
    obj.data.materials.clear();obj.data.materials.append(bpy.data.materials.new('StudioBaked'))
    for poly in obj.data.polygons:poly.material_index=0
    bpy.ops.wm.obj_export(filepath=str(out/'building.obj'),export_selected_objects=True,export_materials=False,export_uv=True,export_normals=True,export_triangulated_mesh=True,forward_axis='Y',up_axis='Z')
    report={'source':source.name,'sourceTriangles':source_triangles,'simplificationRequested':args.simplify,'parts':source_parts,'materialLosses':sorted(set(material_losses)),'triangles':len(obj.data.polygons),'textureSize':args.size,'upAxis':'Z','baked':'unlit base color only','notes':['Inspect the atlas and model before use. Complex procedural, emission, transparency and non-diffuse materials may need manual preparation.','Source file was not saved. Animation, lights, cameras and collision are not exported.','Preservation retains geometry, not all shader effects. Budget simplification can still change anatomy, silhouette and contacts; compare the result to the original.']}
    (out/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print('Prepared OBJ and diffuse PNG:',out)

if __name__=='__main__':main()
