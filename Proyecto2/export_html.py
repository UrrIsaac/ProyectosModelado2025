#!/usr/bin/env python3
"""
Genera un archivo index.html desde las tareas almacenadas en .tareas.json.
Usa agenda.py para cargar las tareas.
"""

import os
from agenda import cargar_tareas

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Agenda de tareas</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Agenda de tareas</h1>

    {content}

    <footer>
        <p>Generado automáticamente por export_html.py</p>
    </footer>
</body>
</html>
"""

def generar_html():
    tareas = cargar_tareas()

    if not tareas:
        content = "<p class='vacio'>No hay tareas registradas.</p>"
    else:
        filas = []
        for t in tareas:
            clase = "completada" if t.completada else "pendiente"
            estado = "Completada" if t.completada else "Pendiente"
            filas.append(f"""
                <div class="tarea {clase}">
                    <h2>{t.titulo}</h2>
                    <p><strong>ID:</strong> {t.id}</p>
                    <p><strong>Fecha:</strong> {t.fecha}</p>
                    <p><strong>Prioridad:</strong> {t.prioridad}</p>
                    <p><strong>Etiquetas:</strong> {", ".join(t.etiquetas) if t.etiquetas else "—"}</p>
                    <p><strong>Descripción:</strong> {t.descripcion or "Sin descripción"}</p>
                    <span class="estado">{estado}</span>
                </div>
            """)
        content = "\n".join(filas)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE.format(content=content))

    print("Archivo 'index.html' generado correctamente.")

if __name__ == "__main__":
    generar_html()

