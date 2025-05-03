import io
from typing import List, Dict

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

from pdf_signature_service import PdfSignatureService


if __name__ == "__main__":
    pdf_sign = {
        "posX": 20,
        "posY": 200,
        "width": 100,
        "height": 50,
        "pages": []  # firmar todas las páginas
    }

    input_pdf_path = "pdf/original/pdf1.pdf"
    output_pdf_path = "pdf/signed/pdf1_signed.pdf"
    signature_image_path = "pdf/original/sign.png"

    service = PdfSignatureService(
        signature_image_path=signature_image_path,
        posX=pdf_sign["posX"],
        posY=pdf_sign["posY"],
        width=pdf_sign["width"],
        height=pdf_sign["height"],
        pages=pdf_sign["pages"],
    )

    service.sign(input_pdf_path, output_pdf_path)
