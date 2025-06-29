# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

import fitz  # PyMuPDF
from typing import List, Dict

class ImageQualityController:
    def __init__(self, min_dpi: int = 150):
        self.min_dpi = min_dpi

    def check(self, pdf_path) -> List[Dict[str, str]]:
        issues = []
        doc = fitz.open(pdf_path)

        for page_index in range(len(doc)):
            page = doc[page_index]
            images = page.get_images(full=True)

            for img_index, img in enumerate(images):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)

                xres = pix.xres
                yres = pix.yres

                if xres < self.min_dpi or yres < self.min_dpi:
                    issues.append({
                        "page": str(page_index + 1),
                        "dpi": f"{xres}x{yres}",
                        "message": f"Low DPI image found on page {page_index + 1}: {xres}x{yres} dpi"
                    })

                pix = None

        return issues
