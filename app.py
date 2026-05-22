# app.py

import streamlit as st
import base64

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Focus Investment Resume Maker",
    layout="wide"
)

# =========================================================
# FUNCTIONS
# =========================================================

def image_to_base64(image_file):

    if image_file is None:
        return ""

    image_file.seek(0)

    return base64.b64encode(
        image_file.read()
    ).decode()


def local_image_to_base64(path):

    with open(path, "rb") as f:

        return base64.b64encode(
            f.read()
        ).decode()

# =========================================================
# LOAD LOGOS
# =========================================================

focus_logo_base64 = local_image_to_base64(
    "assets/focus_logo.png"
)

club_logo_base64 = local_image_to_base64(
    "assets/100cr_logo.png"
)

# =========================================================
# THEMES
# =========================================================

themes = {

    "Classic Black": {
        "secondary": "#f5f5f5"
    },

    "Royal Blue": {
        "secondary": "#EDF4FF"
    },

    "Emerald Green": {
        "secondary": "#EFFFF7"
    },

    "Luxury Gold": {
        "secondary": "#FFF8E1"
    }

}

# =========================================================
# TITLE
# =========================================================

st.title("💼 Focus Investment One Pager")

st.caption(
    "Tamil + English Resume / Story Maker"
)

# =========================================================
# INPUTS
# =========================================================

col1, col2 = st.columns(2)

with col1:

    theme_name = st.selectbox(
        "Choose Theme",
        list(themes.keys())
    )

    name = st.text_input(
        "Name"
    )

    duration = st.text_input(
        "Experience / Duration",
        value="More than 5 Years"
    )

    page_number = st.number_input(
        "Page Number",
        min_value=1,
        value=1
    )

with col2:

    uploaded_image = st.file_uploader(
        "Upload Profile Image",
        type=["png", "jpg", "jpeg"]
    )

    # =====================================================
    # FONT SIZE CONTROLS
    # =====================================================

    content_font_size = st.slider(
        "Content Font Size",
        14,
        36,
        22
    )

    name_font_size = st.slider(
        "Name Font Size",
        20,
        60,
        34
    )

    duration_font_size = st.slider(
        "Duration Font Size",
        24,
        80,
        52
    )

    # =====================================================
    # HEIGHT CONTROLS
    # =====================================================

    header_height = st.slider(
        "Header Height",
        80,
        250,
        120
    )

    footer_height = st.slider(
        "Footer Height",
        140,
        450,
        220
    )

    # =====================================================
    # CONTENT POSITION CONTROLS
    # =====================================================

    content_left_padding = st.slider(
        "Content Left Spacing",
        0,
        150,
        20
    )

    content_top_padding = st.slider(
        "Content Top Spacing",
        0,
        100,
        8
    )

theme = themes[theme_name]

# =========================================================
# CONTENT
# =========================================================

intro = st.text_area(
    "Introduction",
    height=350
)

# Remove ONLY accidental first newline



# =========================================================
# PROFILE IMAGE
# =========================================================

if uploaded_image:

    profile_base64 = image_to_base64(
        uploaded_image
    )

    profile_html = f"""

    <img
    src="data:image/png;base64,{profile_base64}"

    style="
    width:170px;
    height:170px;
    border-radius:50%;
    border:6px solid white;
    object-fit:cover;
    ">

    """

else:

    profile_html = """

    <div style="
    width:170px;
    height:170px;
    border-radius:50%;
    background:#cccccc;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#666666;
    font-size:18px;
    ">

    No Image

    </div>

    """

# =========================================================
# HTML TEMPLATE
# =========================================================

preview_html = f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0">

<link
href="https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;700&display=swap"
rel="stylesheet">

<style>

@page {{

    size:A4;
    margin:0;
}}

* {{

    box-sizing:border-box;
}}

html, body {{

    margin:0;
    padding:0;

    background:white;

    font-family:'Noto Sans Tamil', sans-serif;
}}

body {{

    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;

    padding:0;
}}

.page {{

    width:794px;

    min-height:1123px;

    margin:0 auto;

    background:white;

    display:flex;

    flex-direction:column;

    overflow:hidden;
}}

.header {{

    display:flex;

    justify-content:space-between;

    align-items:center;

    height:{header_height}px;

    padding:15px 25px;

    border-bottom:4px solid black;

    gap:15px;
}}

