# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

import fitz  # install PyMuPDF
from pathlib import Path
from typing import List

class DocumentParser:
    def extract_headings(self, pdf_path: Path) -> List[str]:
        if not pdf_path.is_file():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        headings = set()
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text = page.get_text()
                for line in text.split("\n"):
                    if line.strip() and any(char.isalpha() for char in line):
                        headings.add(line.strip())
        return sorted(list(headings))