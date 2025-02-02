from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Datos de salario base según el convenio
SALARIOS_BASE = {
    "mensajero": 1097.98,
    "ciclomensajero": 1097.98,
    "conductor": 1097.98,
    "andarin": 1097.98
}

# Valores de retribución por unidad de obra (RUO) según la población
RUO = {
    "mas_1500000": {"urgente": 1.78, "standard": 1.35},
    "500001_1500000": {"urgente": 1.35, "standard": 1.10},
    "300001_500000": {"urgente": 1.22, "standard": 1.10},
    "150001_300000": {"urgente": 1.10, "standard": 1.10},
    "menos_150000": {"urgente": 1.04, "standard": 1.04}
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/calcular', methods=['POST'])
def calcular_paga():
    try:
        data = request.get_json()
        categoria = data.get("categoria")
        poblacion = data.get("poblacion")
        direcciones_por_hora = float(data.get("direccionesPorHora", 0))
        horas_por_dia = float(data.get("horasPorDia", 0))
        dias_trabajados = float(data.get("diasTrabajados", 0))
        km_recorridos = float(data.get("kmRecorridos", 0))
        horas_extras = float(data.get("horasExtras", 0))
        antiguedad = float(data.get("antiguedad", 0))
        festivos_trabajados = float(data.get("festivosTrabajados", 0))
        dias_vacaciones = float(data.get("diasVacaciones", 0))

        if categoria not in SALARIOS_BASE or poblacion not in RUO:
            return jsonify({"error": "Datos inválidos"}), 400

        salario_base = SALARIOS_BASE[categoria]
        valor_urgente = RUO[poblacion]["urgente"]
        valor_standard = RUO[poblacion]["standard"]
        
        # Calcular total de direcciones al mes
        total_direcciones_mes = direcciones_por_hora * horas_por_dia * dias_trabajados
        salario = salario_base + (total_direcciones_mes * (valor_urgente + valor_standard) / 2)

        # Cálculo de horas extras
        valor_hora_extra = (salario_base / 160) * 1.75
        salario += horas_extras * valor_hora_extra

        # Cálculo de antigüedad y festivos
        salario += antiguedad * 30
        salario += festivos_trabajados * 30

        # Descuento por vacaciones
        salario -= (salario_base / 30) * dias_vacaciones

        return jsonify({"paga_calculada": round(salario, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
