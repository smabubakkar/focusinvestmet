# app.py

import streamlit as st
from PIL import Image
from io import BytesIO
import tempfile
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as RLImage,
    Table,
    TableStyle
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Focus Investment Resume Maker",
    layout="centered"
)

# =========================================
# TAMIL FONT SETUP
# =========================================

# Download and keep this font in same folder:
# https://github.com/googlefonts/noto-fonts/blob/main/hinted/ttf/NotoSansTamil/NotoSansTamil-Regular.ttf

FONT_NAME = "Tamil"

if os.path.exists("NotoSansTamil-Regular.ttf"):
    pdfmetrics.registerFont(
        TTFont(FONT_NAME, "NotoSansTamil-Regular.ttf")
    )
else:
    FONT_NAME = "Helvetica"

# =========================================
# THEMES
# =========================================

themes = {
    "Classic Black": {
        "primary": colors.black,
        "secondary": colors.HexColor("#F3F3F3"),
        "text": colors.black,
        "header_text": colors.white
    },

    "Royal Blue": {
        "primary": colors.HexColor("#0B3D91"),
        "secondary": colors.HexColor("#EAF1FF"),
        "text": colors.black,
        "header_text": colors.white
    },

    "Emerald Green": {
        "primary": colors.HexColor("#006B4F"),
        "secondary": colors.HexColor("#E9FFF6"),
        "text": colors.black,
        "header_text": colors.white
    },

    "Luxury Gold": {
        "primary": colors.HexColor("#B8860B"),
        "secondary": colors.HexColor("#FFF8E1"),
        "text": colors.black,
        "header_text": colors.black
    }
}

# =========================================
# UI
# =========================================

st.title("📄 Focus Investment One Pager")

theme_choice = st.selectbox(
    "Choose Theme",
    list(themes.keys())
)

selected_theme = themes[theme_choice]

community = st.text_input(
    "Community Name",
    value="FOCUS INVESTMENT"
)

name = st.text_input("Your Name")

dob = st.date_input("Date of Birth")

intro = st.text_area(
    "Introduction (Tamil + English Supported)",
    height=220,
    placeholder="உங்களை பற்றிய சிறிய அறிமுகம்..."
)

uploaded_image = st.file_uploader(
    "Upload Your Photo",
    type=["png", "jpg", "jpeg"]
)

# =========================================
# LIVE PREVIEW
# =========================================

st.markdown("---")
st.subheader("Live Preview")

preview_bg = selected_theme["secondary"].hexval()

st.markdown(
    f"""
    <div style="
        background-color:{preview_bg};
        padding:20px;
        border-radius:15px;
        border:2px solid #DDD;
    ">
    <h1>{community}</h1>
    <hr>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 2])

with col1:
    if uploaded_image:
        st.image(uploaded_image, width=180)

with col2:
    st.markdown(f"## {name}")
    st.write(f"**DOB:** {dob}")
    st.write(intro)

# =========================================
# PDF FUNCTION
# =========================================

def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "title_style",
        parent=styles['Title'],
        fontName=FONT_NAME,
        fontSize=28,
        textColor=selected_theme["header_text"],
        alignment=TA_CENTER,
        spaceAfter=20
    )

    body_style = ParagraphStyle(
        "body_style",
        parent=styles['BodyText'],
        fontName=FONT_NAME,
        fontSize=13,
        leading=22,
        textColor=selected_theme["text"]
    )

    name_style = ParagraphStyle(
        "name_style",
        parent=styles['Heading1'],
        fontName=FONT_NAME,
        fontSize=24,
        textColor=selected_theme["text"]
    )

    elements = []

    # =====================================
    # HEADER
    # =====================================

    header_table = Table(
        [[Paragraph(community, title_style)]],
        colWidths=[7.2 * inch]
    )

    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), selected_theme["primary"]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
        ('TOPPADDING', (0, 0), (-1, -1), 18),
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 0.3 * inch))

    # =====================================
    # IMAGE
    # =====================================

    image_path = None

    if uploaded_image:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_image.getvalue())
            image_path = tmp.name

    left_side = []
    right_side = []

    if image_path:
        img = RLImage(
            image_path,
            width=2.4 * inch,
            height=3 * inch
        )
        left_side.append(img)

    # =====================================
    # CONTENT
    # =====================================

    content = f"""
    <b>{name}</b><br/><br/>
    <b>Date of Birth:</b> {dob}<br/><br/>
    {intro}
    """

    right_side.append(
        Paragraph(content, body_style)
    )

    profile_table = Table(
        [[left_side, right_side]],
        colWidths=[2.6 * inch, 4.3 * inch]
    )

    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), selected_theme["secondary"]),
        ('BOX', (0, 0), (-1, -1), 2, selected_theme["primary"]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),

        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))

    elements.append(profile_table)

    # =====================================
    # FOOTER
    # =====================================

    elements.append(Spacer(1, 0.4 * inch))

    footer = Paragraph(
        "Focus Investment Community",
        body_style
    )

    elements.append(footer)

    # =====================================
    # BUILD PDF
    # =====================================

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    if image_path and os.path.exists(image_path):
        os.remove(image_path)

    return pdf

# =========================================
# DOWNLOAD
# =========================================

st.markdown("---")

if st.button("Generate PDF"):

    if not name or not intro:
        st.error("Please fill mandatory fields")
    else:

        pdf = generate_pdf()

        st.success("PDF Generated Successfully")

        st.download_button(
            label="📥 Download PDF",
            data=pdf,
            file_name=f"{name}_focus_resume.pdf",
            mime="application/pdf"
        )

# =========================================
# SIDEBAR INFO
# =========================================

st.sidebar.title("Tamil Font Setup")

st.sidebar.code(
"""
1. Download Tamil Font:
NotoSansTamil-Regular.ttf

2. Keep it beside app.py

3. Run:
streamlit run app.py
"""
)