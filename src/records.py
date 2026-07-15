import json
import os
from typing import List, Dict, Any
from datetime import datetime
from src.config import RECORDS_FILE, MAX_RECORDS


class RecordsManager:
    def __init__(self):
        self.records_file = RECORDS_FILE
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.records_file), exist_ok=True)
            if not os.path.exists(self.records_file):
                with open(self.records_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                os.chmod(self.records_file, 0o666)
        except Exception:
            pass

    def load_records(self) -> List[Dict[str, Any]]:
        try:
            with open(self.records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_records(self, records: List[Dict[str, Any]]) -> None:
        try:
            os.makedirs(os.path.dirname(self.records_file), exist_ok=True)
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            os.chmod(self.records_file, 0o666)
        except Exception:
            pass

    def add_records(self, player_name: str, time_seconds: int,
                    rows: int, cols: int, mines: int) -> bool:
        try:
            records = self.load_records()

            record = {
                'player': player_name,
                'time': time_seconds,
                'rows': rows,
                'cols': cols,
                'mines': mines,
                'date': datetime.now().isoformat()
            }

            records.append(record)
            records.sort(key=lambda x: x['time'])

            best_records = {}
            for rec in records:
                key = f"{rec['rows']}x{rec['cols']}x{rec['mines']}"
                if key not in best_records or rec['time'] < best_records[key]['time']:
                    best_records[key] = rec

            all_records = list(best_records.values())
            all_records.sort(key=lambda x: x['time'])
            self.save_records(all_records[:MAX_RECORDS])
            return True
        except Exception:
            return False

    def get_best_time(self, rows: int, cols: int, mines: int):
        records = self.load_records()
        filtered = [r for r in records
                    if r['rows'] == rows and r['cols'] == cols and r['mines'] == mines]
        if filtered:
            return filtered[0]['time']
        return None

    def get_records_by_preset(self, rows: int, cols: int, mines: int) -> List[Dict[str, Any]]:
        records = self.load_records()
        return [r for r in records
                if r['rows'] == rows and r['cols'] == cols and r['mines'] == mines]