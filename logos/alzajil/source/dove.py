import re
import os
OC=os.path.join(os.path.dirname(os.path.abspath(__file__)),"birds")
def load(id):
    s=open([os.path.join(OC,f) for f in os.listdir(OC) if f.startswith(f"openclipart-{id}")][0]).read()
    s=re.sub(r"<\?xml.*?\?>|<!--.*?-->","",s,flags=re.S)
    s=re.sub(r"<sodipodi:namedview.*?/>","",s,flags=re.S)
    s=re.sub(r"<metadata.*?</metadata\s*>","",s,flags=re.S)
    s=re.sub(r'\s(?:inkscape|sodipodi|xmlns:\w+)[:\w-]*="[^"]*"',"",s)
    s=re.sub(r"<script.*?</script\s*>","",s,flags=re.S|re.I)
    vb=re.search(r'viewBox="([^"]+)"',s).group(1)
    inner=re.search(r"<svg\b[^>]*>(.*)</svg\s*>",s,flags=re.S).group(1)
    return vb, inner
def dove(id, x, y, w, recolor=None, flip=False, base_fill=None):
    vb, inner = load(id)
    rc=list((recolor or {}).items())
    for i,(a,b) in enumerate(rc):
        inner=re.sub(re.escape(a), f"@@{i}@@", inner, flags=re.I)
    for i,(a,b) in enumerate(rc):
        inner=inner.replace(f"@@{i}@@", b)
    if base_fill: inner=f'<g fill="{base_fill}">{inner}</g>'
    vx,vy,vw,vh=map(float,vb.split()); h=w*vh/vw
    t=f' transform="translate({2*x+w},0) scale(-1,1)"' if flip else ""
    return f'<g{t}><svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="{vb}" overflow="visible">{inner}</svg></g>'
