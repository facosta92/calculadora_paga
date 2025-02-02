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

# Variables para el cálculo de gastos de locomoción
COEFICIENTE_K = 0.91
CONSTANTE_C = 0.78
PRECIO_KM = 0.19

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/calcular', methods=['POST'])
def calcular_paga():
    try:
        data = request.get_json()
        categoria = data.get("categoria")
        poblacion = data.get("poblacion")
        direcciones_urgentes = float(data.get("direccionesUrgentes", 0))
        direcciones_standard = float(data.get("direccionesStandard", 0))
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
        
        # Cálculo del salario por unidad de obra
        salario = salario_base + (direcciones_urgentes * valor_urgente) + (direcciones_standard * valor_standard)
        
        # Cálculo del plus de peligrosidad
        plus_peligrosidad = salario * 0.06 if categoria == "mensajero" else direcciones_urgentes * 0.07
        salario += plus_peligrosidad

        # Cálculo de gastos de locomoción
        ruo_mensual = salario_base / 14
        gasto_locomocion = ((ruo_mensual * COEFICIENTE_K) / CONSTANTE_C) * km_recorridos * PRECIO_KM
        salario += gasto_locomocion

        # Cálculo de incentivos
        if categoria == "mensajero" and direcciones_urgentes + direcciones_standard > 506:
            salario += (direcciones_urgentes + direcciones_standard - 506) * 0.45
        if categoria == "ciclomensajero" and direcciones_urgentes + direcciones_standard > 394:
            salario += (direcciones_urgentes + direcciones_standard - 394) * 0.50

        # Cálculo de horas extras
        valor_hora_extra = (salario_base / 160) * 1.75
        salario += horas_extras * valor_hora_extra

        # Cálculo de antigüedad
        salario += antiguedad * 30
        salario += festivos_trabajados * 30

        # Descuento por vacaciones
        salario -= (salario_base / 30) * dias_vacaciones

        return jsonify({"paga_calculada": round(salario, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
