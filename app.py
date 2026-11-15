import streamlit as st
import base64
import html

st.set_page_config(page_title="Focus Investment Profile Maker", page_icon="🎯", layout="wide")


def b64(data):
    return base64.b64encode(data).decode("utf-8") if data else ""


def upload_img(file):
    return f"data:{file.type or 'image/png'};base64,{b64(file.getvalue())}" if file else ""


def esc(value):
    return html.escape(str(value or ""), quote=True)


def make_block(kind, block_id):
    return {
        "id": block_id, "type": kind, "text": "", "heading": "",
        "image": None, "width": 70, "align": "center",
        "font_size": 22, "color": "#111111",
        "heading_color": "#111111", "background": "#FFFFFF",
        "use_default": True, "custom_bg": False,
    }


if "blocks" not in st.session_state:
    st.session_state.blocks = [make_block("text", 1)]
    st.session_state.next_id = 2
if "next_id" not in st.session_state:
    st.session_state.next_id = 2
# Upgrade blocks created by an older version of the app in the same session.
for _b in st.session_state.blocks:
    _b.setdefault("use_default", True)
    _b.setdefault("custom_bg", False)
    if not str(_b.get("background", "")).startswith("#"):
        _b["background"] = "#FFFFFF"

st.title("🎯 Focus Investment – Profile / Story Maker")
st.caption("Tamil + English community profile maker. Add text, headings and photos anywhere in the content.")

st.subheader("Profile details")
a, b = st.columns(2)
with a:
    name = st.text_input("Name")
    highlight = st.text_input("Experience / Highlight (optional)", "")
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
h1, h2 = st.columns(2)
with h1:
    header_height = st.slider("Header height (px)", 0, 300, 60,
                              help="Set to 0 to hide the header (page label and divider).")
    header_padding = st.slider("Header left/right padding (px)", 0, 100, 25)
    page_label_size = st.slider("Page label font size (px)", 0, 40, 16)
with h2:
    footer_height = st.slider("Footer height (px)", 0, 500, 220)
    footer_padding = st.slider("Footer padding (px)", 0, 100, 20)

st.divider()
st.subheader("Content default appearance")
st.caption("Blocks with “Use default text style” ticked follow these settings.")
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
            s1, s2 = st.columns(2)
            with s1:
                block["use_default"] = st.checkbox("Use default text style", value=block["use_default"],
                                                   key=f"usedef_{bid}")
            with s2:
                block["custom_bg"] = st.checkbox("Custom block background", value=block["custom_bg"],
                                                 key=f"custombg_{bid}")
            q1, q2, q3 = st.columns(3)
            with q1:
                block["font_size"] = st.slider("Block text size (px)", 0, 60, int(block["font_size"]),
                                               key=f"size_{bid}", disabled=block["use_default"])
            with q2:
                block["color"] = st.color_picker("Text colour", block["color"], key=f"colour_{bid}",
                                                 disabled=block["use_default"])
            with q3:
                block["background"] = st.color_picker("Block background", block["background"],
                                                      key=f"background_{bid}", disabled=not block["custom_bg"])
            if block["type"] == "heading":
                block["heading_color"] = st.color_picker("Heading colour", block["heading_color"],
                                                         key=f"hcolour_{bid}", disabled=block["use_default"])

st.divider()
st.subheader("Footer appearance")
f1, f2, f3 = st.columns(3)
with f1:
    footer_start = st.color_picker("Footer gradient start", "#000000")
with f2:
    footer_end = st.color_picker("Footer gradient end", "#DDDDDD")
with f3:
    footer_text = st.color_picker("Footer text colour", "#FFFFFF")
n1, n2 = st.columns(2)
with n1:
    name_size = st.slider("Name font size (px)", 0, 100, 34)
with n2:
    highlight_size = st.slider("Highlight font size (px)", 0, 120, 52)


def block_style(block):
    """Resolve per-block style, falling back to the content defaults."""
    if block.get("use_default", True):
        size, color, hcolor = default_font_size, default_text_color, default_heading_color
    else:
        size, color, hcolor = int(block["font_size"]), block["color"], block["heading_color"]
    bg = block["background"] if block.get("custom_bg") else "transparent"
    pad = "padding:10px 12px;border-radius:6px;" if block.get("custom_bg") else ""
    return size, color, hcolor, bg, pad


