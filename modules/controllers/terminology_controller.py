# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

from typing import List, Dict

class TerminologyController:
    def __init__(self, forbidden_words: List[str] = None, preferred_words: List[str] = None):
        self.forbidden_words = forbidden_words or []
        self.preferred_words = preferred_words or []

    def check(self, pages: List[str]) -> List[Dict[str, str]]:
        issues = []
        for page_num, page_text in enumerate(pages, start=1):
            for word in self.forbidden_words:
                if word.lower() in page_text.lower():
                    issues.append({
                        "page": str(page_num),
                        "term": word,
                        "message": f"Forbidden term '{word}' found on page {page_num}."
                    })
        return issues
