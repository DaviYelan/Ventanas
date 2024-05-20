import json

class User:
    def __init__(self, id, name, action, time, nota):
        self.id = id
        self.name = name
        self.action = action
        self.time = time
        self.nota = nota

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "action": self.action,
            "time": self.time,
            "nota": self.nota
        }

    @staticmethod
    def from_json(json_data):
        return [User(user["id"], user["name"], user["action"], user["time"], user["nota"]) for user in json.loads(json_data)]