# Build HTML blocks in the same order as the editor.
parts = []
for block in st.session_state.blocks:
    kind = block["type"]
    if kind == "text":
        value = esc(block["text"])
        if value:
            size, color, _, bg, pad = block_style(block)
            parts.append(
                f'<div class="content-block" style="font-size:{size}px;'
                f'color:{color};background:{bg};{pad}">{value}</div>'
            )
    elif kind == "heading":
        heading = esc(block["heading"])
        supporting = esc(block["text"])
        if heading or supporting:
            size, color, hcolor, bg, pad = block_style(block)
            heading_html = (f'<h2 style="font-size:{size}px;color:{hcolor};">'
                            f'{heading}</h2>') if heading else ""
            supporting_html = (f'<div class="supporting" style="font-size:{size}px;'
                               f'color:{color};">{supporting}</div>') if supporting else ""
            parts.append(f'<section class="content-block" style="background:{bg};{pad}">'
                         f'{heading_html}{supporting_html}</section>')
    elif kind == "image" and block["image"] is not None:
        src = upload_img(block["image"])
        parts.append(
            f'<div class="photo-block" style="text-align:{block["align"]};">'
            f'<img src="{src}" alt="" style="width:{int(block["width"])}%;max-width:100%;height:auto;"></div>'
        )

content_html = "\n".join(parts)
profile_src = upload_img(profile_file)

# Profile picture is optional: nothing is shown unless a photo is uploaded.
if profile_src and profile_size > 0:
    profile_html = (f'<img class="profile" src="{profile_src}" alt="" '
                    f'style="width:{profile_size}px;height:{profile_size}px;border:{profile_border}px solid white;">')
else:
    profile_html = ""

header_html = (f'<header class="header"><div class="page-label">{esc(page_label)}</div></header>'
               if header_height > 0 else "")
profile_section = f'<div class="profile-section">{profile_html}</div>' if profile_html else ""
name_html = f'<div class="name">{esc(name)}</div>' if name.strip() else ""
highlight_html = f'<div class="highlight">{esc(highlight)}</div>' if highlight.strip() else ""
details_html = f'<div class="details">{name_html}{highlight_html}</div>' if (name_html or highlight_html) else ""
# Footer is shown only when it has content (photo, name or highlight).
footer_html = (f'<footer class="footer">{profile_section}{details_html}</footer>'
               if (profile_section or details_html) and footer_height >= 0 else "")

