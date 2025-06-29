# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

import re
from typing import List, Dict

class HeadingSequenceController:
    def __init__(self):
        self.heading_pattern = re.compile(r"^(\d+(?:\.\d+)*)(\s+)")

    def check(self, headings: List[str]) -> List[Dict[str, str]]:
        last = []
        issues = []

        for heading in headings:
            match = self.heading_pattern.match(heading.strip())
            if not match:
                continue

            current = [int(n) for n in match.group(1).split(".")]

            # Compare shared prefix
            for i in range(min(len(last), len(current)) - 1):
                if current[i] != last[i]:
                    break

            if len(last) == len(current) and current[:-1] == last[:-1]:
                if current[-1] != last[-1] + 1:
                    issues.append({
                        "heading": heading,
                        "message": f"Non-sequential heading: {'.'.join(map(str, current))} follows {'.'.join(map(str, last))}"
                    })

            last = current

        return issues