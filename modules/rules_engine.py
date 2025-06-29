# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

from typing import List

class RulesEngine:
    def __init__(self, config: dict):
        self.required_sections = config.get("required_sections", [])
        self.ignore_case = config.get("options", {}).get("ignore_case", True)
        self.allow_partial = config.get("options", {}).get("allow_partial_matches", True)

    def check_required_sections(self, headings: List[str]) -> List[str]:
        missing = []

        for required in self.required_sections:
            match_found = False
            for heading in headings:
                source = heading.lower() if self.ignore_case else heading
                target = required.lower() if self.ignore_case else required

                if self.allow_partial and target in source:
                    match_found = True
                    break
                if not self.allow_partial and target == source:
                    match_found = True
                    break

            if not match_found:
                missing.append(required)

        return missing