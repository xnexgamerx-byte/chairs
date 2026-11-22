from mark import RED, RED_D, RED_L, INK
from dove import dove
VB="120 25 1175 665"
def mark2(theme="light", uid="a", mono=None, knock=None, bird="213628"):
    ink = INK if theme=="light" else "#F2F2F2"
    if mono:
        Z=SP=SW=mono; ENV=mono
    else:
        Z=f"url(#zg{uid})"; SP=f"url(#sp{uid})"; SW=f"url(#sw{uid})"; ENV=RED
    kn = knock or ("#ffffff" if (mono or "")!="#ffffff" else "#000000")
    g=[f"""<defs>
  <linearGradient id="zg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{RED_L}"/><stop offset=".55" stop-color="{RED}"/><stop offset="1" stop-color="{RED_D}"/></linearGradient>
  <linearGradient id="zs{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".3"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="sp{uid}" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
  <linearGradient id="sw{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ink}" stop-opacity="0"/><stop offset=".45" stop-color="{ink}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
</defs>"""]
    # speed lines left of Z
    for (x0,y0,x1,y1,w) in [(150,300,420,318,11),(120,350,400,362,14),(170,400,380,404,10),(230,448,350,448,7)]:
        g.append(f'<path d="M{x0},{y0} L{x1},{y1-w/2} L{x1},{y1+w/2} Z" fill="{SP}"/>')
    # Z
    zpts=[(345,110),(825,110),(790,205),(475,545),(765,545),(730,640),(190,640),(225,545),(330,545),(645,205),(310,205)]
    zp="M"+" L".join(f"{x},{y}" for x,y in zpts)+" Z"
    stripes="".join(f'<path d="M{x},540 L{x+18},540 L{x-8},645 L{x-26},645 Z" fill="#000"/>' for x in [262,302])
    g.append(f'<mask id="zm{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1400" height="800"><rect width="1400" height="800" fill="#fff"/>{stripes}</mask>')
    g.append(f'<path d="{zp}" fill="{Z}" mask="url(#zm{uid})"/>')
    if not mono: g.append(f'<path d="{zp}" fill="url(#zs{uid})" mask="url(#zm{uid})"/>')
    # swoosh: from under Z bottom-right sweeping up to the bird
    g.append(f'<path d="M520,685 C800,690 1010,610 1130,440 C1010,590 800,655 520,685 Z" fill="{SW}"/>')
    # bird to the right of the Z
    if bird=="213628":
        bw=480; bx,by=770,55
        rc = {"#5599ff": (mono or RED)}
        if mono: rc["#ffffff"]=kn
        g.append(dove(bird,bx,by,bw,rc))
        s=bw/502.5; beak=(bx+462*s, by+200*s)
    else:
        bw=400; bx,by=790,40
        rc={}; bf=None
        if mono=="#ffffff": rc={"#fff\"":kn+'"',"#ccc":kn,"#fc0":"#ffffff"}; bf="#ffffff"
        elif mono: rc={"#ccc":"#ffffff","#fc0":"#ffffff"}; bf=mono
        g.append(dove(bird,bx,by,bw,rc,base_fill=bf))
        s=bw/300; beak=(bx+281*s, by+189*s)
    # envelope held in beak
    ex,ey=beak[0]+10,beak[1]+32
    line = "#fff" if not mono else kn
    edge = INK if (theme=="light" and not mono) else ("#111" if not mono else kn)
    g.append(f'<g transform="translate({ex:.0f},{ey:.0f}) rotate(-8)"><rect x="-34" y="-24" width="68" height="48" rx="5" fill="{ENV}" stroke="{edge}" stroke-width="3"/><path d="M-30,-20 L0,4 L30,-20 M-30,20 L-9,1 M30,20 L9,1" fill="none" stroke="{line}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return "\n".join(g)
if __name__=="__main__":
    rows=[]
    for b in ["213628","182180"]:
        for th,bg in [("light","#fff"),("dark","#161616")]:
            rows.append(f'<svg viewBox="{VB}" width="770" height="448" style="background:{bg}">{mark2(th,uid=b+th,bird=b)}</svg>')
    open("t2.html","w").write('<html><body style="margin:0;width:1540px;display:flex;flex-wrap:wrap">'+"".join(rows)+'</body></html>')
