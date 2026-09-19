// ============================================================
// PragyanAI QR Code Generator & Decoder
// script.js
// ============================================================


// ============================================================
// FASTAPI BACKEND URL
// ============================================================

// ------------------------------------------------------------
// LOCAL DEVELOPMENT
// ------------------------------------------------------------
//
// const API_URL = "http://127.0.0.1:8000";
//
// ------------------------------------------------------------


// ------------------------------------------------------------
// PRODUCTION
// ------------------------------------------------------------
//
// Replace this URL with your deployed FastAPI backend.
//
// Example:
//
// const API_URL = "https://your-fastapi-backend.onrender.com";
//
// ------------------------------------------------------------

const API_URL ="https://pragyanai-super30-python-project-qrcode.onrender.com";

console.log("QR API URL:", API_URL);
// ============================================================
// DOM ELEMENTS
// ============================================================

const qrData =
    document.getElementById("qrData");

const generateButton =
    document.getElementById("generateButton");

const generateMessage =
    document.getElementById("generateMessage");

const qrContainer =
    document.getElementById("qrContainer");

const qrImage =
    document.getElementById("qrImage");

const downloadButton =
    document.getElementById("downloadButton");

const decodeGeneratedButton =
    document.getElementById(
        "decodeGeneratedButton"
    );

const decodedGenerated =
    document.getElementById(
        "decodedGenerated"
    );

const qrFile =
    document.getElementById("qrFile");

const uploadedPreview =
    document.getElementById(
        "uploadedPreview"
    );

const previewImage =
    document.getElementById(
        "previewImage"
    );

const decodeUploadButton =
    document.getElementById(
        "decodeUploadButton"
    );

const decodeMessage =
    document.getElementById(
        "decodeMessage"
    );

const decodedUploaded =
    document.getElementById(
        "decodedUploaded"
    );

const apiStatus =
    document.getElementById(
        "apiStatus"
    );

const statusIndicator =
    document.getElementById(
        "statusIndicator"
    );

const swaggerLink =
    document.getElementById(
        "swaggerLink"
    );

const characterCount =
    document.getElementById(
        "characterCount"
    );


// ============================================================
// APPLICATION STATE
// ============================================================

let generatedQRBlob = null;

let generatedQRURL = null;


// ============================================================
// CHARACTER COUNT
// ============================================================

qrData.addEventListener(
    "input",
    function () {

        characterCount.textContent =
            qrData.value.length;

    }
);


// ============================================================
// INITIALIZE
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        checkAPIStatus();

        swaggerLink.href =
            `${API_URL}/docs`;

    }
);


// ============================================================
// CHECK API STATUS
// ============================================================

async function checkAPIStatus() {

    try {

        apiStatus.textContent =
            "Checking backend...";

        statusIndicator.className =
            "status-indicator checking";


        const response =
            await fetch(
                `${API_URL}/health`
            );


        if (!response.ok) {

            throw new Error(
                "Backend returned an error."
            );

        }


        const result =
            await response.json();


        if (
            result.success &&
            result.status === "healthy"
        ) {

            apiStatus.textContent =
                "Backend API is online";

            statusIndicator.className =
                "status-indicator online";

        }

        else {

            apiStatus.textContent =
                "Backend API is unavailable";

            statusIndicator.className =
                "status-indicator offline";

        }

    }

    catch (error) {

        apiStatus.textContent =
            "Backend API is offline";

        statusIndicator.className =
            "status-indicator offline";

    }

}


// ============================================================
// GENERATE QR CODE
// ============================================================

generateButton.addEventListener(
    "click",
    generateQRCode
);


