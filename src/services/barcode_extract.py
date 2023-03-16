from dataclasses import dataclass
from typing import List

from PIL.Image import Image
from erros import ConvertPdfToImageException, ExtractBarcodeFromPdfImageException
from pdf2image import convert_from_bytes
from pyzbar.pyzbar import decode, Decoded


@dataclass
class ResponseTicket:
    tipo_boleto: str
    codigo_de_barra: str


class ReaderBarcodeTicketPdf:

    @staticmethod
    def _ticket_is_payment(ticket_type: str) -> bool:
        return ticket_type == "I25"

    @staticmethod
    def _pdf_to_image(pdf_buffer: bytes) -> List[Image]:
        try:
            images = convert_from_bytes(pdf_buffer, poppler_path="./poppler/bin")
            if not len(images) >= 1:
                raise Exception("Não houve imagens convertidas.")
            return images
        except Exception as err:
            raise ConvertPdfToImageException(str(err))

    @staticmethod
    def _extract_barcode_from_image_pdf(image: Image) -> List[Decoded]:
        try:
            decoded = decode(image)
            if not len(decoded) >= 1:
                raise Exception("Não houve extração de codigos de barras.")
            return decoded
        except Exception as err:
            raise ExtractBarcodeFromPdfImageException(str(err))

    def reader(self, pdf_buffer: bytes, filter_type: str = "I25") -> List[ResponseTicket]:
        images = self._pdf_to_image(pdf_buffer=pdf_buffer)
        decoded = self._extract_barcode_from_image_pdf(image=images[0])
        filter_ticket = [item for item in decoded if item.type == filter_type]
        map_ticket = [ResponseTicket(tipo_boleto=item.type, codigo_de_barra=item.data.decode("utf-8"))
                    for item in filter_ticket]
        return map_ticket
