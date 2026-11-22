from mark import RED, INK
from dove import dove
from z3d import z3d
VB="110 0 1200 765"
VB_APP="-30 -75 1080 1080"
def mark2(theme="light", uid="a", mono=None, knock=None, bird="213628", layout="wide"):
    ink = INK if theme=="light" else "#F2F2F2"
    kn = knock or ("#ffffff" if (mono or "")!="#ffffff" else "#000000")
    SP = mono or f"url(#sp{uid})"; SW = mono or f"url(#sw{uid})"; ENV = mono or RED
    g=[f"""<defs>
  <linearGradient id="sp{uid}" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
  <linearGradient id="sw{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ink}" stop-opacity="0"/><stop offset=".45" stop-color="{ink}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
  <filter id="bs{uid}" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="6" dy="10" stdDeviation="9" flood-color="#000" flood-opacity=".35"/></filter>
</defs>"""]
    if layout=="app":
        zs,zx,zy = 1.35,-215,85
        speed=[(-10,430,300,450,14),(-30,490,270,505,17),(10,550,240,560,12),(60,605,200,610,8)]
        bw,bx,by = (590,385,-70) if bird=="213628" else (500,440,-95)
        swoosh=None
    else:
        zs,zx,zy = 1.12,-40,-30
        speed=[(130,300,400,318,12),(100,352,380,364,15),(150,404,360,408,11),(210,452,330,452,8)]
        bw,bx,by = (470,800,25) if bird=="213628" else (400,820,10)
        swoosh="M520,712 C800,716 1020,630 1150,450 C1030,610 800,682 520,712 Z"
    for (x0,y0,x1,y1,w) in speed:
        g.append(f'<path d="M{x0},{y0} L{x1},{y1-w/2} L{x1},{y1+w/2} Z" fill="{SP}"/>')
    g.append(z3d(uid, s=zs, ox=zx, oy=zy, mono=mono))
    if swoosh: g.append(f'<path d="{swoosh}" fill="{SW}"/>')
    flt = "" if mono else f' filter="url(#bs{uid})"'
    if bird=="213628":
        rc={"#5599ff": (mono or RED)}
        if mono: rc["#ffffff"]=kn
        d=dove(bird,bx,by,bw,rc); s=bw/502.5; beak=(bx+462*s, by+200*s)
    else:
        rc={}; bf=None
        if mono=="#ffffff": rc={"#fff\"":kn+'"',"#ccc":kn,"#fc0":"#ffffff"}; bf="#ffffff"
        elif mono: rc={"#ccc":"#ffffff","#fc0":"#ffffff"}; bf=mono
        d=dove(bird,bx,by,bw,rc,base_fill=bf); s=bw/300; beak=(bx+281*s, by+189*s)
    ex,ey=beak[0]+10,beak[1]+34
    line = "#fff" if not mono else kn
    edge = "#1a1a1a" if not mono else kn
    env=f'<g transform="translate({ex:.0f},{ey:.0f}) rotate(-8) scale({1.15 if layout=="app" else 1})"><rect x="-34" y="-24" width="68" height="48" rx="5" fill="{ENV}" stroke="{edge}" stroke-width="3"/><path d="M-30,-20 L0,4 L30,-20 M-30,20 L-9,1 M30,20 L9,1" fill="none" stroke="{line}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g>'
    g.append(f'<g{flt}>{d}{env}</g>')
    return "\n".join(g)
if __name__=="__main__":
    cells=[]
    for b in ["213628","182180"]:
        for th,bg in [("light","#fff"),("dark","#1B1B1B")]:
            cells.append(f'<div style="width:500px;height:500px;border-radius:110px;background:{bg};display:flex;align-items:center;justify-content:center;margin:10px;box-shadow:0 0 0 1px #ccc"><svg viewBox="{VB_APP}" width="440">{mark2(th,uid="a"+b+th,bird=b,layout="app")}</svg></div>')
    for b in ["213628","182180"]:
        cells.append(f'<svg viewBox="{VB}" width="1040" style="background:#fff;margin:10px">{mark2("light",uid="w"+b,bird=b)}</svg>')
    open("t3.html","w").write('<html><body style="margin:0;width:2100px;display:flex;flex-wrap:wrap;background:#ddd">'+"".join(cells)+'</body></html>')
