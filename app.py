import streamlit as st
import base64
import html
from pathlib import Path

st.set_page_config(page_title="Focus Investment Profile Maker", page_icon="🎯", layout="wide")
ASSETS = Path(__file__).parent / "assets"

def b64(data):
    return base64.b64encode(data).decode("utf-8") if data else ""

def local_img(filename):
    path = ASSETS / filename
    if not path.exists():
        return ""
    ext = path.suffix.lower()
    mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    return f"data:{mime};base64,{b64(path.read_bytes())}"

def upload_img(file):
    return f"data:{file.type or 'image/png'};base64,{b64(file.getvalue())}" if file else ""

def esc(value):
    return html.escape(str(value or ""), quote=True)

def make_block(kind, block_id):
    return {
        "id": block_id, "type": kind, "text": "", "heading": "",
        "image": None, "width": 70, "align": "center",
        "font_size": 22, "color": "#111111",
        "heading_color": "#111111", "background": "transparent"
    }

if "blocks" not in st.session_state:
    st.session_state.blocks = [make_block("text", 1)]
    st.session_state.next_id = 2
if "next_id" not in st.session_state:
    st.session_state.next_id = 2

st.title("🎯 Focus Investment – Profile / Story Maker")
st.caption("Tamil + English community profile maker. Add text, headings and photos anywhere in the content.")

st.subheader("Profile details")
a, b = st.columns(2)
with a:
    name = st.text_input("Name")
    highlight = st.text_input("Experience / Highlight", "More than 5 Years")
    page_label = st.text_input("Page label", "Page 1")
    theme = st.selectbox("Theme", ["Classic Grey", "Royal Blue", "Emerald Green", "Luxury Gold", "White"])
with b:
    profile_file = st.file_uploader("Profile picture (optional)", type=["png", "jpg", "jpeg"])
    profile_size = st.slider("Profile picture size (px)", 0, 300, 170)
    profile_border = st.slider("Profile picture border (px)", 0, 20, 6)
    profile_position = st.selectbox("Profile picture alignment", ["Left", "Center", "Right"])

theme_bg = {
    "Classic Grey": "#F4F4F4", "Royal Blue": "#EDF4FF",
    "Emerald Green": "#EFFFF7", "Luxury Gold": "#FFF8E1", "White": "#FFFFFF"
}[theme]

st.divider()
st.subheader("Header and footer settings")
h1, h2, h3 = st.columns(3)
with h1:
    header_height = st.slider("Header height (px)", 0, 300, 120)
    header_padding = st.slider("Header left/right padding (px)", 0, 100, 25)
with h2:
    footer_height = st.slider("Footer height (px)", 0, 500, 220)
    footer_padding = st.slider("Footer padding (px)", 0, 100, 20)
with h3:
    focus_logo_width = st.slider("Focus logo width (px)", 0, 300, 220)
    club_logo_width = st.slider("100CR logo width (px)", 0, 250, 140)

st.divider()
st.subheader("Content default appearance")
c1, c2, c3 = st.columns(3)
with c1:
    default_font_size = st.slider("Default text size (px)", 0, 60, 22)
    default_text_color = st.color_picker("Default text colour", "#111111")
with c2:
    content_bg = st.color_picker("Content background colour", theme_bg)
    default_heading_color = st.color_picker("Default heading colour", "#111111")
with c3:
    top_padding = st.slider("Content top spacing (px)", 0, 200, 8)
    bottom_padding = st.slider("Content bottom spacing (px)", 0, 200, 15)

p1, p2, p3 = st.columns(3)
with p1:
    left_padding = st.slider("Content left spacing (px)", 0, 250, 20)
with p2:
    right_padding = st.slider("Content right spacing (px)", 0, 250, 20)
with p3:
    line_height = st.slider("Content line height", 1.0, 2.5, 1.5, 0.1)

st.divider()
st.subheader("Build your content")
st.write("Add blocks in the order you want. Use ↑ / ↓ to position a photo between any text sections.")

x1, x2, x3 = st.columns(3)
with x1:
    if st.button("＋ Add text", use_container_width=True):
        st.session_state.blocks.append(make_block("text", st.session_state.next_id))
        st.session_state.next_id += 1
        st.rerun()
with x2:
    if st.button("＋ Add heading", use_container_width=True):
        st.session_state.blocks.append(make_block("heading", st.session_state.next_id))
        st.session_state.next_id += 1
        st.rerun()
with x3:
    if st.button("＋ Add photo", use_container_width=True):
        st.session_state.blocks.append(make_block("image", st.session_state.next_id))
        st.session_state.next_id += 1
        st.rerun()

