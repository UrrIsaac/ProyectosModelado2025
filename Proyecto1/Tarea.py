"""
Módulo tarea.py

Define la clase Tarea que modela una entrada en la agenda.
Cumple con PEP 8 y PEP 257.
"""

import re
from datetime import datetime


class Tarea:
    """
    Representa una tarea dentro de la agenda.

    Atributos:
        id (str): Identificador único de la tarea (ej. "T-0001").
        titulo (str): Título breve de la tarea.
        prioridad (int): Número entero entre 1 y 5 que indica la prioridad.
        fecha (str): Fecha en formato 'AAAA-MM-DD'.
        etiquetas (list[str]): Lista de etiquetas asociadas.
        descripcion (str): Descripción opcional de la tarea.
        completada (bool): Estado de finalización de la tarea.
    """

    def __init__(self, id_, titulo, prioridad, fecha,
                 etiquetas=None, descripcion="", completada=False):
        """
        Inicializa una nueva tarea validando campos básicos.

        Args:
            id_ (str): Identificador único de la tarea.
            titulo (str): Título breve.
            prioridad (int): Valor entre 1 y 5.
            fecha (str): Fecha en formato 'AAAA-MM-DD'.
            etiquetas (list[str], opcional): Lista de etiquetas. Por defecto [].
            descripcion (str, opcional): Texto descriptivo. Por defecto "".
            completada (bool, opcional): Estado inicial. Por defecto False.

        Raises:
            ValueError: Si algún campo no cumple las validaciones.
        """
        self.id = self._validar_id(id_)
        self.titulo = titulo.strip()
        self.prioridad = self._validar_prioridad(prioridad)
        self.fecha = self._validar_fecha(fecha)
        self.etiquetas = etiquetas if etiquetas is not None else []
        self.descripcion = descripcion.strip()
        self.completada = bool(completada)

    @staticmethod
    def _validar_id(id_):
        """Valida el formato del id (ej. 'T-0001')."""
        if not isinstance(id_, str) or not id_.strip():
            raise ValueError("El id debe ser una cadena no vacía.")
        return id_

    @staticmethod
    def _validar_prioridad(valor):
        """Valida que la prioridad esté en el rango 1..5."""
        if not isinstance(valor, int) or not (1 <= valor <= 5):
            raise ValueError("La prioridad debe ser un entero entre 1 y 5.")
        return valor

    @staticmethod
    def _validar_fecha(fecha):
        """Valida que la fecha tenga formato AAAA-MM-DD."""
        patron = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(patron, fecha):
            raise ValueError("Formato de fecha inválido (AAAA-MM-DD).")
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Fecha no válida en el calendario.") from exc
        return fecha

    def marcar_completada(self):
        """Marca la tarea como completada."""
        self.completada = True

    def to_dict(self):
        """
        Convierte la tarea a un diccionario serializable en JSON.

        Returns:
            dict: Representación de la tarea.
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "prioridad": self.prioridad,
            "fecha": self.fecha,
            "etiquetas": self.etiquetas,
            "descripcion": self.descripcion,
            "completada": self.completada,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea una tarea a partir de un diccionario (ej. cargado desde JSON).

        Args:
            data (dict): Diccionario con los campos de la tarea.

        Returns:
            Tarea: Nueva instancia de la clase.
        """
        return cls(
            id_=data["id"],
            titulo=data["titulo"],
            prioridad=data["prioridad"],
            fecha=data["fecha"],
            etiquetas=data.get("etiquetas", []),
            descripcion=data.get("descripcion", ""),
            completada=data.get("completada", False),
        )

