# ============================================================
# app.py
# PragyanAI QR Code Generator & Decoder
# Streamlit Application
# ============================================================

import io

import qrcode
import zxingcpp

import streamlit as st

from PIL import (
    Image,
    UnidentifiedImageError
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title=
        "PragyanAI QR Code Generator & Decoder",

    page_icon="🔳",

    layout="wide",

    initial_sidebar_state="expanded"
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_NAME = (
    "PragyanAI QR Code Generator & Decoder"
)

APP_VERSION = "1.0.0"

MAX_UPLOAD_SIZE_MB = 5

MAX_UPLOAD_SIZE_BYTES = (
    MAX_UPLOAD_SIZE_MB * 1024 * 1024
)

ALLOWED_FILE_TYPES = [

    "png",

    "jpg",

    "jpeg",

    "webp",

    "bmp"
]


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(

    """
    <style>

    /* =====================================================
       GLOBAL
    ====================================================== */

    .main-title {

        font-size: 40px;

        font-weight: 700;

        text-align: center;

        margin-bottom: 5px;

    }


    .subtitle {

        text-align: center;

        font-size: 18px;

        color: #6b7280;

        margin-bottom: 25px;

    }


    .section-title {

        font-size: 26px;

        font-weight: 700;

        margin-top: 10px;

        margin-bottom: 15px;

    }


    .info-card {

        padding: 18px;

        border-radius: 12px;

        background-color: #f8fafc;

        border: 1px solid #e5e7eb;

        margin-bottom: 15px;

    }


    .footer {

        text-align: center;

        margin-top: 50px;

        padding: 25px;

        color: #6b7280;

        font-size: 14px;

    }


    /* =====================================================
       RESPONSIVE
       ====================================================== */

    @media (max-width: 768px) {

        .main-title {

            font-size: 28px;

        }

        .subtitle {

            font-size: 15px;

        }

    }

    </style>
    """,

    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(

    f"""
    <div class="main-title">

        🔳 {APP_NAME}

    </div>

    <div class="subtitle">

        Generate • Download • Decode QR Codes

        <br>

        Python + Streamlit + QRCode + Pillow + ZXing-C++

    </div>
    """,

    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Application")

    st.write(
        f"**Version:** {APP_VERSION}"
    )

    st.divider()

    st.subheader("Technology Stack")

    st.write("🐍 Python")

    st.write("🎈 Streamlit")

    st.write("🔳 QRCode")

    st.write("🖼️ Pillow")

    st.write("🔍 ZXing-C++")

    st.divider()

    st.subheader("Features")

    st.write("✅ Generate QR Code")

    st.write("✅ Download QR Code")

    st.write("✅ Upload QR Image")

    st.write("✅ Decode QR Code")

    st.write("✅ Detect Multiple QR Codes")

    st.write("✅ URL Detection")

    st.write("✅ Image Validation")

    st.write("❌ OpenCV Not Used")


# ============================================================
# SESSION STATE
# ============================================================

if "generated_qr" not in st.session_state:

    st.session_state.generated_qr = None


if "generated_data" not in st.session_state:

    st.session_state.generated_data = ""


# ============================================================
# MAIN APPLICATION
# ============================================================

generate_column, decode_column = st.columns(

    2,

    gap="large"
)


# ============================================================
# COLUMN 1
# QR GENERATOR
# ============================================================

with generate_column:

    st.markdown(

        '<div class="section-title">'
        '1️⃣ Generate QR Code'
        '</div>',

        unsafe_allow_html=True
    )


    st.write(

        "Enter a URL, text or any information "
        "that you want to convert into a QR Code."
    )


    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    qr_data = st.text_area(

        "URL or Information",

        placeholder=(
            "Example: https://pragyanai.com"
        ),

        height=150,

        max_chars=5000,

        key="qr_data"
    )


    # --------------------------------------------------------
    # CHARACTER COUNT
    # --------------------------------------------------------

    st.caption(

        f"Characters: {len(qr_data)} / 5000"
    )


    # --------------------------------------------------------
    # GENERATE BUTTON
    # --------------------------------------------------------

    generate_button = st.button(

        "🔳 Generate QR Code",

        type="primary",

        use_container_width=True
    )


    # --------------------------------------------------------
    # GENERATE QR
    # --------------------------------------------------------

    if generate_button:

        data = qr_data.strip()


        if not data:

            st.error(

                "Please enter a URL or information."
            )


        else:

            try:

                # --------------------------------------------
                # Create QR Code
                # --------------------------------------------

                qr = qrcode.QRCode(

                    version=None,

                    error_correction=
                        qrcode.constants.ERROR_CORRECT_H,

                    box_size=10,

                    border=4
                )


                # --------------------------------------------
                # Add data
                # --------------------------------------------

                qr.add_data(

                    data
                )


                # --------------------------------------------
                # Generate QR
                # --------------------------------------------

                qr.make(

                    fit=True
                )


                # --------------------------------------------
                # Create Pillow Image
                # --------------------------------------------

                qr_image = qr.make_image(

                    fill_color="black",

                    back_color="white"

                ).convert("RGB")


                # --------------------------------------------
                # Convert image to bytes
                # --------------------------------------------

                buffer = io.BytesIO()


                qr_image.save(

                    buffer,

                    format="PNG"
                )


                buffer.seek(0)


                # --------------------------------------------
                # Store in session state
                # --------------------------------------------

                st.session_state.generated_qr = (

                    buffer.getvalue()
                )


                st.session_state.generated_data = (

                    data
                )


                st.success(

                    "QR Code generated successfully!"
                )


            except Exception as error:

                st.error(

                    f"QR generation failed: {error}"
                )


    # ========================================================
    # DISPLAY GENERATED QR
    # ========================================================

    if st.session_state.generated_qr:

        st.divider()


        st.subheader(

            "Generated QR Code"
        )


        # ----------------------------------------------------
        # Display Image
        # ----------------------------------------------------

        st.image(

            st.session_state.generated_qr,

            caption="Generated QR Code",

            width=300
        )


        # ----------------------------------------------------
        # Show Original Data
        # ----------------------------------------------------

        st.write(

            "**Encoded Information:**"
        )


        st.code(

            st.session_state.generated_data,

            language="text"
        )


        # ----------------------------------------------------
        # Download
        # ----------------------------------------------------

        st.download_button(

            label=
                "⬇️ Download QR Code",

            data=
                st.session_state.generated_qr,

            file_name=
                "generated_qr_code.png",

            mime=
                "image/png",

            use_container_width=True
        )


# ============================================================
# COLUMN 2
# QR DECODER
# ============================================================

with decode_column:

    st.markdown(

        '<div class="section-title">'
        '2️⃣ Decode QR Code'
        '</div>',

        unsafe_allow_html=True
    )


    st.write(

        "Upload an existing QR Code image "
        "and decode the information."
    )


    # --------------------------------------------------------
    # FILE UPLOADER
    # --------------------------------------------------------

    uploaded_file = st.file_uploader(

        "Upload QR Code Image",

        type=ALLOWED_FILE_TYPES,

        help=(
            f"Supported formats: PNG, JPG, JPEG, "
            f"WEBP, BMP | Maximum size: "
            f"{MAX_UPLOAD_SIZE_MB} MB"
        )
    )


    # ========================================================
    # FILE SELECTED
    # ========================================================

    if uploaded_file:

        # ----------------------------------------------------
        # File Size
        # ----------------------------------------------------

        file_size = uploaded_file.size


        file_size_mb = (

            file_size /

            (1024 * 1024)

        )


        # ----------------------------------------------------
        # Display File Information
        # ----------------------------------------------------

        st.info(

            f"File: {uploaded_file.name}  |  "
            f"Size: {file_size_mb:.2f} MB"
        )


        # ----------------------------------------------------
        # Validate File Size
        # ----------------------------------------------------

        if file_size > MAX_UPLOAD_SIZE_BYTES:

            st.error(

                f"File is too large. "
                f"Maximum allowed size is "
                f"{MAX_UPLOAD_SIZE_MB} MB."
            )


        else:

            try:

                # ------------------------------------------------
                # Read File
                # ------------------------------------------------

                image_bytes = (

                    uploaded_file.getvalue()
                )


                # ------------------------------------------------
                # Open Image
                # ------------------------------------------------

                image = Image.open(

                    io.BytesIO(image_bytes)
                )


                # ------------------------------------------------
                # Convert to RGB
                # ------------------------------------------------

                image = image.convert(

                    "RGB"
                )


                # ------------------------------------------------
                # Display Preview
                # ------------------------------------------------

                st.subheader(

                    "Image Preview"
                )


                st.image(

                    image,

                    caption=uploaded_file.name,

                    width=300
                )


                # ------------------------------------------------
                # Decode Button
                # ------------------------------------------------

                decode_button = st.button(

                    "🔍 Decode QR Code",

                    type="primary",

                    use_container_width=True
                )


                # =================================================
                # DECODE
                # =================================================

                if decode_button:

                    try:

                        # -----------------------------------------
                        # ZXing-C++ Detection
                        # -----------------------------------------

                        results = (

                            zxingcpp.read_barcodes(

                                image

                            )

                        )


                        # -----------------------------------------
                        # No Result
                        # -----------------------------------------

                        if not results:

                            st.warning(

                                "No QR Code detected "
                                "in the image."
                            )


                        else:

                            # -------------------------------------
                            # Extract Readable Results
                            # -------------------------------------

                            decoded_results = []


                            for result in results:

                                if result.text:

                                    decoded_results.append({

                                        "text":
                                            result.text,

                                        "format":
                                            str(
                                                result.format
                                            ),

                                        "type":
                                            str(
                                                result.content_type
                                            )
                                    })


                            # -------------------------------------
                            # No Readable Result
                            # -------------------------------------

                            if not decoded_results:

                                st.warning(

                                    "QR Code was detected, "
                                    "but no readable data "
                                    "was found."
                                )


                            else:

                                st.success(

                                    "QR Code decoded successfully!"
                                )


                                st.write(

                                    f"**QR Codes detected:** "
                                    f"{len(decoded_results)}"
                                )


                                # =================================
                                # DISPLAY ALL RESULTS
                                # =================================

                                for (

                                    index,

                                    result

                                ) in enumerate(

                                    decoded_results,

                                    start=1

                                ):

                                    st.markdown(

                                        f"### 🔳 QR Result {index}"
                                    )


                                    # -----------------------------
                                    # Decoded Data
                                    # -----------------------------

                                    st.write(

                                        "**Decoded Information:**"
                                    )


                                    st.code(

                                        result["text"],

                                        language="text"
                                    )


                                    # -----------------------------
                                    # Metadata
                                    # -----------------------------

                                    col1, col2 = st.columns(2)


                                    with col1:

                                        st.write(
                                            "**Format**"
                                        )

                                        st.code(

                                            result["format"]
                                        )


                                    with col2:

                                        st.write(
                                            "**Content Type**"
                                        )

                                        st.code(

                                            result["type"]
                                        )


                                    # -----------------------------
                                    # URL Detection
                                    # -----------------------------

                                    if is_valid_url(

                                        result["text"]

                                    ):

                                        st.link_button(

                                            "🌐 Open URL",

                                            result["text"],

                                            use_container_width=True
                                        )


            except UnidentifiedImageError:

                st.error(

                    "The uploaded file is not "
                    "a valid image."
                )


            except Exception as error:

                st.error(

                    f"Unable to process image: {error}"
                )


# ============================================================
# TEST GENERATED QR
# ============================================================

st.divider()


st.markdown(

    '<div class="section-title">'
    '3️⃣ Test Generated QR'
    '</div>',

    unsafe_allow_html=True
)


st.write(

    "Generate a QR Code and then test whether "
    "ZXing-C++ can decode it."
)


if st.session_state.generated_qr:

    test_button = st.button(

        "🔍 Decode Generated QR",

        use_container_width=True
    )


    if test_button:

        try:

            # ------------------------------------------------
            # Open generated image
            # ------------------------------------------------

            generated_image = Image.open(

                io.BytesIO(

                    st.session_state.generated_qr

                )

            ).convert("RGB")


            # ------------------------------------------------
            # Decode
            # ------------------------------------------------

            results = (

                zxingcpp.read_barcodes(

                    generated_image

                )

            )


            # ------------------------------------------------
            # Process results
            # ------------------------------------------------

            if not results:

                st.error(

                    "Generated QR Code could "
                    "not be decoded."
                )


            else:

                successful_results = [

                    result.text

                    for result in results

                    if result.text

                ]


                if successful_results:

                    st.success(

                        "Generated QR Code "
                        "decoded successfully!"
                    )


                    for result in successful_results:

                        st.code(

                            result,

                            language="text"
                        )


                else:

                    st.warning(

                        "QR Code detected but "
                        "no readable information "
                        "was found."
                    )


        except Exception as error:

            st.error(

                f"QR decoding failed: {error}"
            )

else:

    st.info(

        "Generate a QR Code first."
    )


# ============================================================
# APPLICATION ARCHITECTURE
# ============================================================

st.divider()


st.markdown(

    '<div class="section-title">'
    '4️⃣ Application Architecture'
    '</div>',

    unsafe_allow_html=True
)


architecture_col1, architecture_col2 = st.columns(2)


# ============================================================
# GENERATION ARCHITECTURE
# ============================================================

with architecture_col1:

    st.subheader(

        "🔳 QR Generation"
    )


    st.code(

        """
User Input
    ↓
Streamlit
    ↓
QRCode
    ↓
Pillow
    ↓
PNG Image
    ↓
Download
        """,

        language="text"
    )


# ============================================================
# DECODING ARCHITECTURE
# ============================================================

with architecture_col2:

    st.subheader(

        "🔍 QR Decoding"
    )


    st.code(

        """
Upload Image
    ↓
Streamlit
    ↓
Pillow
    ↓
ZXing-C++
    ↓
Decoded Data
    ↓
Display Result
        """,

        language="text"
    )


# ============================================================
# ADVANCED VERSION ARCHITECTURE
# ============================================================

st.subheader(

    "🚀 Advanced Web Architecture"
)


st.code(

    """
                 USER
                   │
                   ▼
          HTML + CSS + JavaScript
                   │
                   ▼
                Netlify
                   │
              REST API / JSON
                   │
                   ▼
                FastAPI
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
       QRCode    Pillow   ZXing-C++
          │        │        │
          └────────┼────────┘
                   ▼
                Result
    """,

    language="text"
)


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.divider()


st.markdown(

    '<div class="section-title">'
    '5️⃣ Technology Stack'
    '</div>',

    unsafe_allow_html=True
)


technology_data = {

    "Programming Language":
        "Python",

    "Application Framework":
        "Streamlit",

    "Advanced Backend":
        "FastAPI",

    "Frontend":
        "HTML + CSS + JavaScript",

    "QR Generation":
        "QRCode",

    "Image Processing":
        "Pillow",

    "QR Decoding":
        "ZXing-C++",

    "Data Format":
        "JSON",

    "Image Format":
        "PNG",

    "Frontend Deployment":
        "Netlify",

    "OpenCV":
        "Not Used"

}


# ============================================================
# TECHNOLOGY TABLE
# ============================================================

for technology, value in technology_data.items():

    col1, col2 = st.columns(

        [1, 2]
    )


    with col1:

        st.write(

            f"**{technology}**"
        )


    with col2:

        st.write(

            value
        )


# ============================================================
# LEARNING OBJECTIVES
# ============================================================

st.divider()


st.markdown(

    '<div class="section-title">'
    '6️⃣ Learning Objectives'
    '</div>',

    unsafe_allow_html=True
)


learning_col1, learning_col2 = st.columns(2)


with learning_col1:

    st.subheader(

        "Python Skills"
    )


    st.write(

        """
        • Functions

        • Modules

        • Exception Handling

        • File Handling

        • JSON

        • Python Libraries

        • Virtual Environments
        """
    )


with learning_col2:

    st.subheader(

        "Application Skills"
    )


    st.write(

        """
        • Streamlit

        • FastAPI

        • REST API

        • JSON

        • File Upload

        • Image Processing

        • API Integration
        """
    )


# ============================================================
# PROJECT PROGRESSION
# ============================================================

st.divider()


st.markdown(

    '<div class="section-title">'
    '7️⃣ Student Learning Progression'
    '</div>',

    unsafe_allow_html=True
)


st.code(

    """
Python Basics
      ↓
Python Application
      ↓
Streamlit
      ↓
HTML + CSS + JavaScript
      ↓
REST API
      ↓
FastAPI
      ↓
Frontend + Backend
      ↓
GitHub
      ↓
Cloud Deployment
      ↓
Production Application
    """,

    language="text"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(

    f"""
    <div class="footer">

        <strong>
            {APP_NAME}
        </strong>

        <br><br>

        Version {APP_VERSION}

        <br>

        Built with:

        Python + Streamlit + QRCode
        + Pillow + ZXing-C++

        <br><br>

        OpenCV: Not Used

    </div>
    """,

    unsafe_allow_html=True
)
