# ============================================================
# backend/main.py
# PragyanAI QR Code Generator & Decoder
# FastAPI Backend
# ============================================================

import json
from pathlib import Path

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse

from pydantic import BaseModel, Field

from utils import (
    generate_qr_image,
    validate_image_type,
    decode_qr_from_bytes
)


# ============================================================
# APPLICATION PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CONFIG_FILE = BASE_DIR / "config.json"


# ============================================================
# DEFAULT CONFIGURATION
# ============================================================

DEFAULT_CONFIG = {

    "app_name":
        "PragyanAI QR Code Generator & Decoder",

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

    """
    Load application configuration from config.json.
    """

    try:

        with open(

            CONFIG_FILE,

            "r",

            encoding="utf-8"

        ) as file:

            loaded_config = json.load(file)


        # ----------------------------------------------------
        # Merge loaded configuration with defaults
        # ----------------------------------------------------

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

            "WARNING: config.json contains invalid JSON. "
            "Using default configuration."
        )

        return DEFAULT_CONFIG


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

config = load_config()


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

    DEFAULT_CONFIG["cors_origins"]

)


MAX_UPLOAD_SIZE_MB = config.get(

    "max_upload_size_mb",

    DEFAULT_CONFIG["max_upload_size_mb"]

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

    """
    Root API endpoint.

    Returns basic information about the application,
    available endpoints and documentation.
    """

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

    """
    Health check endpoint.

    Useful for:
    - Cloud deployment
    - Monitoring
    - Testing
    - Load balancers
    """

    return {

        "success": True,

        "status":
            "healthy",

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

    """
    Generate a QR Code.

    Request JSON:

    {
        "data": "https://pragyanai.com"
    }

    Response:

    PNG image
    """

    # --------------------------------------------------------
    # Clean input
    # --------------------------------------------------------

    data = request.data.strip()


    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not data:

        raise HTTPException(

            status_code=400,

            detail=
                "URL or information is required."
        )


    try:

        # ----------------------------------------------------
        # Generate QR Image
        # ----------------------------------------------------

        qr_buffer = generate_qr_image(

            data
        )


        # ----------------------------------------------------
        # Return PNG Image
        # ----------------------------------------------------

        return StreamingResponse(

            qr_buffer,

            media_type="image/png",

            headers={

                "Content-Disposition":
                    "inline; "
                    "filename=generated_qr_code.png"
            }
        )


    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)
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

    """
    Decode QR Code from an uploaded image.

    Request:

    multipart/form-data

    Response:

    JSON
    """

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:

        raise HTTPException(

            status_code=400,

            detail=
                "No file selected."
        )


    # --------------------------------------------------------
    # Validate file type
    # --------------------------------------------------------

    if not validate_image_type(

        file.content_type or ""

    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "Unsupported image format. "
                "Please upload PNG, JPG, JPEG, "
                "WEBP or BMP."
            )
        )


    try:

        # ----------------------------------------------------
        # Read uploaded file
        # ----------------------------------------------------

        contents = await file.read()


        # ----------------------------------------------------
        # Check empty file
        # ----------------------------------------------------

        if not contents:

            raise HTTPException(

                status_code=400,

                detail=
                    "Uploaded file is empty."
            )


        # ----------------------------------------------------
        # Check file size
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
        # Decode QR
        # ----------------------------------------------------

        decoded_results = decode_qr_from_bytes(

            contents
        )


        # ----------------------------------------------------
        # No QR detected
        # ----------------------------------------------------

        if not decoded_results:

            return {

                "success": False,

                "data": None,

                "filename":
                    file.filename,

                "count": 0,

                "results": [],

                "message":
                    "No QR Code detected in the image."
            }


        # ----------------------------------------------------
        # First decoded result
        # ----------------------------------------------------

        first_result = decoded_results[0]


        # ----------------------------------------------------
        # Successful response
        # ----------------------------------------------------

        return {

            "success": True,

            "data":
                first_result["text"],

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


    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)
        )


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

    """
    Return application architecture and
    technology information.
    """

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

            "frontend_host":
                "Netlify",

            "backend":
                "FastAPI",

            "api_style":
                "REST API",

            "communication":
                "HTTPS",

            "request_format":
                "JSON / multipart-form-data",

            "response_format":
                "JSON / PNG"
        },

        "technologies": {

            "programming_language":
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
