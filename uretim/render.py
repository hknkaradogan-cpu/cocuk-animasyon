import bpy, math, sys, json
from mathutils import Vector
import os
D0=os.environ.get('IS_DIR','.');TL=json.load(open(D0+'/tl.json'));SC=json.load(open(D0+'/sahneler.json'));FPS=TL['fps'];ENV=TL['env'];L=TL['tl']


def mat(name,col,rough=.5,sss=0.0,emit=0):
    m=bpy.data.materials.new(name);m.use_nodes=True;b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(*col,1);b.inputs['Roughness'].default_value=rough
    if sss: b.inputs['Subsurface Weight'].default_value=sss;b.inputs['Subsurface Radius'].default_value=(1,.4,.25)
    if emit: b.inputs['Emission Color'].default_value=(*col,1);b.inputs['Emission Strength'].default_value=emit
    return m
def emp(n,loc=(0,0,0),par=None):
    o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o);o.location=loc
    if par:o.parent=par
    return o
def sph(n,loc,sc,m,par=None,seg=40):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=seg//2,location=(0,0,0));o=bpy.context.object;o.name=n;o.scale=sc;o.location=loc;o.data.materials.append(m);bpy.ops.object.shade_smooth()
    if par:o.parent=par
    return o
def cyl(n,loc,r,h,m,par=None,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=h,vertices=40);o=bpy.context.object;o.name=n;o.location=loc;o.rotation_euler=rot;o.data.materials.append(m);bpy.ops.object.shade_smooth()
    if par:o.parent=par
    return o
def box(n,loc,sz,m,bev=.08,par=None):
    bpy.ops.mesh.primitive_cube_add();o=bpy.context.object;o.name=n;o.scale=(sz[0]/2,sz[1]/2,sz[2]/2);o.location=loc;o.data.materials.append(m)
    bpy.ops.object.transform_apply(scale=True);md=o.modifiers.new('b','BEVEL');md.width=bev;md.segments=4;bpy.ops.object.shade_smooth()
    if par:o.parent=par
    return o
bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene
skin=mat('skin',(1,.72,.58),.45,.3);hair=mat('hair',(.75,.25,.07),.4);dress=mat('dress',(1,.35,.6),.5);white=mat('w',(1,1,1),.2);dark=mat('d',(.05,.02,.01),.2)
iris=mat('i',(.35,.16,.05),.2);cheekm=mat('c',(1,.4,.45),.6);wallm=mat('wall',(1,.84,.66),.85);floorm=mat('fl',(.78,.5,.28),.45)
mouthm=mat('mo',(.45,.05,.1),.4);yel=mat('y',(1,.8,.15),.4);brown=mat('br',(.62,.38,.18),.7);bel=mat('bel',(.9,.7,.45),.7);red=mat('red',(.9,.15,.2),.4)
blue=mat('bl',(.3,.55,.95),.6);wood=mat('wd',(.55,.33,.16),.5);sofam=mat('sf',(1,.55,.4),.7);sky=mat('sky',(.7,.9,1),1,emit=.9);rug=mat('rug',(1,.55,.7),.9)
# ---- girl
G=emp('G');U=emp('U',(0,0,.5),G);H=emp('H',(0,0,1.05),U)
hip=[emp('hipL',(-.16,0,.5),G),emp('hipR',(.16,0,.5),G)]
for s,h in zip((-1,1),hip):cyl('leg',(0,0,-.2),.075,.45,skin,h);sph('shoe',(0,-.05,-.43),(.13,.2,.08),dress,h)
cone=None
bpy.ops.mesh.primitive_cone_add(radius1=.58,radius2=.26,depth=.95,vertices=64,location=(0,0,.38));cone=bpy.context.object;cone.data.materials.append(dress);bpy.ops.object.shade_smooth();cone.parent=U
sph('torso',(0,0,.5),(.27,.2,.2),dress,U)
arm=[];
for s in(-1,1):
    p=emp('sh',(s*.34,0,.55),U);cyl('arm',(0,0,-.2),.065,.45,skin,p);sph('hand',(0,0,-.45),(.09,.09,.09),skin,p);sph('sleeve',(0,0,0),(.1,.1,.1),dress,p);arm.append(p)
