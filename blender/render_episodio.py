import bpy, math, os
from mathutils import Vector
OUT=os.environ.get("OUTPUT","episodio-01-base.mp4")
FPS=int(os.environ.get("FPS","15")); W=int(os.environ.get("WIDTH","540")); H=int(os.environ.get("HEIGHT","960")); SECS=60
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
def material(n,c,rough=.5):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*c,1); m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value=rough; return m
red=material("Morango",(.8,.025,.06)); green=material("Folhas",(.08,.35,.1)); white=material("Olhos",(.95,.9,.8)); black=material("Pupilas",(.01,.01,.02)); pink=material("Roupa simples",(.75,.38,.42)); wine=material("Vestido vinho",(.3,.01,.06)); gold=material("Abacaxi",(.95,.48,.04)); suit=material("Terno",(.04,.05,.08)); floor=material("Palco",(.045,.05,.08))
def sphere(n,loc,scale,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=loc); o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(ma)
 for p in o.data.polygons:p.use_smooth=True
 return o
def cube(n,loc,scale,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma);be=o.modifiers.new("Bordas","BEVEL");be.width=.08;be.segments=3;return o
def fruitgirl(n,x,cloth):
 sphere(n+" corpo",(x,0,1.1),(.66,.52,.8),red)
 for i in range(6):
  a=i*math.tau/6;sphere(n+" folha",(x+.18*math.cos(a),0,1.82),(.12,.1,.3),green)
 for dx in [-.22,.22]:
  sphere(n+" olho",(x+dx,-.49,1.25),(.15,.07,.18),white);sphere(n+" pupila",(x+dx,-.55,1.25),(.065,.035,.1),black)
 cube(n+" vestido",(x,0,.42),(.85,.45,.9),cloth)
 for dx in [-.23,.23]:
  sphere(n+" perna",(x+dx,0,-.02),(.12,.14,.3),red)
  sphere(n+" sapato",(x+dx,-.06,-.29),(.2,.27,.1),wine)
def pineapple(x):
 sphere("Abacaxi",(x,0,1.2),(.72,.58,.95),gold)
 for i in range(7):
  a=i*math.tau/7
  bpy.ops.mesh.primitive_cone_add(vertices=16,radius1=.19,radius2=.01,depth=.7,location=(x+.16*math.cos(a),0,2.05),rotation=(.2*math.sin(a),.2*math.cos(a),0));bpy.context.object.data.materials.append(green)
 for dx in [-.24,.24]:
  sphere("Olho",(x+dx,-.52,1.4),(.15,.07,.17),white);sphere("Pupila",(x+dx,-.58,1.4),(.06,.03,.09),black)
 cube("Paleto",(x,0,.48),(.95,.3,.85),suit)
# 7 mini-palcos horizontais, câmera percorre cada um
xs=[-18,-12,-6,0,6,12,18]
cube("Chao",(0,1,-.55),(48,14,.3),floor)
for i,x in enumerate(xs):
 cube("Parede",(x,2,2.6),(7,.3,6),material("Fundo"+str(i),(.10+.025*i,.07,.11+.02*i)),)
 if i in [0,2,4,6]:
  fruitgirl("Moranguinha"+str(i),x-.2,wine if i==4 else pink)
 elif i in [1,5]:
  fruitgirl("Moranguinha"+str(i),x-1,wine if i==5 else pink);pineapple(x+1)
 else:
  fruitgirl("Moranguinha descoberta",x-.5,pink)
  cube("Foto ou objeto",(x+1,-.2,1.5),(1.6,.1,1.2),gold)
# luzes e câmera
for x in xs:
 bpy.ops.object.light_add(type="AREA",location=(x,-5,6));l=bpy.context.object;l.data.energy=850;l.data.shape="DISK";l.data.size=5
bpy.ops.object.camera_add(location=(xs[0],-17,3.2));cam=bpy.context.object;cam.data.type="ORTHO";cam.data.ortho_scale=7.6
target=bpy.data.objects.new("Alvo",None);bpy.context.collection.objects.link(target)
con=cam.constraints.new("TRACK_TO");con.target=target;con.track_axis="TRACK_NEGATIVE_Z";con.up_axis="UP_Y"
bpy.context.scene.camera=cam
frames=FPS*SECS
for i,x in enumerate(xs):
 f=1+i*(frames-1)//7;target.location=(x,0,1.35);target.keyframe_insert(data_path="location",frame=f)
 cam.location=(x,-17,3.2);cam.keyframe_insert(data_path="location",frame=f)
# suavizar curvas
for ob in [cam,target]:
 if ob.animation_data:
  for fc in ob.animation_data.action.fcurves:
   for k in fc.keyframe_points:k.interpolation="BEZIER"
sc=bpy.context.scene;sc.render.engine="BLENDER_EEVEE_NEXT";sc.eevee.taa_render_samples=16
sc.render.resolution_x=W;sc.render.resolution_y=H;sc.render.resolution_percentage=100;sc.render.fps=FPS;sc.frame_start=1;sc.frame_end=frames
sc.render.image_settings.file_format="FFMPEG";sc.render.ffmpeg.format="MPEG4";sc.render.ffmpeg.codec="H264";sc.render.filepath=OUT
sc.world.color=(.035,.035,.05);sc.view_settings.view_transform="Standard";sc.camera=cam
os.makedirs(os.path.dirname(OUT) or ".",exist_ok=True)
print("START_RENDER",OUT,flush=True);bpy.ops.render.render(animation=True);print("RENDER_FINISHED",flush=True)
