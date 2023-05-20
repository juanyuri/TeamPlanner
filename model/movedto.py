import sirope
import werkzeug.security as safe

class MovimientoDTO:
    def __init__(self, nombre, desc, categoria, potencia, tipo):
        self.__nombre = nombre
        self.__descripcion = desc
        self.__categoria = categoria
        self.__potencia = potencia
        self.__tipo = tipo

    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    @property
    def categoria(self):
        return self.__categoria
    
    @property
    def potencia(self):
        return self.__potencia
    
    @property
    def tipo(self):
        return self.__tipo
    
    def __str__(self):
        return "Equipo [nombre=" + self.__nombre + ", descripción=" + self.__descripcion + ", categoría=" + self.__categoria \
                + ", potencia=" + self.__potencia + ", tipo=" + self.tipo + "]"
    
    @staticmethod
    def find(s: sirope.Sirope, codigo: str) -> "MovimientoDTO":
        return s.find_first(MovimientoDTO, lambda t: t.nombre == nombre)
    
    @staticmethod
    def findall(sirope):
        return list(sirope.filter(MovimientoDTO, lambda t: t))