sph('head',(0,0,0),(.55,.5,.52),skin,H)
sph('hairb',(0,.12,.08),(.6,.5,.58),hair,H)
sph('bang',(0,-.14,.36),(.5,.3,.2),hair,H);
for s in(-1,1):
    sph('bang2',(s*.28,-.2,.28),(.26,.25,.25),hair,H)
    sph('pig',(s*.72,.05,-.12),(.22,.22,.22),hair,H);sph('bow',(s*.6,0,.12),(.13,.09,.13),yel,H);sph('ear',(s*.55,0,0),(.08,.06,.12),skin,H)
    sph('ch',(s*.33,-.4,-.13),(.1,.04,.07),cheekm,H)
eyes=[]
for s in(-1,1):
    w=sph('ew',(s*.2,-.43,.03),(.15,.07,.18),white,H);i=sph('ei',(s*.2,-.48,.03),(.1,.05,.12),iris,H);p=sph('ep',(s*.2,-.52,.03),(.055,.03,.07),dark,H);h=sph('hl',(s*.17,-.545,.09),(.03,.02,.03),white,H)
    eyes.append((w,i,p,h,s))
brows=[]
for s in(-1,1):
    b=cyl('brow',(s*.2,-.52,.24),.022,.17,hair,H,(0,math.pi/2,0));brows.append((b,s))
sph('nose',(0,-.5,-.05),(.04,.035,.035),skin,H)
mouth=sph('mouth',(0,-.49,-.2),(.11,.03,.02),mouthm,H)
# ---- bear
B=emp('B');sph('bb',(0,0,.28),(.26,.2,.28),brown,B);sph('bbel',(0,-.14,.26),(.17,.08,.18),bel,B);sph('bh',(0,0,.68),(.26,.22,.23),brown,B)
for s in(-1,1):
    sph('be',(s*.2,0,.86),(.09,.07,.09),brown,B);sph('bsn',(0,-.18,.62),(.11,.07,.08),bel,B) if s==-1 else None
    sph('bey',(s*.09,-.2,.72),(.03,.02,.035),dark,B);sph('bar',(s*.27,-.02,.3),(.09,.09,.16),brown,B);sph('bl',(s*.13,-.02,.07),(.1,.11,.09),brown,B)
sph('bno',(0,-.24,.65),(.04,.03,.03),dark,B);sph('bbow',(0,-.17,.47),(.09,.04,.04),red,B)
# ---- room
box('floor',(0,0,-.1),(40,40,.2),floorm,.01);box('wall',(0,3.6,4),(40,.2,10),wallm,.01)
box('win',(0,3.45,2.5),(2.0,.05,2.6),sky,.02);box('frm1',(0,3.4,3.85),(2.3,.1,.14),white,.02);box('frm2',(0,3.4,1.15),(2.3,.1,.14),white,.02);box('frm3',(-1.1,3.4,2.5),(.14,.1,2.6),white,.02);box('frm4',(1.1,3.4,2.5),(.14,.1,2.6),white,.02);box('frm5',(0,3.4,2.5),(.1,.1,2.6),white,.02)
bpy.ops.mesh.primitive_cylinder_add(radius=2.2,depth=.03,vertices=64,location=(0,-.3,.015));r=bpy.context.object;r.scale=(1.2,.6,1);r.data.materials.append(rug)
# bed
bx=-4.6
box('bed',(bx,1.4,.55),(3,2.2,.35),wood);box('mat',(bx,1.4,.85),(2.9,2.1,.3),blue,.12);box('pil',(bx-.9,1.9,1.1),(.9,.55,.22),white,.1);box('hb',(bx,2.6,1.2),(3,.15,1.1),wood)
for sx in(-1.35,1.35):
    for sy in(.45,2.35):box('bleg',(bx+sx,sy,.2),(.18,.18,.4),wood,.03)
# basket + toys
cyl('bask',(0,1.7,.35),.62,.7,mat('bk',(.9,.7,.35),.8));cyl('bin',(0,1.7,.72),.5,.04,dark)
for k,c in enumerate([(.9,.2,.2),(.2,.7,.3),(.2,.4,.9)]):sph('toy',(-.25+k*.25,1.7,.85),(.16,.16,.16),mat('t%d'%k,c,.5))
# sofa
sx=4.5
box('sofa',(sx,1.4,.75),(3.2,1.3,.55),sofam,.15);box('sback',(sx,2.0,1.4),(3.2,.4,1.2),sofam,.15);box('sarm1',(sx-1.5,1.4,1.05),(.4,1.3,.9),sofam,.15);box('sarm2',(sx+1.5,1.4,1.05),(.4,1.3,.9),sofam,.15);box('cush',(sx-.6,1.5,1.2),(.5,.5,.5),yel,.15)
for ax in(-1.4,1.4):
    for ay in(.9,1.9):box('slg',(sx+ax,ay,.25),(.2,.2,.5),wood,.03)
