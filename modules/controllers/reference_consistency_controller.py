# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

import re
from typing import List, Dict

class ReferenceConsistencyController:
    def __init__(self, reference_heading_keywords: List[str] = None):
        self.ref_call_pattern = re.compile(r"\[(\d+)\]")
        self.reference_heading_keywords = reference_heading_keywords or ["references"]

    def check(self, pages: List[str], headings: List[str]) -> List[Dict[str, str]]:
        all_refs_called = set()
        all_refs_listed = set()
        in_reference_section = False

        for page in pages:
            all_refs_called.update(self.ref_call_pattern.findall(page))

        for page in pages:
            lines = page.lower().splitlines()
            for i, line in enumerate(lines):
                if any(h in line for h in self.reference_heading_keywords):
                    in_reference_section = True
                    continue
                if in_reference_section:
                    listed = self.ref_call_pattern.findall(line)
                    all_refs_listed.update(listed)

        missing = sorted(all_refs_called - all_refs_listed)

        issues = []
        for ref in missing:
            issues.append({
                "reference": ref,
                "message": f"Reference [{ref}] is used in the text but not defined in the reference list."
            })

        return issues