async function generateQRCode() {

    const data =
        qrData.value.trim();


    // --------------------------------------------------------
    // Validate input
    // --------------------------------------------------------

    if (!data) {

        showMessage(
            generateMessage,
            "Please enter a URL or information.",
            "error"
        );

        return;

    }


    // --------------------------------------------------------
    // Clear previous results
    // --------------------------------------------------------

    qrContainer.classList.add(
        "hidden"
    );

    decodedGenerated.innerHTML = "";


    // --------------------------------------------------------
    // Disable button
    // --------------------------------------------------------

    setButtonLoading(
        generateButton,
        true,
        "Generating..."
    );


    try {

        // ----------------------------------------------------
        // Send JSON request
        // ----------------------------------------------------

        const response =
            await fetch(
                `${API_URL}/generate`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        data: data

                    })

                }
            );


        // ----------------------------------------------------
        // Check response
        // ----------------------------------------------------

        if (!response.ok) {

            const errorData =
                await getErrorResponse(
                    response
                );

            throw new Error(
                errorData
            );

        }


        // ----------------------------------------------------
        // Receive PNG image
        // ----------------------------------------------------

        generatedQRBlob =
            await response.blob();


        // ----------------------------------------------------
        // Create browser URL
        // ----------------------------------------------------

        if (generatedQRURL) {

            URL.revokeObjectURL(
                generatedQRURL
            );

        }


        generatedQRURL =
            URL.createObjectURL(
                generatedQRBlob
            );


        // ----------------------------------------------------
        // Display QR
        // ----------------------------------------------------

        qrImage.src =
            generatedQRURL;


        qrContainer.classList.remove(
            "hidden"
        );


        // ----------------------------------------------------
        // Download button
        // ----------------------------------------------------

        downloadButton.href =
            generatedQRURL;


        downloadButton.download =
            "generated_qr_code.png";


        // ----------------------------------------------------
        // Success message
        // ----------------------------------------------------

        showMessage(

            generateMessage,

            "QR Code generated successfully!",

            "success"

        );

    }

    catch (error) {

        showMessage(

            generateMessage,

            `QR generation failed: ${error.message}`,

            "error"

        );

    }

    finally {

        setButtonLoading(

            generateButton,

            false,

            "🔳 Generate QR Code"

        );

    }

}


// ============================================================
// DECODE GENERATED QR
// ============================================================

decodeGeneratedButton.addEventListener(
    "click",
    decodeGeneratedQR
);


async function decodeGeneratedQR() {

    if (!generatedQRBlob) {

        showResultMessage(

            decodedGenerated,

            "Please generate a QR Code first.",

            "error"

        );

        return;

    }


    setButtonLoading(

        decodeGeneratedButton,

        true,

        "Decoding..."

    );


    try {

        // ----------------------------------------------------
        // Create File
        // ----------------------------------------------------

        const qrFileObject =
            new File(

                [
                    generatedQRBlob
                ],

                "generated_qr_code.png",

                {
                    type:
                        "image/png"
                }

            );


        // ----------------------------------------------------
        // Create FormData
        // ----------------------------------------------------

        const formData =
            new FormData();


        formData.append(
            "file",
            qrFileObject
        );


        // ----------------------------------------------------
        // Send request
        // ----------------------------------------------------

        const response =
            await fetch(

                `${API_URL}/decode`,

                {

                    method: "POST",

                    body: formData

                }

            );


        // ----------------------------------------------------
        // Process response
        // ----------------------------------------------------

        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(

                result.detail ||
                result.message ||
                "Decoding failed."

            );

        }


        // ----------------------------------------------------
        // Display result
        // ----------------------------------------------------

        displayDecodedResult(

            decodedGenerated,

            result

        );

    }

    catch (error) {

        showResultMessage(

            decodedGenerated,

            `QR decoding failed: ${error.message}`,

            "error"

        );

    }

    finally {

        setButtonLoading(

            decodeGeneratedButton,

            false,

            "🔍 Decode Generated QR"

        );

    }

}


// ============================================================
// FILE SELECTION
// ============================================================

qrFile.addEventListener(

    "change",

    handleFileSelection

);


