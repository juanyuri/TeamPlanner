import sirope
import werkzeug.security as safe

class TipoDTO:
    def __init__(self, nombre, ):
        self.__nombre = nombre

    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo):
        self.__nombre = nuevo

    def __str__(self):
        return "Tipo [nombre=" + self.__nombre + "]"
    
    @staticmethod
    def find(s: sirope.Sirope, nombre: str) -> "TipoDTO":
        return s.find_first(TipoDTO, lambda t: t.nombre == nombre)
    
    @staticmethod
    def findall(sirope):
        return list(sirope.filter(TipoDTO, lambda t: t))