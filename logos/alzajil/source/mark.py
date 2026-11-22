import math
RED="#E54839"; RED_D="#B8291B"; RED_L="#F2604A"
INK="#232323"; GRAY="#8C8C8C"

def feather(base1, base2, tip, bulge=0.18):
    # tapered feather from two base points to a tip, slightly curved
    (x1,y1),(x2,y2),(tx,ty)=base1,base2,tip
    mx,my=(x1+x2)/2,(y1+y2)/2
    dx,dy=tx-mx,ty-my; L=math.hypot(dx,dy); nx,ny=-dy/L,dx/L
    c1=(x1+(tx-x1)*0.55+nx*L*bulge*0.3, y1+(ty-y1)*0.55+ny*L*bulge*0.3)
    c2=(x2+(tx-x2)*0.55-nx*L*bulge*0.15, y2+(ty-y2)*0.55-ny*L*bulge*0.15)
    # rounded tip: two points either side of tip
    r=9; ax,ay=tx+nx*r,ty+ny*r; bx,by=tx-nx*r,ty-ny*r
    return (f"M{x1:.1f},{y1:.1f} Q{c1[0]:.1f},{c1[1]:.1f} {ax:.1f},{ay:.1f} "
            f"A{r},{r} 0 0 0 {bx:.1f},{by:.1f} Q{c2[0]:.1f},{c2[1]:.1f} {x2:.1f},{y2:.1f} Z")

def mark(theme="light", uid="a", mono=None, knock=None):
    """theme: light (on white) / dark (on charcoal). mono: None, '#000', '#fff'"""
    if mono:
        zfill=mono; dove=("none" if False else mono); acc=mono
    ink = INK if theme=="light" else "#F2F2F2"
    stroke = INK if theme=="light" else "#1a1a1a"
    g=[]
    d=f"""<defs>
  <linearGradient id="zg{uid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{RED_L}"/><stop offset=".55" stop-color="{RED}"/><stop offset="1" stop-color="{RED_D}"/></linearGradient>
  <linearGradient id="zs{uid}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="sp{uid}" x1="1" y1="0" x2="0" y2="0">
    <stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
  <linearGradient id="sw{uid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ink}" stop-opacity="0"/><stop offset=".35" stop-color="{ink}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
  <linearGradient id="dv{uid}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D9D9D9"/></linearGradient>
</defs>"""
    g.append(d)
    if mono:
        Z=mono; SP=mono; SW=mono; DV="none"
    else:
        Z=f"url(#zg{uid})"; SP=f"url(#sp{uid})"; SW=f"url(#sw{uid})"; DV=f"url(#dv{uid})"
    # swoosh (behind)
    g.append(f'<path d="M470,70 C650,10 900,20 950,150 C990,260 900,380 770,470 C870,370 920,260 880,175 C830,75 660,55 470,70 Z" fill="{SW}"/>')
    # Z
    zpts=[(345,110),(825,110),(790,205),(475,545),(765,545),(730,640),(190,640),(225,545),(330,545),(645,205),(310,205)]
    zp="M"+" L".join(f"{x},{y}" for x,y in zpts)+" Z"
    stripes="".join(f'<path d="M{x},540 L{x+18},540 L{x-8},645 L{x-26},645 Z" fill="#000"/>' for x in [262,302])
    g.append(f'<mask id="zm{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="700"><rect width="1000" height="700" fill="#fff"/>{stripes}</mask>')
    g.append(f'<path d="{zp}" fill="{Z}" mask="url(#zm{uid})"/>')
    if not mono:
        g.append(f'<path d="{zp}" fill="url(#zs{uid})" mask="url(#zm{uid})"/>')
    # old-logo style stripes on bottom bar (cut in background color)
    cut = "#ffffff" if theme=="light" else "#161616"
    if mono: cut = knock or ("#ffffff" if mono!="#ffffff" else "#000000")
    # speed lines
    for (x0,y0,x1,y1,w) in [(120,300,470,330,10),(90,350,470,372,13),(140,400,470,410,10),(200,445,470,445,7)]:
        g.append(f'<path d="M{x0},{y0} L{x1},{y1-w/2} L{x1},{y1+w/2} Z" fill="{SP}"/>')
    # wing feathers
    base1=(615,325); base2=(585,395)
    tips=[(235,105),(245,165),(275,222),(330,275),(405,320)]
    sty = f'stroke="{stroke}" stroke-width="5" stroke-linejoin="round"'
    if mono: sty=f'stroke="{cut}" stroke-width="6" stroke-linejoin="round"'
    for i,t in enumerate(tips):
        fill = DV if i%2==0 else ("#EFEFEF" if not mono else mono)
        if mono: fill=mono
        g.append(f'<path d="{feather(base1,base2,t)}" fill="{fill}" {sty}/>')
    # wing covert
    g.append(f'<path d="M690,318 C650,245 555,195 450,185 C500,245 540,320 555,400 C610,380 660,350 690,318 Z" fill="{DV if not mono else mono}" {sty}/>')
    # body
    body="M805,318 L772,300 C766,278 746,268 728,272 C705,277 690,295 680,312 C640,360 560,400 470,420 L355,452 L382,468 L325,492 L405,482 C505,470 605,450 682,410 C742,380 770,348 774,326 Z"
    g.append(f'<path d="{body}" fill="{DV if not mono else mono}" {sty}/>')
    # beak
    g.append(f'<path d="M774,301 L812,316 L775,326 Z" fill="{"#F2A93B" if not mono else mono}" {sty.replace("5","3")}/>')
    eye = "#111" if not mono else cut
    g.append(f'<circle cx="742" cy="292" r="6" fill="{eye}"/>')
    # envelope
    ex,ey=840,330
    env_fill = RED if not mono else mono
    env_line = "#fff" if not mono else cut
    g.append(f'<g transform="translate({ex},{ey}) rotate(-12)"><rect x="-40" y="-28" width="80" height="56" rx="5" fill="{env_fill}" stroke="{stroke if not mono else cut}" stroke-width="4"/><path d="M-36,-24 L0,4 L36,-24 M-36,24 L-10,0 M36,24 L10,0" fill="none" stroke="{env_line}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return "\n".join(g)

if __name__=="__main__":
    for th,bg in [("light","#ffffff"),("dark","#161616")]:
        open(f"t_{th}.html","w").write(f'<html><body style="margin:0;background:{bg}"><svg viewBox="0 0 1000 700" width="1000" height="700">{mark(th)}</svg></body></html>')