function handleFileSelection() {

    decodedUploaded.innerHTML = "";

    decodeMessage.textContent = "";


    const file =
        qrFile.files[0];


    // --------------------------------------------------------
    // No file
    // --------------------------------------------------------

    if (!file) {

        uploadedPreview.classList.add(
            "hidden"
        );

        decodeUploadButton.disabled =
            true;

        return;

    }


    // --------------------------------------------------------
    // Maximum file size
    // --------------------------------------------------------

    const maxSize =
        5 * 1024 * 1024;


    if (file.size > maxSize) {

        showMessage(

            decodeMessage,

            "File size must be less than 5 MB.",

            "error"

        );


        uploadedPreview.classList.add(
            "hidden"
        );

        decodeUploadButton.disabled =
            true;

        qrFile.value = "";

        return;

    }


    // --------------------------------------------------------
    // Validate image type
    // --------------------------------------------------------

    const allowedTypes = [

        "image/png",

        "image/jpeg",

        "image/jpg",

        "image/webp",

        "image/bmp"

    ];


    if (
        !allowedTypes.includes(
            file.type
        )
    ) {

        showMessage(

            decodeMessage,

            "Please select a valid image file.",

            "error"

        );


        uploadedPreview.classList.add(
            "hidden"
        );

        decodeUploadButton.disabled =
            true;

        qrFile.value = "";

        return;

    }


    // --------------------------------------------------------
    // Preview image
    // --------------------------------------------------------

    const reader =
        new FileReader();


    reader.onload =
        function (event) {

            previewImage.src =
                event.target.result;

            uploadedPreview.classList.remove(
                "hidden"
            );

        };


    reader.readAsDataURL(
        file
    );


    // --------------------------------------------------------
    // Enable decode button
    // --------------------------------------------------------

    decodeUploadButton.disabled =
        false;


    showMessage(

        decodeMessage,

        "Image selected. Ready to decode.",

        "info"

    );

}


// ============================================================
// DECODE UPLOADED QR
// ============================================================

decodeUploadButton.addEventListener(

    "click",

    decodeUploadedQR

);


async function decodeUploadedQR() {

    const file =
        qrFile.files[0];


    if (!file) {

        showMessage(

            decodeMessage,

            "Please select a QR image.",

            "error"

        );

        return;

    }


    setButtonLoading(

        decodeUploadButton,

        true,

        "Decoding..."

    );


    try {

        // ----------------------------------------------------
        // FormData
        // ----------------------------------------------------

        const formData =
            new FormData();


        formData.append(
            "file",
            file
        );


        // ----------------------------------------------------
        // Send request
        // ----------------------------------------------------

        const response =
            await fetch(

                `${API_URL}/decode`,

                {

                    method: "POST",

                    body: formData

                }

            );


        // ----------------------------------------------------
        // Read JSON
        // ----------------------------------------------------

        const result =
            await response.json();


        // ----------------------------------------------------
        // Check response
        // ----------------------------------------------------

        if (!response.ok) {

            throw new Error(

                result.detail ||
                result.message ||
                "QR decoding failed."

            );

        }


        // ----------------------------------------------------
        // Display result
        // ----------------------------------------------------

        displayDecodedResult(

            decodedUploaded,

            result

        );


        if (result.success) {

            showMessage(

                decodeMessage,

                "QR Code decoded successfully!",

                "success"

            );

        }

        else {

            showMessage(

                decodeMessage,

                result.message ||
                "No QR Code found.",

                "error"

            );

        }

    }

    catch (error) {

        showMessage(

            decodeMessage,

            `QR decoding failed: ${error.message}`,

            "error"

        );

    }

    finally {

        setButtonLoading(

            decodeUploadButton,

            false,

            "🔍 Decode QR Code"

        );

    }

}


// ============================================================
// DISPLAY DECODED RESULT
// ============================================================