for i, block in enumerate(st.session_state.blocks):
    bid = block["id"]
    with st.container(border=True):
        t, up, down, delete = st.columns([5, 1, 1, 1])
        with t:
            st.markdown(f"**{i + 1}. {block['type'].capitalize()} block**")
        with up:
            if st.button("↑", key=f"up_{bid}", disabled=i == 0):
                st.session_state.blocks[i-1], st.session_state.blocks[i] = st.session_state.blocks[i], st.session_state.blocks[i-1]
                st.rerun()
        with down:
            if st.button("↓", key=f"down_{bid}", disabled=i == len(st.session_state.blocks)-1):
                st.session_state.blocks[i+1], st.session_state.blocks[i] = st.session_state.blocks[i], st.session_state.blocks[i+1]
                st.rerun()
        with delete:
            if st.button("✕", key=f"del_{bid}", disabled=len(st.session_state.blocks) == 1):
                st.session_state.blocks.pop(i)
                st.rerun()

        if block["type"] == "text":
            block["text"] = st.text_area("Text", value=block["text"], height=130, key=f"text_{bid}",
                                         help="Line breaks and blank lines are preserved.")
        elif block["type"] == "heading":
            block["heading"] = st.text_input("Heading", value=block["heading"], key=f"heading_{bid}")
            block["text"] = st.text_area("Supporting text (optional)", value=block["text"], height=90, key=f"support_{bid}")
        else:
            block["image"] = st.file_uploader("Choose photo", type=["png", "jpg", "jpeg", "webp"], key=f"photo_{bid}")
            im1, im2 = st.columns(2)
            with im1:
                block["width"] = st.slider("Photo width (%)", 5, 100, int(block["width"]), key=f"width_{bid}")
            with im2:
                block["align"] = st.selectbox("Photo alignment", ["left", "center", "right"],
                                              index=["left", "center", "right"].index(block["align"]), key=f"align_{bid}")

        if block["type"] in ("text", "heading"):
            q1, q2, q3 = st.columns(3)
            with q1:
                block["font_size"] = st.slider("Block text size (px)", 0, 60, int(block["font_size"]), key=f"size_{bid}")
            with q2:
                block["color"] = st.color_picker("Text colour", block["color"], key=f"colour_{bid}")
            with q3:
                block["background"] = st.color_picker("Block background", "#FFFFFF", key=f"background_{bid}")
            if block["type"] == "heading":
                block["heading_color"] = st.color_picker("Heading colour", block["heading_color"], key=f"hcolour_{bid}")

st.divider()
st.subheader("Footer appearance")
f1, f2, f3 = st.columns(3)
with f1:
    footer_start = st.color_picker("Footer gradient start", "#000000")
with f2:
    footer_end = st.color_picker("Footer gradient end", "#DDDDDD")
with f3:
    footer_text = st.color_picker("Footer text colour", "#FFFFFF")
name_size = st.slider("Name font size (px)", 0, 100, 34)
highlight_size = st.slider("Highlight font size (px)", 0, 120, 52)

# Build HTML blocks in the same order as the editor.
parts = []
for block in st.session_state.blocks:
    kind = block["type"]
    if kind == "text":
        value = esc(block["text"])
        if value:
            parts.append(
                f'<div class="content-block" style="font-size:{int(block["font_size"])}px;'
                f'color:{block["color"]};background:{block["background"]};">{value}</div>'
            )
    elif kind == "heading":
        heading = esc(block["heading"])
        supporting = esc(block["text"])
        if heading or supporting:
            heading_html = (f'<h2 style="font-size:{int(block["font_size"])}px;color:{block["heading_color"]};">'
                            f'{heading}</h2>') if heading else ""
            supporting_html = (f'<div class="supporting" style="font-size:{int(block["font_size"])}px;'
                               f'color:{block["color"]};">{supporting}</div>') if supporting else ""
            parts.append(f'<section class="content-block" style="background:{block["background"]};">'
                         f'{heading_html}{supporting_html}</section>')
    elif kind == "image" and block["image"] is not None:
        src = upload_img(block["image"])
        parts.append(
            f'<div class="photo-block" style="text-align:{block["align"]};">'
            f'<img src="{src}" style="width:{int(block["width"])}%;max-width:100%;height:auto;"></div>'
        )

content_html = "\n".join(parts)
focus_logo = local_img("focus_logo.png")
club_logo = local_img("100cr_logo.png")
profile_src = upload_img(profile_file)

def logo(uri, width, alt):
    return f'<img class="logo" src="{uri}" style="width:{width}px;" alt="{esc(alt)}">' if uri and width > 0 else ""

if profile_src and profile_size > 0:
    profile_html = (f'<img class="profile" src="{profile_src}" '
                    f'style="width:{profile_size}px;height:{profile_size}px;border:{profile_border}px solid white;">')
else:
    profile_html = '<div class="no-image">No Image</div>'

