# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

from typing import List, Dict

class ConceptConsistencyController:
    def __init__(self, concept_groups: Dict[str, List[str]]):
        self.concept_groups = concept_groups

    def check(self, pages: List[str]) -> List[Dict[str, str]]:
        text = "\n".join(pages).lower()
        issues = []

        for concept_name, variants in self.concept_groups.items():
            found = set()
            for variant in variants:
                if variant.lower() in text:
                    found.add(variant.lower())

            if len(found) > 1:
                issues.append({
                    "concept": concept_name,
                    "variants": sorted(found),
                    "message": f"Inconsistent usage of concept '{concept_name}': found {', '.join(found)}"
                })

        return issues