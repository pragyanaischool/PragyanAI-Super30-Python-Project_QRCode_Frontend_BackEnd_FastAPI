import io
import json
from pathlib import Path

import qrcode
import zxingcpp

from PIL import Image, UnidentifiedImageError

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse

from pydantic import BaseModel, Field


# ============================================================
# APPLICATION PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CONFIG_FILE = BASE_DIR / "config.json"


# ============================================================
# APPLICATION DEFAULT CONFIGURATION
# ============================================================

DEFAULT_CONFIG = {

    "app_name":
        "QR Code Generator & Decoder",

    "version":
        "1.0.0",

    "description":
        "QR Code Generator and Decoder using "
        "FastAPI, Pillow and ZXing-C++",

    "cors_origins": [

        "*"
    ],

    "max_upload_size_mb":
        5
}


# ============================================================
# LOAD CONFIGURATION
# ============================================================

def load_config():

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            loaded_config = json.load(file)

            # Merge loaded configuration
            # with default configuration

            config = {
                **DEFAULT_CONFIG,
                **loaded_config
            }

            return config

    except FileNotFoundError:

        print(
            "WARNING: config.json not found. "
            "Using default configuration."
        )

        return DEFAULT_CONFIG

    except json.JSONDecodeError:

        print(
            "WARNING: Invalid config.json. "
            "Using default configuration."
        )

        return DEFAULT_CONFIG


# Load configuration

config = load_config()


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = config.get(
    "app_name",
    DEFAULT_CONFIG["app_name"]
)

APP_VERSION = config.get(
    "version",
    DEFAULT_CONFIG["version"]
)

APP_DESCRIPTION = config.get(
    "description",
    DEFAULT_CONFIG["description"]
)

CORS_ORIGINS = config.get(
    "cors_origins",
    ["*"]
)

MAX_UPLOAD_SIZE_MB = config.get(
    "max_upload_size_mb",
    5
)

MAX_UPLOAD_SIZE = (
    MAX_UPLOAD_SIZE_MB
    * 1024
    * 1024
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title=APP_NAME,

    description=APP_DESCRIPTION,

    version=APP_VERSION,

    docs_url="/docs",

    redoc_url="/redoc"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=CORS_ORIGINS,

    allow_credentials=False,

    allow_methods=[
        "GET",
        "POST"
    ],

    allow_headers=[
        "Content-Type"
    ]
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QRRequest(BaseModel):

    data: str = Field(

        ...,

        min_length=1,

        max_length=5000,

        description=
            "Text, URL or information to encode"
    )


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {

        "success": True,

        "message":
            "QR Code Generator & Decoder API is running",

        "application":
            APP_NAME,

        "version":
            APP_VERSION,

        "status":
            "online",

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
                "GET /health",

            "info":
                "GET /info"
        },

        "technologies": [

            "Python",

            "FastAPI",

            "QRCode",

            "Pillow",

            "ZXing-C++"
        ]
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {

        "success": True,

        "status": "healthy",

        "service":
            "QR Code API",

        "version":
            APP_VERSION,

        "components": {

            "fastapi":
                "running",

            "qrcode":
                "available",

            "pillow":
                "available",

            "zxing_cpp":
                "available"
        }
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

        raise HTTPException(

            status_code=400,

            detail=
                "URL or information is required."
        )


    try:

        # ----------------------------------------------------
        # Create QR Code
        # ----------------------------------------------------

        qr = qrcode.QRCode(

            version=None,

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
                    "inline; "
                    "filename=generated_qr_code.png"
            }
        )


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=
                f"QR generation failed: {str(error)}"
        )


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

            raise HTTPException(

                status_code=400,

                detail=
                    "No file selected."
            )


        # ----------------------------------------------------
        # Validate content type
        # ----------------------------------------------------

        allowed_types = {

            "image/png",

            "image/jpeg",

            "image/jpg",

            "image/webp",

            "image/bmp"
        }


        if file.content_type not in allowed_types:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Unsupported image format. "
                    "Please upload PNG, JPG, JPEG, "
                    "WEBP or BMP."
                )
            )


        # ----------------------------------------------------
        # Read uploaded image
        # ----------------------------------------------------

        contents = await file.read()


        # ----------------------------------------------------
        # Validate empty file
        # ----------------------------------------------------

        if not contents:

            raise HTTPException(

                status_code=400,

                detail=
                    "Uploaded file is empty."
            )


        # ----------------------------------------------------
        # Validate file size
        # ----------------------------------------------------

        if len(contents) > MAX_UPLOAD_SIZE:

            raise HTTPException(

                status_code=413,

                detail=(
                    f"File size exceeds the maximum "
                    f"allowed size of "
                    f"{MAX_UPLOAD_SIZE_MB} MB."
                )
            )


        # ----------------------------------------------------
        # Open image using Pillow
        # ----------------------------------------------------

        try:

            image = Image.open(

                io.BytesIO(contents)
            )

            image = image.convert("RGB")


        except UnidentifiedImageError:

            raise HTTPException(

                status_code=400,

                detail=
                    "Uploaded file is not a valid image."
            )


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

                "data": None,

                "filename":
                    file.filename,

                "message":
                    "No QR Code detected in the image."
            }


        # ----------------------------------------------------
        # Extract decoded results
        # ----------------------------------------------------

        decoded_results = []


        for result in results:

            if result.text:

                decoded_results.append({

                    "text":
                        result.text,

                    "format":
                        str(result.format),

                    "type":
                        str(result.content_type)
                })


        # ----------------------------------------------------
        # No readable data
        # ----------------------------------------------------

        if not decoded_results:

            return {

                "success": False,

                "data": None,

                "filename":
                    file.filename,

                "message":
                    "QR code detected, but no readable data found."
            }


        # ----------------------------------------------------
        # Return decoded information
        # ----------------------------------------------------

        return {

            "success": True,

            "data":
                decoded_results[0]["text"],

            "filename":
                file.filename,

            "count":
                len(decoded_results),

            "results":
                decoded_results,

            "message":
                "QR code decoded successfully."
        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=
                f"QR decoding failed: {str(error)}"
        )


# ============================================================
# APPLICATION INFORMATION
# ============================================================

@app.get("/info")
def application_info():

    return {

        "application":
            APP_NAME,

        "version":
            APP_VERSION,

        "description":
            APP_DESCRIPTION,

        "architecture": {

            "frontend":
                "HTML + CSS + JavaScript",

            "hosting_frontend":
                "Netlify",

            "backend":
                "FastAPI",

            "api_style":
                "REST API",

            "data_format":
                "JSON",

            "image_format":
                "PNG"
        },

        "technologies": {

            "language":
                "Python",

            "api_framework":
                "FastAPI",

            "qr_generation":
                "QRCode",

            "image_processing":
                "Pillow",

            "qr_decoding":
                "ZXing-C++"
        },

        "opencv_used":
            False
    }


# ============================================================
# RUN APPLICATION LOCALLY
# ============================================================

if __name__ == "__main__":

    import uvicorn


    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True
    )
    
