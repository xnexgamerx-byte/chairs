import re, os
from mark import RED, INK
from mark2 import mark2, VB
import sys
BIRD=sys.argv[1] if len(sys.argv)>1 else "213628"
def mark(theme, uid="a", mono=None, knock=None): return mark2(theme, uid=uid, mono=mono, knock=knock, bird=BIRD)
F="/tmp/claude-0/-home-user-chairs/24d548da-cbc8-56d1-8600-369a1f297ef8/scratchpad/fonts"
AL=f"{F}/fontsource-alexandria-5.3.0/files"; CA=f"{F}/fontsource-cairo-5.3.0/files"
def icon(name):
    s=open(f"{F}/lucide/package/icons/{name}.svg").read()
    return "".join(re.findall(r"<(?:path|circle)[^>]*/>", s))
CSS=f"""
@font-face{{font-family:Alex;font-weight:900;src:url(file://{AL}/alexandria-arabic-900-normal.woff2)}}
@font-face{{font-family:Alex;font-weight:700;src:url(file://{AL}/alexandria-arabic-700-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:700;src:url(file://{CA}/cairo-arabic-700-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent}}
.lat{{font-family:'Inter Display','Inter',sans-serif;font-weight:600}}
"""
def icons_row(col, line, size=104):
    ic=lambda n:f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{icon(n)}</svg>'
    bar=f'<span style="width:4px;height:{int(size*.8)}px;background:{col};border-radius:2px"></span>'
    ln=lambda d:f'<span style="flex:1;height:3px;background:linear-gradient(to {d},{line},transparent)"></span>'
    return f'<div style="display:flex;align-items:center;gap:44px;width:100%">{ln("left")}{ic("truck")}{bar}{ic("globe")}{bar}{ic("handshake")}{ln("right")}</div>'

def full(theme, mono=None, bg=None, W=1600, H=1750, knock=None):
    ink = mono or (INK if theme=="light" else "#F4F4F4")
    acc = mono or RED
    sub = mono or ("#7A7A7A" if theme=="light" else "#BDBDBD")
    lines = mono or RED
    m = mark(theme, uid=theme+(mono or ""), mono=mono, knock=knock)
    bgcss = f"background:{bg};" if bg else ""
    return f"""<html><head><style>{CSS}</style></head><body style="width:{W}px;height:{H}px;{bgcss}">
<div style="width:{W}px;height:{H}px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 170px">
 <svg viewBox="{VB}" width="1180" style="margin-bottom:-6px">{m}</svg>
 <div dir="rtl" style="font-family:Alex;font-weight:900;font-size:200px;line-height:1.3;white-space:nowrap;color:{ink}">شركة <span style="color:{acc}">الزاجل</span></div>
 <div style="display:flex;align-items:center;gap:36px;width:100%;margin-top:6px">
   <span style="flex:1;height:4px;background:linear-gradient(to left,{lines},transparent)"></span>
   <span class="lat" style="font-size:70px;letter-spacing:10px;color:{ink}">AL-ZAJIL COMPANY</span>
   <span style="flex:1;height:4px;background:linear-gradient(to right,{lines},transparent)"></span></div>
 <div dir="rtl" style="font-family:Cairo;font-weight:700;font-size:62px;color:{sub};margin:6px 0 34px">سرعة .. أمان .. ثقة</div>
 {icons_row(acc, lines)}
</div></body></html>"""

def horizontal(theme, mono=None, bg=None, W=2200, H=760):
    ink = mono or (INK if theme=="light" else "#F4F4F4")
    acc = mono or RED
    sub = mono or ("#7A7A7A" if theme=="light" else "#BDBDBD")
    m = mark(theme, uid="h"+theme+(mono or ""), mono=mono)
    bgcss = f"background:{bg};" if bg else ""
    return f"""<html><head><style>{CSS}</style></head><body style="width:{W}px;height:{H}px;{bgcss}">
<div style="width:{W}px;height:{H}px;display:flex;align-items:center;justify-content:center;gap:40px;padding:40px">
 <svg viewBox="{VB}" width="900">{m}</svg>
 <div style="display:flex;flex-direction:column;align-items:flex-end">
  <div dir="rtl" style="font-family:Alex;font-weight:900;font-size:190px;line-height:1.2;white-space:nowrap;color:{ink}">شركة <span style="color:{acc}">الزاجل</span></div>
  <div style="display:flex;align-items:center;gap:24px;width:100%">
   <span style="flex:1;height:4px;background:{acc}"></span>
   <span class="lat" style="font-size:62px;letter-spacing:9px;color:{sub}">AL-ZAJIL COMPANY</span></div>
  <div dir="rtl" style="font-family:Cairo;font-weight:700;font-size:52px;color:{sub};margin-top:4px">سرعة .. أمان .. ثقة</div>
 </div></div></body></html>"""

def appicon(theme, W=1024):
    bg = "#FFFFFF" if theme=="light" else "#1B1B1B"
    m = mark(theme, uid="i"+theme)
    return f"""<html><head><style>{CSS}</style></head><body style="width:{W}px;height:{W}px">
<div style="width:{W}px;height:{W}px;border-radius:230px;background:{bg};display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 2px rgba(0,0,0,.06)">
 <svg viewBox="{VB}" width="900">{m}</svg></div></body></html>"""

def symbol(theme, mono=None, W=1200, H=900):
    m = mark(theme, uid="s"+theme+(mono or ""), mono=mono)
    return f"""<html><body style="margin:0;width:{W}px;height:{H}px;display:flex;align-items:center;justify-content:center"><svg viewBox="{VB}" width="{W-80}">{m}</svg></body></html>"""

jobs = {
 "01-alzajil-full-dark":     (full("dark", bg="#161616"), 1600,1750,False),
 "02-alzajil-full-light":    (full("light", bg="#FFFFFF"), 1600,1750,False),
 "03-alzajil-full-transparent": (full("light"), 1600,1750,True),
 "04-alzajil-horizontal-light": (horizontal("light", bg="#FFFFFF"), 2200,760,False),
 "05-alzajil-horizontal-dark":  (horizontal("dark", bg="#161616"), 2200,760,False),
 "06-alzajil-icon-light":    (appicon("light"),1024,1024,True),
 "07-alzajil-icon-dark":     (appicon("dark"),1024,1024,True),
 "08-alzajil-symbol-transparent": (symbol("light"),1200,900,True),
 "09-alzajil-mono-black":    (full("light", mono="#111111"),1600,1750,True),
 "10-alzajil-mono-white":    (full("dark", mono="#ffffff", bg="#E54839", knock="#E54839"),1600,1750,False),
}
os.makedirs("html",exist_ok=True)
with open("jobs.txt","w") as f:
    for k,(h,w,hh,t) in jobs.items():
        open(f"html/{k}.html","w").write(h)
        f.write(f"{k} {w} {hh} {1 if t else 0}\n")
