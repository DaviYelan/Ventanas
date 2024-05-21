from datetime import datetime
import random
from models.user import User
from models.attention import Attention, calculate_final_nota
from controls.generate import generate_random_attention
from controls.ventanillaDao import VentanillaDao

class VentanillaDaoControl:
    def __init__(self, users):
        self.users = users
        self.dao = VentanillaDao()

    def generate_attentions(self, ventanilla):
        num_attentions = random.randint(1, 15)
        new_attentions = []

        for _ in range(num_attentions):
            new_attention = generate_random_attention(self.users, ventanilla)
            self.dao.attentions[ventanilla].append(new_attention)
            new_attentions.append(new_attention.to_dict())

        total_persons = len(self.dao.attentions[ventanilla])
        total_time = sum(attention.duration() for attention in self.dao.attentions[ventanilla])
        final_nota = calculate_final_nota(self.dao.attentions[ventanilla])

        return new_attentions, total_persons, total_time, final_nota

    def save_day_record(self, ventanilla, total_persons, total_time, final_nota):
        record = {
            "day": self.dao.current_day,
            "total_persons": total_persons,
            "total_time": total_time,
            "final_nota": final_nota,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.dao.save_record(ventanilla, record)
        self.dao.clear_attentions(ventanilla)
        self.dao.save_json_to_file(self.dao.records, f'records_day_{self.dao.current_day}.json')
        self.dao.next_day()

    def delete_attentions(self, ventanilla):
        self.dao.clear_attentions(ventanilla)

    def delete_record(self, ventanilla, day):
        self.dao.delete_record(ventanilla, day)
