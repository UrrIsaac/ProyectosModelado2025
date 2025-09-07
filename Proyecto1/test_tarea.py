import unittest
from tarea import Tarea


class TestTarea(unittest.TestCase):
    """Pruebas básicas para la clase Tarea."""

    def test_crear_tarea_valida(self):
        """Crear una tarea válida debería funcionar."""
        t = Tarea(
            id_="T-0001",
            titulo="Estudiar MVC",
            prioridad=3,
            fecha="2025-09-01",
            etiquetas=["escuela", "poo"],
            descripcion="resumen de clase"
        )
        self.assertEqual(t.id, "T-0001")
        self.assertEqual(t.titulo, "Estudiar MVC")
        self.assertFalse(t.completada)

    def test_prioridad_invalida(self):
        """Prioridad fuera de rango debería lanzar ValueError."""
        with self.assertRaises(ValueError):
            Tarea("T-0002", "Algo", 7, "2025-09-01")

    def test_fecha_invalida(self):
        """Fecha en formato incorrecto debería lanzar ValueError."""
        with self.assertRaises(ValueError):
            Tarea("T-0003", "Algo", 3, "01-09-2025")

    def test_to_dict_y_from_dict(self):
        """Convertir a dict y recrear desde dict debería ser consistente."""
        datos = {
            "id": "T-0004",
            "titulo": "Probar JSON",
            "prioridad": 2,
            "fecha": "2025-09-02",
            "etiquetas": ["test"],
            "descripcion": "prueba",
            "completada": True,
        }
        t1 = Tarea.from_dict(datos)
        t2 = Tarea(**datos, id_=datos["id"])  # usando el constructor
        self.assertEqual(t1.to_dict(), datos)
        self.assertEqual(t1.titulo, t2.titulo)


if __name__ == "__main__":
    unittest.main()