preview = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;500;600;700&family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; padding:0;
font-family:'Noto Sans Tamil','Noto Sans','Nirmala UI','Latha',sans-serif;
font-kerning:normal; text-rendering:optimizeLegibility; letter-spacing:normal;
-webkit-print-color-adjust:exact!important; print-color-adjust:exact!important; }}
body {{ background:#eeeeee; }}
.page {{ width:794px; min-height:1123px; margin:20px auto; background:white; display:flex;
flex-direction:column; overflow:hidden; box-shadow:0 2px 14px #0002; }}
.header {{ height:{header_height}px; flex:0 0 {header_height}px; padding:0 {header_padding}px;
background:#FFFFFF; display:flex; align-items:center; justify-content:flex-end;
border-bottom:1px solid #000; overflow:hidden; }}
.page-label {{ color:#111; font-size:{page_label_size}px; font-weight:600; white-space:nowrap; }}
.content {{ flex:1 0 auto; padding:{top_padding}px {right_padding}px {bottom_padding}px {left_padding}px;
background:{content_bg}; line-height:{line_height}; overflow-wrap:break-word; }}
.content-block {{ white-space:pre-wrap; overflow-wrap:break-word; margin:0 0 22px 0; }}
.content-block:last-child, .photo-block:last-child {{ margin-bottom:0; }}
.content-block h2 {{ line-height:1.3; margin:0 0 10px 0; white-space:pre-wrap; overflow-wrap:break-word;
break-after:avoid; page-break-after:avoid; }}
.supporting {{ white-space:pre-wrap; overflow-wrap:break-word; }}
.photo-block {{ width:100%; margin:18px 0 24px; line-height:0; break-inside:avoid; page-break-inside:avoid; }}
.photo-block img {{ display:inline-block; object-fit:contain; }}
.footer {{ min-height:{footer_height}px; flex:0 0 auto; padding:{footer_padding}px;
display:flex; align-items:center; gap:24px; break-inside:avoid; page-break-inside:avoid;
background:linear-gradient(90deg,{footer_start},#777,{footer_end}); }}
.profile-section {{ flex:0 0 auto; display:flex; align-items:center; justify-content:{profile_position.lower()}; }}
.profile {{ display:block; border-radius:50%; object-fit:cover; }}
.no-image {{ border-radius:50%;background:#ccc;color:#666;
display:flex;align-items:center;justify-content:center; }}
.details {{ flex:1;min-width:0;color:{footer_text}; }}
.name {{ font-size:{name_size}px;font-weight:bold;text-decoration:underline;margin-bottom:12px;overflow-wrap:break-word; }}
.highlight {{ font-size:{highlight_size}px;line-height:1.2;overflow-wrap:break-word; }}
.printbar {{ width:794px;margin:12px auto;text-align:right; }}
.printbar button {{ border:0;background:#111;color:white;border-radius:7px;padding:12px 20px;font-size:16px;cursor:pointer; }}
@media(max-width:820px) {{
 body {{ background:#eee; }}
 .page {{ width:100%;min-height:0;margin:8px auto; }}
 .header {{ padding:0 12px;justify-content:flex-end; }}
 .page-label {{ font-size:min({page_label_size}px,14px); }}
 .content {{ padding:{top_padding}px 15px {bottom_padding}px 15px; }}
 .footer {{ flex-wrap:wrap;justify-content:center;text-align:center;padding:18px; }}
 .profile-section {{ width:100%;justify-content:center; }}
 .profile, .no-image {{ max-width:min({profile_size}px,45vw);max-height:min({profile_size}px,45vw); }}
 .details {{ width:100%;text-align:center; }}
 .name {{ font-size:min({name_size}px,30px); }}
 .highlight {{ font-size:min({highlight_size}px,36px); }}
 .printbar {{ width:100%;padding:0 12px; }}
}}
@media print {{
 html,body {{ width:210mm;margin:0!important;padding:0!important;background:white!important; }}
 .printbar {{ display:none!important; }}
 .page {{ width:210mm!important;min-height:296.5mm!important;margin:0!important;box-shadow:none!important;
 overflow:visible!important; }}
 .header {{ height:{header_height}px!important;flex-wrap:nowrap!important;padding:0 {header_padding}px!important; }}
 .content {{ padding:{top_padding}px {right_padding}px {bottom_padding}px {left_padding}px!important; }}
 .footer {{ flex-wrap:nowrap!important;text-align:left!important;padding:{footer_padding}px!important; }}
 .profile-section {{ width:auto!important;justify-content:{profile_position.lower()}!important; }}
 .profile, .no-image {{ max-width:none!important;max-height:none!important; }}
 .details {{ width:auto!important;text-align:left!important; }}
 .name {{ font-size:{name_size}px!important; }}
 .highlight {{ font-size:{highlight_size}px!important; }}
}}
</style></head><body>
<div class="printbar"><button onclick="(document.fonts?document.fonts.ready:Promise.resolve()).then(function(){{window.print();}})">🖨 Print / Save as PDF</button></div>
<div class="page">
{header_html}
<main class="content">{content_html}</main>
{footer_html}
</div></body></html>"""

st.divider()
st.subheader("Live preview")
st.info("Use the Print / Save as PDF button inside the preview. In Chrome, enable Background graphics and "
        "disable browser Headers and footers. On mobile, download the HTML below, open it in your browser "
        "and print from there so only the profile is printed.")
if hasattr(st, "iframe"):  # newer Streamlit versions
    st.iframe(preview, height=1250)
else:  # older Streamlit versions
    import streamlit.components.v1 as components
    components.html(preview, height=1250, scrolling=True)
st.download_button("⬇ Download profile (HTML for printing)", data=preview.encode("utf-8"),
                   file_name=f"{(name or 'profile').strip().replace(' ', '_')}_profile.html",
                   mime="text/html", use_container_width=True)
