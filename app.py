from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Función para extraer valores numéricos de operaciones, oficiales y aerotécnicos segmentados por literales
def extraer_informacion(texto):
    # Dividir el texto en secciones basadas en los cuatro literales principales
    # Ajustamos las expresiones regulares para que coincidan con el formato 'A.-', 'B.-', etc.
    seccion_a = re.search(r'A\.\-?\s*(.*?)(?=B\.\-)', texto, re.DOTALL | re.IGNORECASE)
    seccion_b = re.search(r'B\.\-?\s*(.*?)(?=C\.\-)', texto, re.DOTALL | re.IGNORECASE)
    seccion_c = re.search(r'C\.\-?\s*(.*?)(?=D\.\-)', texto, re.DOTALL | re.IGNORECASE)
    seccion_d = re.search(r'D\.\-?\s*(.*?)(?=TOTAL DE LAS OPERACIONES)', texto, re.DOTALL | re.IGNORECASE)

    # Función para extraer los valores de operaciones, oficiales y aerotécnicos de una sección
    def extraer_valores(seccion):
        if not seccion:
            return 0, 0, 0  # Si la sección es None, devolver ceros

        operaciones = re.findall(r'\((\d+)\)\s*operaciones?', seccion, re.IGNORECASE)
        operaciones = list(map(int, operaciones))
        
        oficiales = re.findall(r'(\d+)\s*Oficial(?:es)?', seccion, re.IGNORECASE)
        oficiales = list(map(int, oficiales))
        
        aerotecnicos = re.findall(r'(\d+)\s*Aerotécnicos?', seccion, re.IGNORECASE)
        aerotecnicos = list(map(int, aerotecnicos))
        
        total_operaciones = sum(operaciones)
        total_oficiales = sum(oficiales)
        total_aerotecnicos = sum(aerotecnicos)
        
        return total_operaciones, total_oficiales, total_aerotecnicos

    # Extraer valores para cada literal (A, B, C, D)
    total_operaciones_a, total_oficiales_a, total_aerotecnicos_a = extraer_valores(seccion_a.group(1) if seccion_a else None)
    total_operaciones_b, total_oficiales_b, total_aerotecnicos_b = extraer_valores(seccion_b.group(1) if seccion_b else None)
    total_operaciones_c, total_oficiales_c, total_aerotecnicos_c = extraer_valores(seccion_c.group(1) if seccion_c else None)
    total_operaciones_d, total_oficiales_d, total_aerotecnicos_d = extraer_valores(seccion_d.group(1) if seccion_d else None)

    # Calcular los totales globales
    total_operaciones_global = total_operaciones_a + total_operaciones_b + total_operaciones_c + total_operaciones_d
    total_oficiales_global = total_oficiales_a + total_oficiales_b + total_oficiales_c + total_oficiales_d
    total_aerotecnicos_global = total_aerotecnicos_a + total_aerotecnicos_b + total_aerotecnicos_c + total_aerotecnicos_d

    return {
        "A": (total_operaciones_a, total_oficiales_a, total_aerotecnicos_a),
        "B": (total_operaciones_b, total_oficiales_b, total_aerotecnicos_b),
        "C": (total_operaciones_c, total_oficiales_c, total_aerotecnicos_c),
        "D": (total_operaciones_d, total_oficiales_d, total_aerotecnicos_d),
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
