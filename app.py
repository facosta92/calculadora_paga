from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

salarios_base = {
    "mensajero": 1025,
    "ciclomensajero": 1025,
    "conductor": 1100,
    "andarin": 1000
}

valores_unidad = {
    "mensajero": 1.78,
    "ciclomensajero": 1.35,
    "conductor": 1.50,
    "andarin": 1.25
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/calcular', methods=['POST'])
def calcular_paga():
    data = request.get_json()
    categoria = data.get("categoria", "mensajero")
    unidades_trabajo = float(data.get("unidadesTrabajo", 0))
    horas_extras = float(data.get("horasExtras", 0))
    antiguedad = float(data.get("antiguedad", 0))
    festivos_trabajados = float(data.get("festivosTrabajados", 0))
    dias_vacaciones = float(data.get("diasVacaciones", 0))

    salario_base = salarios_base.get(categoria, 0)
    valor_unidad = valores_unidad.get(categoria, 0)

    salario = salario_base + (unidades_trabajo * valor_unidad)
    valor_hora_extra = (salario_base / 160) * 1.75
    salario += horas_extras * valor_hora_extra
    salario += antiguedad * 30
    salario += festivos_trabajados * 30
    salario -= (salario_base / 30) * dias_vacaciones

    return jsonify({"paga_calculada": round(salario, 2)})

if __name__ == '__main__':
    app.run(debug=True)