preview = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; padding:0; font-family:'Noto Sans Tamil','Nirmala UI',sans-serif;
-webkit-print-color-adjust:exact!important; print-color-adjust:exact!important; }}
body {{ background:#eeeeee; }}
.page {{ width:794px; min-height:1123px; margin:20px auto; background:white; display:flex;
flex-direction:column; overflow:hidden; box-shadow:0 2px 14px #0002; }}
.header {{ height:{header_height}px; flex:0 0 {header_height}px; padding:0 {header_padding}px;
display:flex; align-items:center; justify-content:space-between; gap:12px; border-bottom:4px solid black; }}
.logo {{ max-height:95%; height:auto; object-fit:contain; }}
.page-label {{ background:linear-gradient(90deg,#000,#ddd); color:white; padding:9px 18px;
border-radius:6px; font-size:20px; font-weight:bold; white-space:nowrap; }}
.content {{ flex:1 0 auto; padding:{top_padding}px {right_padding}px {bottom_padding}px {left_padding}px;
background:{content_bg}; line-height:{line_height}; overflow-wrap:anywhere; }}
.content-block {{ white-space:pre-wrap; overflow-wrap:anywhere; margin:0 0 22px 0; }}
.content-block h2 {{ line-height:1.3; margin:0 0 10px 0; white-space:pre-wrap; overflow-wrap:anywhere; }}
.supporting {{ white-space:pre-wrap; overflow-wrap:anywhere; }}
.photo-block {{ width:100%; margin:18px 0 24px; }}
.photo-block img {{ display:inline-block; object-fit:contain; }}
.footer {{ min-height:{footer_height}px; flex:0 0 auto; padding:{footer_padding}px;
display:flex; align-items:center; gap:24px;
background:linear-gradient(90deg,{footer_start},#777,{footer_end}); }}
.profile-section {{ flex:0 0 auto; display:flex; align-items:center; justify-content:{profile_position.lower()}; }}
.profile {{ display:block; border-radius:50%; object-fit:cover; }}
.no-image {{ width:170px;height:170px;border-radius:50%;background:#ccc;color:#666;
display:flex;align-items:center;justify-content:center; }}
.details {{ flex:1;min-width:0;color:{footer_text}; }}
.name {{ font-size:{name_size}px;font-weight:bold;text-decoration:underline;margin-bottom:12px;overflow-wrap:anywhere; }}
.highlight {{ font-size:{highlight_size}px;line-height:1.2;overflow-wrap:anywhere; }}
.printbar {{ width:794px;margin:12px auto;text-align:right; }}
.printbar button {{ border:0;background:#111;color:white;border-radius:7px;padding:12px 20px;font-size:16px; }}
@media(max-width:820px) {{
 body {{ background:#eee; }}
 .page {{ width:100%;min-height:0;margin:8px auto; }}
 .header {{ height:auto;min-height:{header_height}px;flex-wrap:wrap;justify-content:space-around;padding:12px; }}
 .logo {{ max-width:30%;max-height:75px; }}
 .page-label {{ font-size:13px;padding:7px 10px; }}
 .content {{ padding:{top_padding}px 15px {bottom_padding}px 15px; }}
 .footer {{ flex-wrap:wrap;justify-content:center;text-align:center;padding:18px; }}
 .profile-section {{ width:100%;justify-content:center; }}
 .details {{ width:100%;text-align:center; }}
 .name {{ font-size:min({name_size}px,30px); }}
 .highlight {{ font-size:min({highlight_size}px,36px); }}
 .printbar {{ width:100%;padding:0 12px; }}
}}
@media print {{
 html,body {{ width:210mm;margin:0!important;padding:0!important;background:white!important; }}
 .printbar {{ display:none!important; }}
 .page {{ width:210mm!important;min-height:297mm!important;margin:0!important;box-shadow:none!important;
 break-after:page;page-break-after:always; }}
}}
</style></head><body>
<div class="printbar"><button onclick="window.print()">🖨 Print / Save as PDF</button></div>
<div class="page">
<header class="header">{logo(focus_logo,focus_logo_width,"Focus Investment logo")}
{logo(club_logo,club_logo_width,"100CR logo")}<div class="page-label">{esc(page_label)}</div></header>
<main class="content">{content_html}</main>
<footer class="footer"><div class="profile-section">{profile_html}</div>
<div class="details"><div class="name">{esc(name)}</div><div class="highlight">{esc(highlight)}</div></div></footer>
</div></body></html>"""

st.divider()
st.subheader("Live preview")
st.info("Use the Print / Save as PDF button inside the preview. In Chrome, enable Background graphics and disable browser Headers and footers.")
st.components.v1.html(preview, height=1250, scrolling=True)
st.caption("Optional logo files: assets/focus_logo.png and assets/100cr_logo.png. If not present, the logo positions remain blank.")
