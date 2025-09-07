#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
from Tarea import Tarea

DATA_FILE = ".tareas.json"
#Creo este archivo oculto para el usuario para yo poder manipular de buena manera las tareas

#Algo parecido estará en save y load, solo que se activará cuando el usuario lo quiera
def cargar_tareas():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return [Tarea.from_dict(d) for d in datos]

def guardar_tareas(tareas):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tareas], f, indent=2, ensure_ascii=False) #ocupo la lista por comprensión

#Genero id's unicos para hacer más fácil la manipulacion
def generar_id(tareas):
    if not tareas:
        return "T-0001"
    nums = [int(t.id.split("-")[1]) for t in tareas]
    siguiente = max(nums) + 1
    return f"T-{siguiente:04d}"

def cmd_add(args):
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
    tareas.append(tarea)
    guardar_tareas(tareas)
    print(f"Tarea añadida con id {nuevo_id}")

def cmd_ls(args):
    tareas = cargar_tareas()
    if args.por:
        # orden por atributo: fecha, prioridad o id
        tareas.sort(key=lambda t: getattr(t, args.por))
    for t in tareas:
        estado = "."
        print(f"{t.id} [{estado}] {t.fecha} (p{t.prioridad}) {t.titulo}")

def cmd_find(args):
    tareas = cargar_tareas()
    term = args.termino.lower()
    encontradas = [
        t for t in tareas
        if term in t.titulo.lower() or term in t.descripcion.lower()
    ]
    for t in encontradas:
        estado = "."
        print(f"{t.id} [{estado}] {t.fecha} (p{t.prioridad}) {t.titulo}")

def main():
    parser = argparse.ArgumentParser(prog="agenda", description="Gestor de tareas")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Comando add
    a = sub.add_parser("add" )
    a.add_argument("--titulo", required=True )
    a.add_argument("--fecha", required=True )
    a.add_argument("--prioridad", type=int, required=True, choices=range(1,6))
    a.add_argument("--etiquetas" )
    a.add_argument("--descripcion", default="" )
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

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
