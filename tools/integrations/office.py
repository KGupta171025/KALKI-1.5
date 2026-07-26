import csv
from typing import List, Dict, Any

class OfficeDocHelper:
    """
    Utility helpers to parse and export tabular data files.
    """
    @staticmethod
    def parse_csv_file(file_path: str) -> List[List[str]]:
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                return list(reader)
        except Exception as e:
            print(f"[Office Helper] Failed to parse CSV: {str(e)}")
            return []

    @staticmethod
    def write_csv_file(file_path: str, data: List[List[Any]]) -> bool:
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"[Office Helper] Failed to write CSV: {str(e)}")
            return False

office_helper = OfficeDocHelper()