# lights
def area(loc,e,sz,tgt):
    bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=e;l.data.size=sz
    d=Vector(tgt)-Vector(loc);l.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
area((-3,-5,6),420,5,(0,0,1));area((5,-4,3),150,5,(0,0,1));area((0,2.5,3),80,6,(0,0,1))
w=bpy.data.worlds.new('w');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(1,.92,.82,1);w.node_tree.nodes['Background'].inputs[1].default_value=.5
bpy.ops.object.camera_add();CAM=bpy.context.object;sc.camera=CAM
TG=emp('tg');tc=CAM.constraints.new('TRACK_TO');tc.target=TG;tc.track_axis='TRACK_NEGATIVE_Z';tc.up_axis='UP_Y'
sc.render.engine='CYCLES';sc.cycles.samples=int(sys.argv[-3]);sc.cycles.use_denoising=True;sc.cycles.denoiser='OPENIMAGEDENOISE';sc.cycles.device='CPU'
sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.render.resolution_x=540;sc.render.resolution_y=960
# ---- animasyon (sahneler.json + tl.json'dan)
def sm(x):x=max(0,min(1,x));return x*x*(3-2*x)
def kf(t,pts):
    if t<=pts[0][0]:return pts[0][1]
    for (a,va),(b,vb) in zip(pts,pts[1:]):
        if t<=b:return va+(vb-va)*sm((t-a)/max(1e-6,b-a))
    return pts[-1][1]
TOTAL=TL['total']
for s,l in zip(SC,L):s['t0']=l['t0'];s['d']=l['d']
def mk(vals,t_start=0.0,lead=1.0):
    pts=[(t_start,vals[0][1] if False else 0)]
    return pts
def tab(fn,init,lead=1.0):
    pts=[(0.0,init)];cur=init
    for s in SC:
        v=fn(s,cur)
        if v is None:continue
        a=max(pts[-1][0]+.01,s['t0']-lead);b=max(a+.01,s['t0'])
        pts.append((a,cur));pts.append((b,v));cur=v
    pts.append((TOTAL+5,cur));return pts
PX=tab(lambda s,c:s['yer']['x'] if s['yer'] else None,0.0)
PY=tab(lambda s,c:s['yer']['y'] if s['yer'] else None,0.0)
YW=tab(lambda s,c:s['yer']['yaw'] if s['yer'] else (0.0 if s['hareket'] in('sarilma','dans','selam','say') else c),0.0,.9)
def pulses(cond,val=1.0,pre=.3,post=-.1):
    pts=[(0.0,0.0)]
    for s in SC:
        if cond(s):
            a=max(pts[-1][0]+.01,s['t0']+pre);b=max(a+.3,s['t0']+s['d']+post)
            pts+= [(a,0.0),(a+.4,val),(b,val),(b+.4,0.0)]
    pts.append((TOTAL+5,0.0));return pts
def fixp(p):
    out=[p[0]]
    for a,v in p[1:]:
        if a<=out[-1][0]:a=out[-1][0]+.01
        out.append((a,v))
    return out
LEAN=fixp(pulses(lambda s:s['egil'],.85,.9,-.1))
def bal(f,pre=-.15):return fixp(pulses(f,1.0,pre,.3))
SUR=bal(lambda s:s['duygu']=='saskin');WOR=bal(lambda s:s['duygu']=='uzgun');HAP=bal(lambda s:s['duygu']=='mutlu')
HUG_T=next((s['t0'] for s in SC if s['hareket'] in('sarilma','dans')),None)
DANCE_T=next((s['t0'] for s in SC if s['hareket']=='dans'),None)
CAMD={'yakin':(3.4,1.55),'genis':(7.2,1.15),'orta':(4.8,1.2)}
CD=[(0.0,CAMD[SC[0]['kamera']][0])];CZ=[(0.0,CAMD[SC[0]['kamera']][1])]
for s in SC[1:]:
    d,z=CAMD[s['kamera']];a=max(CD[-1][0]+.01,s['t0']-.8);b=max(a+.02,s['t0']+.2)
    CD+=[(a,CD[-1][1]),(b,d)];CZ+=[(a,CZ[-1][1]),(b,z)]
CD.append((TOTAL+5,CD[-1][1]));CZ.append((TOTAL+5,CZ[-1][1]))
def scene_at(t):
    cur=None
    for s in SC:
        if s['t0']-.2<=t:cur=s
    return cur
