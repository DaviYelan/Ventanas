import os
import json
from datetime import datetime

class VentanillaDao:
    def __init__(self):
        self.attentions = {1: [], 2: [], 3: []}
        self.records = {1: [], 2: [], 3: []}
        self.current_day = 1

    def save_json_to_file(self, data, filename):
        filepath = os.path.join('archivos', filename)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def save_record(self, ventanilla, record):
        self.records[ventanilla].append(record)

    def clear_attentions(self, ventanilla):
        self.attentions[ventanilla].clear()

    def clear_records(self, ventanilla):
        self.records[ventanilla].clear()

    def delete_record(self, ventanilla, day):
        for i, record in enumerate(self.records[ventanilla]):
            if record['day'] == day:
                del self.records[ventanilla][i]
                break

    def next_day(self):
        self.current_day += 1
