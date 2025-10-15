#!/usr/bin/env python3

"""
Gestor de tareas (agenda) - Módulo principal.

Este código proporciona una interfaz de línea de comandos para gestionar tareas,
permitiendo agregar, mostrar, buscar, marcar como completadas, eliminar,
guardar en archivo y cargar tareas.

Equipo (en orden alfabetico) :
    Andrade Castañeda Angel
    Urrutia Alfaro Isaac Arturo
"""
import argparse
import json
import os
from datetime import datetime
from Tarea import Tarea

# Archivo por defecto para almacenar las tareas
DATA_FILE = ".tareas.json"


def cargar_tareas(archivo=DATA_FILE):
    """Cargar tareas desde un archivo JSON.
    
    Args:
        archivo (str): Ruta del archivo desde donde cargar las tareas.
        
    Returns:
        list: Lista de objetos Tarea cargados desde el archivo.
    """

    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return [Tarea.from_dict(d) for d in datos]

def guardar_tareas(tareas, archivo=DATA_FILE):
    """Guardar tareas en un archivo JSON.
    
    Args:
        tareas (list): Lista de objetos Tarea a guardar.
        archivo (str): Ruta del archivo donde guardar las tareas.
    """
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tareas], f, indent=2, ensure_ascii=False)

def generar_id(tareas):
    """Generar un ID único para una nueva tarea.
    
    Args:
        tareas (list): Lista de tareas existentes.
        
    Returns:
        str: Nuevo ID en formato T-XXXX.
    """

    if not tareas:
        return "T-0001"
    nums = [int(t.id.split("-")[1]) for t in tareas if t.id.startswith("T-")]
    siguiente = max(nums) + 1 if nums else 1
    return f"T-{siguiente:04d}"

def cmd_add(args):
    """Manejador del comando add: añadir una nueva tarea."""

    # Crear nueva tarea
    tareas = cargar_tareas()
    nuevo_id = generar_id(tareas)
    etiquetas = args.etiquetas.split(",") if args.etiquetas else []
    tarea = Tarea(
        id_=nuevo_id,
        titulo=args.titulo,
        prioridad=args.prioridad,
        fecha=args.fecha,
        etiquetas=etiquetas,
        descripcion=args.descripcion,
    )

    # Guardar tarea
    tareas.append(tarea)
    guardar_tareas(tareas)
    print(f"Tarea añadida con id {nuevo_id}")

def cmd_ls(args):
    """Manejador del comando ls: listar tareas."""

    tareas = cargar_tareas()

     # Verificar si no hay tareas
    if not tareas:
        print("No hay tareas.")
        return
    
    # Ordenar tareas si se especificó un criterio
    if args.por:
        tareas.sort(key=lambda t: getattr(t, args.por))
    for t in tareas:
        estado = "X" if hasattr(t, 'hecha') and t.hecha else "."
        print(f"{t.id} [{estado}] {t.fecha} (p{t.prioridad}) {t.titulo}")

def cmd_find(args):
    """Manejador del comando find: buscar tareas por término."""

    tareas = cargar_tareas()
    term = args.termino.lower()

    # Filtrar tareas que contengan el término en título o descripción
    encontradas = [
        t for t in tareas
        if term in t.titulo.lower() or term in t.descripcion.lower()
    ]
    for t in encontradas:
        estado = "X" if hasattr(t, 'hecha') and t.hecha else "."
        print(f"{t.id} [{estado}] {t.fecha} (p{t.prioridad}) {t.titulo}")

def cmd_done(args):
    """Manejador del comando done: marcar tarea como completada."""
    tareas = cargar_tareas()

    for t in tareas:
        if t.id == args.id:
            t.hecha = True
            guardar_tareas(tareas)
            print(f"Tarea {args.id} marcada como hecha")
            return
        
     # Si no se encuentra la tarea
    print(f"Error: No se encontró la tarea {args.id}")

def cmd_rm(args):
    """Manejador del comando rm: eliminar una tarea."""

    tareas = cargar_tareas()
    nuevas_tareas = [t for t in tareas if t.id != args.id]

    # Verificar si se eliminó alguna tarea
    if len(nuevas_tareas) == len(tareas):
        print(f"Error: No se encontró la tarea {args.id}")
        return
    guardar_tareas(nuevas_tareas)
    print(f"Tarea {args.id} eliminada")

def cmd_save(args):
    """Manejador del comando save: guardar tareas en archivo específico."""
    tareas = cargar_tareas()
    guardar_tareas(tareas, args.archivo)
    print(f"Tareas guardadas en {args.archivo}")

def cmd_load(args):
    """Manejador del comando load: cargar tareas desde archivo específico."""
    if not os.path.exists(args.archivo):
        print(f"Error: El archivo {args.archivo} no existe")
        return
    tareas = cargar_tareas(args.archivo)
    guardar_tareas(tareas)
    print(f"Tareas cargadas desde {args.archivo}")

def main():
    parser = argparse.ArgumentParser(prog="agenda", description="Gestor de tareas")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Comando add
    a = sub.add_parser("add")
    a.add_argument("--titulo", required=True)
    a.add_argument("--fecha", required=True)
    a.add_argument("--prioridad", type=int, required=True, choices=range(1,6))
    a.add_argument("--etiquetas")
    a.add_argument("--descripcion", default="")
    a.set_defaults(func=cmd_add)

    # Comando ls
    l = sub.add_parser("ls", help="Listar tareas")
    l.add_argument("--por", choices=["fecha","prioridad","id"],
                   help="Ordenar por un campo")
    l.set_defaults(func=cmd_ls)

    # Comando find
    f = sub.add_parser("find", help="Buscar término en título o descripción")
    f.add_argument("termino", help="Cadena a buscar")
    f.set_defaults(func=cmd_find)

    # Comando done
    d = sub.add_parser("done", help="Marcar tarea como realizada")
    d.add_argument("id", help="ID de la tarea a marcar como hecha")
    d.set_defaults(func=cmd_done)

    # Comando rm
    r = sub.add_parser("rm", help="Eliminar tarea")
    r.add_argument("id", help="ID de la tarea a eliminar")
    r.set_defaults(func=cmd_rm)

    # Comando save
    s = sub.add_parser("save", help="Guardar tareas en archivo")
    s.add_argument("archivo", help="Archivo donde guardar las tareas")
    s.set_defaults(func=cmd_save)

    # Comando load
    lo = sub.add_parser("load", help="Cargar tareas desde archivo")
    lo.add_argument("archivo", help="Archivo desde donde cargar las tareas")
    lo.set_defaults(func=cmd_load)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