def pose(f):
    t=f/FPS;e=ENV[min(f,len(ENV)-1)]
    gx=kf(t,PX);gy=kf(t,PY);yaw=kf(t,YW);lean=kf(t,LEAN)
    walking=abs(kf(t+.06,PX)-kf(t-.06,PX))>.003 or abs(kf(t+.06,PY)-kf(t-.06,PY))>.003
    wk=t*9;jump=0.0
    hug=HUG_T is not None and t>HUG_T+.3
    if hug and HUG_T+.3<t<HUG_T+1.0:jump=math.sin((t-HUG_T-.3)/.7*math.pi)*.3
    dance=DANCE_T is not None and t>DANCE_T+.2
    bob=abs(math.sin(wk))*.07 if walking else math.sin(t*2.2)*.012
    G.location=(gx,gy,bob+jump-lean*.22);G.rotation_euler=(0,0,yaw);U.rotation_euler=(lean,0,0)
    for s_,h in zip((-1,1),hip):h.rotation_euler=((math.sin(wk)*.5*s_) if walking else (-lean*.5),0,0)
    aL=[0,0];aR=[0,0];sc_=scene_at(t);mv=sc_['hareket'] if sc_ and t<sc_['t0']+sc_['d']+.3 else 'bos'
    if mv=='selam':aR=[0,-(1.9+math.sin(t*10)*.25)]
    if mv=='dusun':aR=[-1.9,0];aL=[0,.2]
    if mv=='say':aL=[0,.8+math.sin(t*5)*.1];aR=[0,-.8-math.sin(t*5)*.1]
    if sc_ and sc_['egil'] and lean>.3:aL=[0,.9];aR=[0,-.9]
    if walking:aL=[math.sin(wk)*.4,.1];aR=[-math.sin(wk)*.4,-.1]
    if hug:aL=[-1.2,-.7];aR=[-1.2,.7]
    if dance:
        jump+=abs(math.sin(t*5.5))*.18;G.rotation_euler=(0,0,math.sin(t*2.75)*.5);G.location.z=jump;U.rotation_euler=(0,math.sin(t*5.5)*.12,0)
    arm[0].rotation_euler=(aL[0],aL[1],0);arm[1].rotation_euler=(aR[0],aR[1],0)
    sur=kf(t,SUR);wor=kf(t,WOR);hap=kf(t,HAP)
    if hug:hap=1.0
    for b,s_ in brows:b.location.z=.24+.06*sur+.02*hap;b.rotation_euler=(0,math.pi/2-s_*.35*wor,0)
    blink=1.0;bt=(t*1000)%3400
    if bt<150:blink=.12+.88*abs(bt-75)/75
    for w_,i_,p_,h_,s_ in eyes:
        k=blink*(1+.12*sur)*(1-.25*hap)
        for o_,base in((w_,.18),(i_,.12),(p_,.07)):o_.scale.z=base*k
        for o_ in(i_,p_):o_.location.x=s_*.2+math.sin(t*1.3)*.03
    m=e if any(l['t0']<=t<=l['t0']+l['d'] for l in L) else 0
    mouth.scale=((.09+.03*hap)+.05*m,.03,.015+.03*hap+.055*m+.02*sur);mouth.location.z=-.2-.01*wor
    H.rotation_euler=(0,0,math.sin(t*2)*.03+m*.05*math.sin(t*14))
    # ayıcık
    gizle=(HUG_T is None or t<HUG_T-.2)
    for c in B.children_recursive:c.hide_render=gizle
    if gizle:pass
    else:
        a=sm((t-HUG_T+.2)/1.0)
        if hug:B.parent=G;B.location=(0,-.42,.55);B.rotation_euler=(0,0,0)
        else:B.parent=None;B.location=(3.5,-.3-a*.5,.2+math.sin(a*math.pi)*.8);B.rotation_euler=(0,0,a*6)
    dist=kf(t,CD);tz=kf(t,CZ)
    fx=gx*(.75+.25*sm((t-(HUG_T or 1e9)+.5)/1.0)) if t>.5 else 0
    TG.location=(fx,0,tz);CAM.location=(fx,-dist,tz+.35);CAM.data.lens=35 if dist>5 else 45
a,b=int(sys.argv[-2]),int(sys.argv[-1])
import os;os.makedirs(D0+'/fr',exist_ok=True)
for f in range(a,b):
    pose(f);bpy.context.view_layer.update();sc.render.filepath=D0+'/fr/%04d.png'%f;bpy.ops.render.render(write_still=True)
