# ============================================================
# backend/utils.py
# ============================================================

import io


import qrcode
import zxingcpp


from PIL import (
    Image,
    UnidentifiedImageError
)


# ============================================================
# SUPPORTED IMAGE TYPES
# ============================================================

ALLOWED_IMAGE_TYPES = {

    "image/png",

    "image/jpeg",

    "image/jpg",

    "image/webp",

    "image/bmp"
}


# ============================================================
# GENERATE QR CODE
# ============================================================

def generate_qr_image(data: str) -> io.BytesIO:
    """
    Generate a QR Code image.

    Parameters
    ----------
    data : str
        Text or URL to encode.

    Returns
    -------
    io.BytesIO
        PNG image stored in memory.
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    data = data.strip()


    if not data:

        raise ValueError(
            "QR data cannot be empty."
        )


    # --------------------------------------------------------
    # Create QR Code
    # --------------------------------------------------------

    qr = qrcode.QRCode(

        version=None,

        error_correction=
            qrcode.constants.ERROR_CORRECT_H,

        box_size=10,

        border=4
    )


    # --------------------------------------------------------
    # Add data
    # --------------------------------------------------------

    qr.add_data(data)


    # --------------------------------------------------------
    # Generate QR Code
    # --------------------------------------------------------

    qr.make(

        fit=True
    )


    # --------------------------------------------------------
    # Create Pillow Image
    # --------------------------------------------------------

    qr_image = qr.make_image(

        fill_color="black",

        back_color="white"

    ).convert("RGB")


    # --------------------------------------------------------
    # Store PNG in memory
    # --------------------------------------------------------

    buffer = io.BytesIO()


    qr_image.save(

        buffer,

        format="PNG"
    )


    # Move pointer to beginning

    buffer.seek(0)


    return buffer


# ============================================================
# VALIDATE IMAGE TYPE
# ============================================================

def validate_image_type(content_type: str) -> bool:
    """
    Validate uploaded image MIME type.

    Parameters
    ----------
    content_type : str
        MIME type received from uploaded file.

    Returns
    -------
    bool
        True if image type is supported.
    """

    return content_type in ALLOWED_IMAGE_TYPES


# ============================================================
# OPEN IMAGE
# ============================================================

def open_image(file_bytes: bytes) -> Image.Image:
    """
    Open an image from raw bytes using Pillow.

    Parameters
    ----------
    file_bytes : bytes
        Uploaded image bytes.

    Returns
    -------
    PIL.Image.Image
        RGB Pillow image.

    Raises
    ------
    ValueError
        If file is not a valid image.
    """

    if not file_bytes:

        raise ValueError(
            "Uploaded file is empty."
        )


    try:

        image = Image.open(

            io.BytesIO(file_bytes)
        )


        # ----------------------------------------------------
        # Convert to RGB
        # ----------------------------------------------------

        image = image.convert("RGB")


        return image


    except UnidentifiedImageError:

        raise ValueError(
            "Uploaded file is not a valid image."
        )


# ============================================================
# DECODE QR CODE
# ============================================================

def decode_qr_image(image: Image.Image) -> list:
    """
    Decode QR/barcode information using ZXing-C++.

    Parameters
    ----------
    image : PIL.Image.Image
        Pillow image.

    Returns
    -------
    list
        List containing decoded QR results.
    """

    # --------------------------------------------------------
    # Make sure image is RGB
    # --------------------------------------------------------

    image = image.convert("RGB")


    # --------------------------------------------------------
    # Decode using ZXing-C++
    # --------------------------------------------------------

    results = zxingcpp.read_barcodes(

        image
    )


    decoded_results = []


    # --------------------------------------------------------
    # Process results
    # --------------------------------------------------------

    for result in results:

        if not result.text:

            continue


        decoded_results.append({

            "text":
                result.text,

            "format":
                str(result.format),

            "type":
                str(result.content_type)
        })


    return decoded_results


# ============================================================
# DECODE QR FROM BYTES
# ============================================================

def decode_qr_from_bytes(
    file_bytes: bytes
) -> list:
    """
    Open an uploaded image and decode its QR code.

    Parameters
    ----------
    file_bytes : bytes
        Uploaded image bytes.

    Returns
    -------
    list
        Decoded QR results.
    """

    image = open_image(

        file_bytes
    )


    return decode_qr_image(

        image
    )
