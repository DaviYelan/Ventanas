import os
from flask import Flask, render_template, request, jsonify
from controls.ventanillaDaoControl import VentanillaDaoControl
from models.user import User

app = Flask(__name__)

users = User.from_json("""
[
    {"id": 1, "name": "Juan", "action": "depositar", "time": 25, "nota": "bueno"},
    {"id": 2, "name": "Maria", "action": "retirar", "time": 38, "nota": "excelente"},
    {"id": 3, "name": "Pedro", "action": "cambiar clave", "time": 43, "nota": "regular"},
    {"id": 4, "name": "Luisa", "action": "recuperar clave", "time": 24, "nota": "muy bueno"},
    {"id": 5, "name": "Carlos", "action": "crear cuenta", "time": 37, "nota": "malo"},
    {"id": 6, "name": "Ana", "action": "depositar", "time": 26, "nota": "bueno"},
    {"id": 7, "name": "Mario", "action": "retirar", "time": 19, "nota": "excelente"},
    {"id": 8, "name": "Laura", "action": "cambiar clave", "time": 32, "nota": "regular"},
    {"id": 9, "name": "Diego", "action": "recuperar clave", "time": 23, "nota": "muy bueno"},
    {"id": 10, "name": "Carla", "action": "crear cuenta", "time": 15, "nota": "malo"}
]
""")

ventanilla_control = VentanillaDaoControl(users)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    ventanilla = data.get('ventanilla')

    new_attentions, total_persons, total_time, final_nota = ventanilla_control.generate_attentions(ventanilla)

    return jsonify({
        "new_attentions": new_attentions,
        "total_persons": total_persons,
        "total_time": total_time,
        "final_nota": final_nota
    })

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    ventanilla = data.get('ventanilla')
    total_persons = data.get('total_persons')
    total_time = data.get('total_time')
    final_nota = data.get('final_nota')

    ventanilla_control.save_day_record(ventanilla, total_persons, total_time, final_nota)

    return jsonify({"message": "Atención guardada correctamente", "day": ventanilla_control.dao.current_day})

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    ventanilla = data.get('ventanilla')
    ventanilla_control.delete_attentions(ventanilla)
    return jsonify({"message": "Atención eliminada correctamente"})

@app.route('/delete_record', methods=['POST'])
def delete_record():
    data = request.get_json()
    ventanilla = data.get('ventanilla')
    day = data.get('day')

    ventanilla_control.delete_record(ventanilla, day)

    return jsonify({"message": "Registro eliminado correctamente"})

@app.route('/compare')
def compare():
    return render_template('compare.html', records=ventanilla_control.dao.records)

if __name__ == '__main__':
    if not os.path.exists('archivos'):
        os.makedirs('archivos')
    app.run(debug=True)
