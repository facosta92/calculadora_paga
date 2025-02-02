from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Datos de salario base
SALARIOS_BASE = {
    "mensajero": 1025,
    "ciclomensajero": 1025,
    "conductor": 1100,
    "andarin": 1000
}

# Factores por unidad de trabajo según población
FACTORES_UNIDAD = {
    "mas_1500000": {"urgente": 1.78, "standard": 1.35, "codigo_postal": 0.80, "kilometros": 0.28, "exceso_pm": 0.99, "tiempo_espera": 0.11, "coef_k": 0.91},
    "501001_1500000": {"urgente": 1.35, "standard": 1.10, "codigo_postal": 0.80, "kilometros": 0.28, "exceso_pm": 0.99, "tiempo_espera": 0.11, "coef_k": 0.91},
    "301001_500000": {"urgente": 1.22, "standard": 1.10, "codigo_postal": 0.80, "kilometros": 0.28, "exceso_pm": 0.99, "tiempo_espera": 0.11, "coef_k": 0.91},
    "50001_300000": {"urgente": 1.10, "standard": 1.10, "codigo_postal": 0.80, "kilometros": 0.28, "exceso_pm": 0.99, "tiempo_espera": 0.11, "coef_k": 0.91},
    "menos_150000": {"urgente": 1.04, "standard": 1.04, "codigo_postal": 0.80, "kilometros": 0.28, "exceso_pm": 0.99, "tiempo_espera": 0.11, "coef_k": 0.91}
}

def calcular_salario(categoria, poblacion, unidades):
    """ Cálculo del salario basado en la población y las unidades de trabajo """
    
    if categoria not in SALARIOS_BASE:
        return {"error": "Categoría inválida"}, 400
    
    if poblacion not in FACTORES_UNIDAD:
        return {"error": "Rango de población inválido"}, 400

    salario_base = SALARIOS_BASE[categoria]
    factores = FACTORES_UNIDAD[poblacion]

    # Cálculo de salario basado en unidades de trabajo
    salario = salario_base
    for key, value in unidades.items():
        salario += unidades[key] * factores.get(key, 0)

    return {"paga_calculada": round(salario, 2)}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/calcular', methods=['POST'])
def calcular_paga():
    """ Ruta para calcular la paga """
    try:
        data = request.get_json()

        categoria = data.get("categoria")
        poblacion = data.get("poblacion")
        unidades = {
            "urgente": float(data.get("urgente", 0)),
            "standard": float(data.get("standard", 0)),
            "codigo_postal": float(data.get("codigo_postal", 0)),
            "kilometros": float(data.get("kilometros", 0)),
            "exceso_pm": float(data.get("exceso_pm", 0)),
            "tiempo_espera": float(data.get("tiempo_espera", 0)),
            "coef_k": float(data.get("coef_k", 0))
        }

        resultado = calcular_salario(categoria, poblacion, unidades)
        return jsonify(resultado)

    except ValueError:
        return jsonify({"error": "Datos inválidos, ingrese solo números"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)