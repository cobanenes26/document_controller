# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

from typing import List, Dict

class EmptySectionController:
    def __init__(self, min_length: int = 30):
        self.min_length = min_length

    def check(self, pages: List[str], headings: List[str]) -> List[Dict[str, str]]:
        issues = []
        for heading in headings:
            section_text = self._extract_section_text(pages, heading)
            if section_text and len(section_text.strip()) < self.min_length:
                issues.append({
                    "heading": heading,
                    "message": f"Section '{heading}' seems empty or too short."
                })
        return issues

    def _extract_section_text(self, pages: List[str], heading: str) -> str:
        collecting = False
        collected = []

        for page in pages:
            for line in page.splitlines():
                if heading in line:
                    collecting = True
                    continue
                if collecting:
                    if line.strip() == "" or line.strip().isdigit():
                        continue
                    if any(char.isdigit() for char in line[:3]):
                        collecting = False
                        break
                    collected.append(line)
        return "\n".join(collected)