import math
ZPTS=[(345,110),(825,110),(790,205),(475,545),(765,545),(730,640),(190,640),(225,545),(330,545),(645,205),(310,205)]
def _isect(p1,d1,p2,d2):
    den=d1[0]*d2[1]-d1[1]*d2[0]
    if abs(den)<1e-9: return p2
    t=((p2[0]-p1[0])*d2[1]-(p2[1]-p1[1])*d2[0])/den
    return (p1[0]+d1[0]*t, p1[1]+d1[1]*t)
def inset(pts, d):
    n=len(pts); lines=[]
    for i in range(n):
        a=pts[i]; b=pts[(i+1)%n]; dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy)
        nx,ny=-dy/L,dx/L  # inward for clockwise (screen) polygon
        lines.append(((a[0]+nx*d,a[1]+ny*d),(dx,dy)))
    return [_isect(*lines[i-1],*lines[i]) for i in range(n)]
def hull(pts):
    pts=sorted(set(pts))
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def tf(pts,s,ox,oy): return [(x*s+ox,y*s+oy) for x,y in pts]
def P(pts): return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)+" Z"
def mix(c1,c2,t):
    a=[int(c1[i:i+2],16) for i in (1,3,5)]; b=[int(c2[i:i+2],16) for i in (1,3,5)]
    return "#"+"".join(f"{round(a[i]+(b[i]-a[i])*t):02x}" for i in range(3))
def z3d(uid, s=1.0, ox=0, oy=0, mono=None, depth=22, bevel=16,
        face=("#F2604A","#E54839","#B8291B"), side="#7E1A10", hi="#FF9A86", lo="#8E1F13", cut_x=(262,302)):
    pts=tf(ZPTS,s,ox,oy); inn=inset(pts,bevel*s)
    g=[]
    if mono:
        side=mix(mono,"#000000",.35) if mono!="#ffffff" else "#d9d9d9"
        hi=mix(mono,"#ffffff",.35); lo=mix(mono,"#000000",.4) if mono!="#ffffff" else "#c4c4c4"
    g.append(f'''<defs><linearGradient id="zf{uid}" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{mono or face[0]}"/><stop offset=".55" stop-color="{mono or face[1]}"/><stop offset="1" stop-color="{mono or face[2]}"/></linearGradient>
<linearGradient id="zh{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="zsh{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{10*s:.1f}"/></filter></defs>''')
    tx,ty=depth*0.55*s,depth*s
    def sw(x):
        q=tf([(x,535),(x+18,535),(x-8,650),(x-26,650)],s,ox,oy)
        return P(hull(q+[(a+tx,b+ty) for a,b in q]))
    stripes="".join(sw(x) for x in cut_x)
    big=f"M-2000,-2000 H4000 V4000 H-2000 Z"
    g.append(f'<mask id="zm{uid}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="6000" height="6000"><rect x="-2000" y="-2000" width="6000" height="6000" fill="#fff"/><path d="{stripes}" fill="#000"/></mask>')
    g.append(f'<g mask="url(#zm{uid})">')
    # soft shadow
    if not mono:
        g.append(f'<path d="{P(pts)}" transform="translate({depth*0.9*s:.1f},{depth*1.6*s:.1f})" fill="#000" opacity=".28" filter="url(#zsh{uid})"/>')
    # extrusion
    steps=int(depth)
    for k in range(steps,0,-1):
        t=k/steps
        g.append(f'<path d="{P(pts)}" transform="translate({depth*0.55*s*t:.1f},{depth*s*t:.1f})" fill="{mix(side,"#000000",.25*t) if not mono or mono!="#ffffff" else side}"/>')
    # bevel facets
    n=len(pts); L=(-0.55,-0.83)
    for i in range(n):
        a,b=pts[i],pts[(i+1)%n]; ia,ib=inn[i],inn[(i+1)%n]
        dx,dy=b[0]-a[0],b[1]-a[1]; l=math.hypot(dx,dy); ox_,oy_=dy/l,-dx/l
        k=ox_*L[0]+oy_*L[1]  # -1..1
        col = mix(mono or face[1], hi, k) if k>0 else mix(mono or face[1], lo, -k)
        g.append(f'<path d="{P([a,b,ib,ia])}" fill="{col}" stroke="{col}" stroke-width=".6"/>')
    # front face
    g.append(f'<path d="{P(inn)}" fill="url(#zf{uid})"/>')
    if not mono: g.append(f'<path d="{P(inn)}" fill="url(#zh{uid})"/>')
    g.append('</g>')
    return "\n".join(g)
if __name__=="__main__":
    h=f'<svg viewBox="100 60 800 650" width="800" height="650" style="background:#fff">{z3d("t")}</svg><svg viewBox="100 60 800 650" width="800" height="650" style="background:#161616">{z3d("u")}</svg>'
    open("z3.html","w").write(f'<html><body style="margin:0;display:flex">{h}</body></html>')
