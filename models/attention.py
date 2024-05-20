from datetime import datetime
from collections import Counter

class Attention:
    def __init__(self, user, ventanilla):
        self.user = user
        self.ventanilla = ventanilla
        self.start_time = datetime.now()
        self.end_time = None

    def end_attention(self):
        self.end_time = datetime.now()

    def duration(self):
        return self.user.time

    def to_dict(self):
        return {
            "user": self.user.to_dict(),
            "ventanilla": self.ventanilla,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration(),
            "nota": self.user.nota
        }

def calculate_final_nota(attentions):
    notas = [attention.user.nota for attention in attentions]
    if not notas:
        return None
    nota_counter = Counter(notas)
    most_common_notas = nota_counter.most_common()
    highest_common = sorted(most_common_notas, key=lambda x: (x[1], x[0]), reverse=True)
    return highest_common[0][0]

