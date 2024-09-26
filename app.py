from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Función para extraer valores numéricos de operaciones, oficiales y aerotécnicos segmentados por literales
def extraer_informacion(texto):
    # Dividir el texto en secciones basadas en los tres literales principales
    seccion_a = re.search(r'OPERACIONES ESPECIALES DE ANTITERRORISMO Y CONTRATERRORISMO(.*?)(OPERACIONES DE COMPETENCIA LEGAL DE FUERZAS ARMADAS|OPERACIONES EN APOYO A LA POLICÍA NACIONAL)', texto, re.DOTALL | re.IGNORECASE)
    seccion_b = re.search(r'OPERACIONES DE COMPETENCIA LEGAL DE FUERZAS ARMADAS(.*?)(OPERACIONES EN APOYO A LA POLICÍA NACIONAL)', texto, re.DOTALL | re.IGNORECASE)
    seccion_c = re.search(r'OPERACIONES EN APOYO A LA POLICÍA NACIONAL EN EL CONTROL DE LOS CRS/CPL(.*?)(TOTAL DE LAS OPERACIONES)', texto, re.DOTALL | re.IGNORECASE)

    # Función para extraer valores de operaciones, oficiales y aerotécnicos
    def extraer_valores(seccion):
        operaciones = re.findall(r'\((\d+)\)\s+operaciones?', seccion, re.IGNORECASE)
        operaciones = list(map(int, operaciones))
        
        oficiales = re.findall(r'(\d+)\s+oficial(?:es)?', seccion, re.IGNORECASE)
        oficiales = list(map(int, oficiales))
        
        aerotecnicos = re.findall(r'(\d+)\s+aerotécnicos?', seccion, re.IGNORECASE)
        aerotecnicos = list(map(int, aerotecnicos))
        
        total_operaciones = sum(operaciones)
        total_oficiales = sum(oficiales)
        total_aerotecnicos = sum(aerotecnicos)
        
        return total_operaciones, total_oficiales, total_aerotecnicos

    # Extraer valores para cada literal (A, B, C)
    total_operaciones_a, total_oficiales_a, total_aerotecnicos_a = extraer_valores(seccion_a.group(1) if seccion_a else "")
    total_operaciones_b, total_oficiales_b, total_aerotecnicos_b = extraer_valores(seccion_b.group(1) if seccion_b else "")
    total_operaciones_c, total_oficiales_c, total_aerotecnicos_c = extraer_valores(seccion_c.group(1) if seccion_c else "")

    # Calcular los totales globales
    total_operaciones_global = total_operaciones_a + total_operaciones_b + total_operaciones_c
    total_oficiales_global = total_oficiales_a + total_oficiales_b + total_oficiales_c
    total_aerotecnicos_global = total_aerotecnicos_a + total_aerotecnicos_b + total_aerotecnicos_c

    return {
        "A": (total_operaciones_a, total_oficiales_a, total_aerotecnicos_a),
        "B": (total_operaciones_b, total_oficiales_b, total_aerotecnicos_b),
        "C": (total_operaciones_c, total_oficiales_c, total_aerotecnicos_c),
        "total": (total_operaciones_global, total_oficiales_global, total_aerotecnicos_global)
    }

@app.route("/", methods=["GET", "POST"])
def resumen_operaciones():
    if request.method == "POST":
        # Extraer el texto ingresado
        texto = request.form["texto"]

        # Llamar a la función para extraer la información segmentada por literales
        resumen = extraer_informacion(texto)

        # Renderizar los resultados en la página
        return render_template("index.html", 
                               texto=texto,
                               resumen=resumen)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
