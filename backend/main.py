import io
import json

import qrcode
import zxingcpp

from PIL import Image

from fastapi import (
    FastAPI,
    File,
    UploadFile
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import (
    StreamingResponse
)

from pydantic import BaseModel


# ============================================================
# LOAD CONFIGURATION
# ============================================================

try:

    with open(
        "backend/config.json",
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

except FileNotFoundError:

    config = {
        "app_name": "QR Code Generator & Decoder",
        "version": "1.0.0"
    }


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title=config.get(
        "app_name",
        "QR Code Generator & Decoder"
    ),

    description=(
        "QR Code Generator and Decoder "
        "using FastAPI, Pillow and ZXing-C++"
    ),

    version=config.get(
        "version",
        "1.0.0"
    )
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QRRequest(BaseModel):

    data: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {

        "success": True,

        "message":
            "QR Code Generator & Decoder API is running",

        "version":
            config.get(
                "version",
                "1.0.0"
            ),

        "documentation": {

            "swagger":
                "/docs",

            "redoc":
                "/redoc"
        },

        "endpoints": {

            "generate":
                "POST /generate",

            "decode":
                "POST /decode",

            "health":
                "GET /health"
        }
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {

        "success": True,

        "status": "healthy",

        "message":
            "QR API is running"
    }


# ============================================================
# GENERATE QR CODE
# ============================================================

@app.post("/generate")
def generate_qr(
    request: QRRequest
):

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    data = request.data.strip()


    if not data:

        return {

            "success": False,

            "message":
                "URL or information is required."
        }


    try:

        # ----------------------------------------------------
        # Create QR Code
        # ----------------------------------------------------

        qr = qrcode.QRCode(

            version=1,

            error_correction=
                qrcode.constants.ERROR_CORRECT_H,

            box_size=10,

            border=4
        )


        # ----------------------------------------------------
        # Add data
        # ----------------------------------------------------

        qr.add_data(data)


        # ----------------------------------------------------
        # Generate QR
        # ----------------------------------------------------

        qr.make(
            fit=True
        )


        # ----------------------------------------------------
        # Create Pillow Image
        # ----------------------------------------------------

        qr_image = qr.make_image(

            fill_color="black",

            back_color="white"

        ).convert("RGB")


        # ----------------------------------------------------
        # Store image in memory
        # ----------------------------------------------------

        buffer = io.BytesIO()


        qr_image.save(

            buffer,

            format="PNG"
        )


        buffer.seek(0)


        # ----------------------------------------------------
        # Return PNG image
        # ----------------------------------------------------

        return StreamingResponse(

            buffer,

            media_type="image/png",

            headers={

                "Content-Disposition":
                    "inline; filename=generated_qr_code.png"
            }
        )


    except Exception as error:

        return {

            "success": False,

            "message":
                f"QR generation failed: {str(error)}"
        }


# ============================================================
# DECODE QR CODE
# ============================================================

@app.post("/decode")
async def decode_qr(

    file: UploadFile = File(...)
):

    try:

        # ----------------------------------------------------
        # Validate filename
        # ----------------------------------------------------

        if not file.filename:

            return {

                "success": False,

                "message":
                    "No file selected."
            }


        # ----------------------------------------------------
        # Read uploaded image
        # ----------------------------------------------------

        contents = await file.read()


        # ----------------------------------------------------
        # Open image using Pillow
        # ----------------------------------------------------

        image = Image.open(

            io.BytesIO(contents)

        ).convert("RGB")


        # ----------------------------------------------------
        # Decode using ZXing-C++
        # ----------------------------------------------------

        results = zxingcpp.read_barcodes(

            image
        )


        # ----------------------------------------------------
        # Check result
        # ----------------------------------------------------

        if not results:

            return {

                "success": False,

                "message":
                    "No QR Code detected in the image."
            }


        # ----------------------------------------------------
        # Get decoded information
        # ----------------------------------------------------

        decoded_data = results[0].text


        # ----------------------------------------------------
        # Return JSON response
        # ----------------------------------------------------

        return {

            "success": True,

            "data": decoded_data,

            "filename": file.filename
        }


    except Exception as error:

        return {

            "success": False,

            "message":
                f"QR decoding failed: {str(error)}"
        }


# ============================================================
# APPLICATION INFORMATION
# ============================================================

@app.get("/info")
def application_info():

    return {

        "application":
            config.get(
                "app_name",
                "QR Code Generator & Decoder"
            ),

        "version":
            config.get(
                "version",
                "1.0.0"
            ),

        "technologies": [

            "Python",

            "FastAPI",

            "QRCode",

            "Pillow",

            "ZXing-C++"
        ],

        "opencv_used": False
    }
