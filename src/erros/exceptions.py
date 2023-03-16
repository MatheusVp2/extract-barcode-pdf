class ConvertPdfToImageException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ExtractBarcodeFromPdfImageException(Exception):
    def __init__(self, message):
        super().__init__(message)
