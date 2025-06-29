# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

from typing import List

class ReportGenerator:
    def print_report(self, standard_name: str, missing_sections: List[str]) -> None:
        print(f"\nStandard Applied: {standard_name}")
        if missing_sections:
            print("\nMissing Sections:")
            for section in missing_sections:
                print(f" - {section}")
        else:
            print("All required sections are present.")