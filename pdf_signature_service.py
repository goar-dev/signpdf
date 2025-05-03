import io
from typing import List, Dict

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas



class PdfSignatureService:
    """
    Servicio para superponer una imagen de firma en un PDF.
    """

    def __init__(
        self,
        signature_image_path: str,
        posX: int,
        posY: int,
        width: int,
        height: int,
        pages: List[int] = None,
    ):
        """
        :param signature_image_path: Ruta a la imagen de la firma.
        :param posX: Coordenada X donde colocar la firma.
        :param posY: Coordenada Y donde colocar la firma.
        :param width: Ancho de la firma en puntos.
        :param height: Alto de la firma en puntos.
        :param pages: Páginas (1-based) donde aplicar la firma; None o [] para todas.
        """
        self.signature_image_path = signature_image_path
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.pages = set(pages) if pages else None

    def sign(
        self,
        input_pdf_path: str,
        output_pdf_path: str,
    ) -> None:
        """
        Aplica la firma sobre el PDF de entrada y guarda el resultado.

        :param input_pdf_path: Ruta al PDF original.
        :param output_pdf_path: Ruta donde guardar el PDF firmado.
        """
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        total_pages = len(reader.pages)
        # Determinar páginas objetivo (0-based)
        if self.pages:
            target = {p - 1 for p in self.pages if 1 <= p <= total_pages}
        else:
            target = set(range(total_pages))

        for idx, page in enumerate(reader.pages):
            if idx in target:
                packet = io.BytesIO()
                media_box = page.mediabox
                page_w = float(media_box.width)
                page_h = float(media_box.height)

                overlay = canvas.Canvas(packet, pagesize=(page_w, page_h))
                overlay.drawImage(
                    self.signature_image_path,
                    self.posX,
                    self.posY,
                    width=self.width,
                    height=self.height,
                    mask="auto",
                )
                overlay.save()

                packet.seek(0)
                overlay_pdf = PdfReader(packet)
                overlay_page = overlay_pdf.pages[0]
                page.merge_page(overlay_page)

            writer.add_page(page)

        with open(output_pdf_path, "wb") as f:
            writer.write(f)