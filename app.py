import os
import json
from flask import Flask, render_template, request, jsonify
import random
from models.user import User
from models.attention import Attention, calculate_final_nota
from utils.generate import generate_random_attention
from datetime import datetime

app = Flask(__name__)

users = User.from_json("""
[
    {"id": 1, "name": "Juan", "action": "depositar", "time": 5, "nota": "bueno"},
    {"id": 2, "name": "Maria", "action": "retirar", "time": 8, "nota": "excelente"},
    {"id": 3, "name": "Pedro", "action": "cambiar clave", "time": 3, "nota": "regular"},
    {"id": 4, "name": "Luisa", "action": "recuperar clave", "time": 4, "nota": "muy bueno"},
    {"id": 5, "name": "Carlos", "action": "crear cuenta", "time": 7, "nota": "malo"}
]
""")

attentions = {1: [], 2: [], 3: []}
records = {1: [], 2: [], 3: []}
current_day = 1

def save_json_to_file(data, filename):
    filepath = os.path.join('archivos', filename)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    ventanilla = data.get('ventanilla')
    num_attentions = random.randint(1, 15)
    new_attentions = []

    for _ in range(num_attentions):
        new_attention = generate_random_attention(users, ventanilla)
        attentions[ventanilla].append(new_attention)
        new_attentions.append(new_attention.to_dict())

    total_persons = len(attentions[ventanilla])
    total_time = sum(attention.duration() for attention in attentions[ventanilla])
    final_nota = calculate_final_nota(attentions[ventanilla])

    return jsonify({
        "new_attentions": new_attentions,
        "total_persons": total_persons,
        "total_time": total_time,
        "final_nota": final_nota
    })

@app.route('/save', methods=['POST'])
def save():
    global current_day

    data = request.get_json()
    ventanilla = data.get('ventanilla')
    total_persons = data.get('total_persons')
    total_time = data.get('total_time')
    final_nota = data.get('final_nota')

    record = {
        "day": current_day,
        "total_persons": total_persons,
        "total_time": total_time,
        "final_nota": final_nota,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    records[ventanilla].append(record)
    attentions[ventanilla].clear()

    # Save record to JSON file
    save_json_to_file(records, f'records_day_{current_day}.json')

    current_day += 1

    return jsonify({"message": "Atención guardada correctamente", "day": current_day})

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    ventanilla = data.get('ventanilla')
    attentions[ventanilla].clear()
    return jsonify({"message": "Atención eliminada correctamente"})

@app.route('/delete_record', methods=['POST'])
def delete_record():
    data = request.get_json()
    ventanilla = data.get('ventanilla')
    day = data.get('day')

    for i, record in enumerate(records[ventanilla]):
        if record['day'] == day:
            del records[ventanilla][i]
            break

    # Save updated records to JSON file
    save_json_to_file(records, f'records_day_{day}_updated.json')

    return jsonify({"message": "Registro eliminado correctamente"})

@app.route('/compare')
def compare():
    return render_template('compare.html', records=records)

if __name__ == '__main__':
    if not os.path.exists('archivos'):
        os.makedirs('archivos')
    app.run(debug=True)