function displayDecodedResult(

    container,

    result

) {

    container.innerHTML = "";


    // --------------------------------------------------------
    // Failed result
    // --------------------------------------------------------

    if (!result.success) {

        showResultMessage(

            container,

            result.message ||
            "No QR Code detected.",

            "error"

        );

        return;

    }


    // --------------------------------------------------------
    // Main result
    // --------------------------------------------------------

    const wrapper =
        document.createElement(
            "div"
        );


    wrapper.className =
        "result-card";


    const title =
        document.createElement(
            "h4"
        );


    title.textContent =
        "✅ QR Code Decoded";


    wrapper.appendChild(
        title
    );


    // --------------------------------------------------------
    // Data
    // --------------------------------------------------------

    const data =
        document.createElement(
            "div"
        );


    data.className =
        "decoded-data";


    data.textContent =
        result.data || "";


    wrapper.appendChild(
        data
    );


    // --------------------------------------------------------
    // Metadata
    // --------------------------------------------------------

    const metadata =
        document.createElement(
            "div"
        );


    metadata.className =
        "result-meta";


    // Filename

    metadata.appendChild(

        createMetaItem(

            "Filename",

            result.filename ||
            "N/A"

        )

    );


    // Number of results

    metadata.appendChild(

        createMetaItem(

            "QR Codes Detected",

            result.count ||
            1

        )

    );


    // --------------------------------------------------------
    // First result metadata
    // --------------------------------------------------------

    if (
        result.results &&
        result.results.length > 0
    ) {

        const firstResult =
            result.results[0];


        metadata.appendChild(

            createMetaItem(

                "Format",

                firstResult.format ||
                "N/A"

            )

        );


        metadata.appendChild(

            createMetaItem(

                "Content Type",

                firstResult.type ||
                "N/A"

            )

        );

    }


    wrapper.appendChild(
        metadata
    );


    // --------------------------------------------------------
    // URL button
    // --------------------------------------------------------

    if (
        isValidURL(
            result.data
        )
    ) {

        const urlButton =
            document.createElement(
                "a"
            );


        urlButton.className =
            "url-button";


        urlButton.href =
            result.data;


        urlButton.target =
            "_blank";


        urlButton.rel =
            "noopener noreferrer";


        urlButton.textContent =
            "🌐 Open URL";


        wrapper.appendChild(
            urlButton
        );

    }


    // --------------------------------------------------------
    // Additional QR results
    // --------------------------------------------------------

    if (
        result.results &&
        result.results.length > 1
    ) {

        const additionalTitle =
            document.createElement(
                "h4"
            );


        additionalTitle.textContent =
            "Additional Results";


        additionalTitle.style.marginTop =
            "20px";


        wrapper.appendChild(
            additionalTitle
        );


        for (
            let i = 1;
            i < result.results.length;
            i++
        ) {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "decoded-data";


            item.textContent =
                result.results[i].text;


            wrapper.appendChild(
                item
            );

        }

    }


    container.appendChild(
        wrapper
    );

}


// ============================================================
// CREATE METADATA ITEM
// ============================================================

function createMetaItem(

    label,
    value

) {

    const item =
        document.createElement(
            "div"
        );


    item.className =
        "meta-item";


    const labelElement =
        document.createElement(
            "span"
        );


    labelElement.className =
        "meta-label";


    labelElement.textContent =
        label;


    const valueElement =
        document.createElement(
            "span"
        );


    valueElement.className =
        "meta-value";


    valueElement.textContent =
        value;


    item.appendChild(
        labelElement
    );


    item.appendChild(
        valueElement
    );


    return item;

}


// ============================================================
// URL VALIDATION
// ============================================================

function isValidURL(value) {

    if (!value) {

        return false;

    }


    try {

        const url =
            new URL(value);


        return (
            url.protocol === "http:" ||
            url.protocol === "https:"
        );

    }

    catch {

        return false;

    }

}


// ============================================================
// SHOW MESSAGE
// ============================================================

function showMessage(

    element,
    message,
    type

) {

    element.textContent =
        message;


    element.className =
        `message ${type}`;

}


// ============================================================
// SHOW RESULT MESSAGE
// ============================================================

function showResultMessage(

    element,
    message,
    type

) {

    element.innerHTML = "";


    const messageElement =
        document.createElement(
            "div"
        );


    messageElement.className =
        "message " + type;


    messageElement.textContent =
        message;


    element.appendChild(
        messageElement
    );

}


// ============================================================
// BUTTON LOADING STATE
// ============================================================

function setButtonLoading(

    button,
    loading,
    text

) {

    button.disabled =
        loading;


    button.textContent =
        text;

}


// ============================================================
// GET ERROR RESPONSE
// ============================================================

async function getErrorResponse(

    response

) {

    try {

        const result =
            await response.json();


        return (

            result.detail ||

            result.message ||

            `Server error (${response.status})`

        );

    }

    catch {

        return (
            `Server error (${response.status})`
        );

    }

}
