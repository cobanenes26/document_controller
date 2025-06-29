# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

import re
from typing import List, Dict

class FigureTableReferenceController:
    def __init__(self):
        self.figure_ref_pattern = re.compile(r"\bFigure\s+(\d+)\b")
        self.table_ref_pattern = re.compile(r"\bTable\s+(\d+)\b")
        self.figure_caption_pattern = re.compile(r"^Figure\s+(\d+):", re.IGNORECASE)
        self.table_caption_pattern = re.compile(r"^Table\s+(\d+):", re.IGNORECASE)

    def check(self, pages: List[str]) -> List[Dict[str, str]]:
        refs_figure = set()
        refs_table = set()
        defs_figure = set()
        defs_table = set()

        for page in pages:
            lines = page.splitlines()
            for line in lines:
                refs_figure.update(self.figure_ref_pattern.findall(line))
                refs_table.update(self.table_ref_pattern.findall(line))
                if self.figure_caption_pattern.match(line):
                    defs_figure.update(self.figure_caption_pattern.findall(line))
                if self.table_caption_pattern.match(line):
                    defs_table.update(self.table_caption_pattern.findall(line))

        issues = []

        for ref in sorted(refs_figure - defs_figure):
            issues.append({
                "type": "Figure",
                "ref": ref,
                "message": f"Figure {ref} is referenced but not defined."
            })

        for ref in sorted(refs_table - defs_table):
            issues.append({
                "type": "Table",
                "ref": ref,
                "message": f"Table {ref} is referenced but not defined."
            })

        return issues