.page-box {{

    background:linear-gradient(to right,#000,#777,#eee);

    color:white;

    padding:10px 20px;

    border-radius:6px;

    font-weight:bold;

    font-size:22px;

    white-space:nowrap;
}}

.content {{

    padding:
    {content_top_padding}px
    20px
    15px
    {content_left_padding}px;

    line-height:1.5;

    font-size:{content_font_size}px;

    min-height:300px;

    background:{theme['secondary']};

    white-space:pre-wrap;

    word-break:break-word;
}}

.footer {{

    margin-top:auto;

    min-height:{footer_height}px;

    display:flex;

    align-items:center;

    background:linear-gradient(to right,#000,#555,#ddd);

    padding:20px 25px;

    gap:20px;
}}

.profile-section {{

    width:220px;
}}

.details-section {{

    flex:1;

    color:white;
}}

.name {{

    font-size:{name_font_size}px;

    font-weight:bold;

    text-decoration:underline;

    margin-bottom:15px;

    word-break:break-word;
}}

.duration {{

    font-size:{duration_font_size}px;

    line-height:1.2;
}}

.print-button {{

    position:fixed;

    top:20px;

    right:20px;

    z-index:9999;

    background:black;

    color:white;

    border:none;

    padding:14px 24px;

    border-radius:10px;

    font-size:18px;

    cursor:pointer;
}}

.instructions {{

    position:fixed;

    top:90px;

    right:20px;

    z-index:9999;

    background:white;

    border:1px solid #cccccc;

    padding:12px;

    border-radius:8px;

    font-size:14px;

    width:240px;

    line-height:1.6;

    box-shadow:0 2px 10px rgba(0,0,0,0.1);
}}

/* =====================================================
   MOBILE FIXES
===================================================== */

@media screen and (max-width:768px) {{

    html, body {{

        overflow-x:hidden;
    }}

    .page {{

        width:100%;

        min-height:auto;
    }}

    .header {{

        flex-wrap:wrap;

        justify-content:center;

        text-align:center;

        height:auto;

        padding:15px;
    }}

    .header img {{

        max-width:110px;
    }}

    .page-box {{

        font-size:14px;

        padding:8px 14px;
    }}

    .content {{

        font-size:18px !important;

        line-height:1.6;

        padding:10px 15px;
    }}

    .footer {{

        flex-direction:column;

        align-items:center;

        justify-content:center;

        text-align:center;

        padding:20px 15px;

        gap:15px;
    }}

    .profile-section {{

        width:100%;

        display:flex;

        justify-content:center;
    }}

    .details-section {{

        width:100%;

        padding:0;

        text-align:center;
    }}

    .name {{

        font-size:28px !important;

        margin-bottom:10px;
    }}

    .duration {{

        font-size:34px !important;
    }}

    .instructions {{

        display:none;
    }}

    .print-button {{

        top:10px;

        right:10px;

        padding:10px 14px;

        font-size:14px;
    }}
}}

@media print {{

    body {{

        background:white !important;

        padding:0 !important;
    }}

    .print-button,
    .instructions {{

        display:none !important;
    }}

    .page {{

        width:794px !important;

        min-height:1123px !important;

        margin:0 auto !important;

        box-shadow:none !important;

        page-break-after:avoid !important;
    }}
}}

</style>

<script>

function printPage() {{

    const content = document.documentElement.outerHTML;

    const printWindow = window.open('', '_blank');

    printWindow.document.open();

    printWindow.document.write(content);

    printWindow.document.close();

    setTimeout(() => {{

        printWindow.focus();

        printWindow.print();

    }}, 500);
}}

</script>

</head>

<body>

<button
class="print-button"
onclick="printPage()">

🖨 Save PDF

</button>

<div class="instructions">

<b>Chrome Print Settings</b>

<br><br>

❌ Disable Headers & Footers

<br>

✅ Enable Background Graphics

</div>

<div class="page">

    <!-- HEADER -->

    <div class="header">

        <img
        src="data:image/png;base64,{focus_logo_base64}"
        width="220">

        <img
        src="data:image/png;base64,{club_logo_base64}"
        width="140">

        <div class="page-box">

            Page {page_number}

        </div>

    </div>

    <!-- CONTENT -->

    <div class="content">{intro}</div>

    <!-- FOOTER -->

    <div class="footer">

        <div class="profile-section">

            {profile_html}

        </div>

        <div class="details-section">

            <div class="name">

                {name}

            </div>

            <div class="duration">

                {duration}

            </div>

        </div>

    </div>

</div>

</body>

</html>

"""

# =========================================================
# PREVIEW
# =========================================================

st.markdown("---")

st.subheader("Preview")

st.info(
    "Use Chrome → Print → Save as PDF"
)

st.components.v1.html(
    preview_html,
    height=1300,
    scrolling=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("PDF Tips")

st.sidebar.write("""

In Chrome Print:

❌ Disable Headers & Footers

✅ Enable Background Graphics

""")