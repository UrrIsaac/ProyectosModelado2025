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
    <title>Agenda de Tareas</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Agenda de Tareas</h1>
    </header>

    {content}

    <footer>
        <p>Generado automáticamente por export_html.py</p>
    </footer>
</body>
</html>
"""

def generar_html():
    """Carga, clasifica, ordena las tareas y genera el archivo index.html."""
    try:
        tareas = cargar_tareas()
    except FileNotFoundError:
        tareas = []
    
    if not tareas:
        content = "<section class='vacio'><h2>La agenda está vacía.</h2><p>No hay tareas registradas para mostrar.</p></section>"
    else:
        # Sorteo de las tareas
        tareas.sort(key=lambda t: t.prioridad * -1) 

        #separación de las secciones
        pendientes = [t for t in tareas if not t.completada]
        completadas = [t for t in tareas if t.completada]
        
        # Contador
        contador_pendientes = len(pendientes)
        contador_completadas = len(completadas)
        
        # Generar contenido HTML para las secciones
        
        seccion_pendientes = f"""
            <section id="pendientes" class="seccion-tareas">
                <h2>Pendientes ({contador_pendientes})</h2>
                <div class="lista-tareas">
                    {_generar_filas_html(pendientes) if pendientes else '<p class="mensaje-seccion">¡Todo al día en esta categoría!</p>'}
                </div>
            </section>
        """

        seccion_completadas = f"""
            <section id="completadas" class="seccion-tareas">
                <h2>Completadas ({contador_completadas})</h2>
                <div class="lista-tareas">
                    {_generar_filas_html(completadas) if completadas else '<p class="mensaje-seccion">Aún no hay tareas finalizadas.</p>'}
                </div>
            </section>
        """
        
        content = seccion_pendientes + seccion_completadas

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE.format(content=content))

    print("Archivo 'index.html' generado correctamente.")

def _generar_filas_html(tareas):
    """Genera el HTML para una lista de tareas."""
    filas = []
    for t in tareas:
        clase = "completada" if t.completada else "pendiente"
        estado = "Completada" if t.completada else "Pendiente"
        filas.append(f"""
            <div class="tarea {clase} prioridad-{t.prioridad}">
                <div class="header-tarea">
                    <h3 class="titulo">{t.titulo}</h3>
                    <span class="prioridad p-{t.prioridad}">P{t.prioridad}</span>
                </div>
                <div class="cuerpo-tarea">
                    <p><strong>Fecha límite:</strong> {t.fecha}</p>
                    <p class="etiquetas"><strong>Etiquetas:</strong> {", ".join(t.etiquetas) if t.etiquetas else "—"}</p>
                    <p class="descripcion"><strong>Descripción:</strong> {t.descripcion or "Sin descripción"}</p>
                </div>
                <span class="estado-final">{estado}</span>
            </div>
        """)
    return "\n".join(filas)


if __name__ == "__main__":
    generar_html()