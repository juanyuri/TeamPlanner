import sirope
import werkzeug.security as safe

class TeamDTO:
    def __init__(self, nombre, descripcion, codigo, fecha, autor, rating):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__descripcion = descripcion
        self.__fecha = fecha
        self.__autor = autor
        self.__rating = rating
    
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo):
        self.__nombre = nuevo
    
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def fecha(self):
        return self.__fecha
    
    @fecha.setter
    def fecha(self, nuevo):
        self.__fecha = nuevo
    
    @property
    def autor(self):
        return self.__autor
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    @descripcion.setter
    def descripcion(self, nuevo):
        self.__descripcion = nuevo
    
    @property
    def rating(self):
        return self.__rating
    
    @rating.setter
    def rating(self, nuevo):
        self.__rating = nuevo
    
    
    def __str__(self):
        return "Equipo [id=" + self.__codigo + ", descripcion=" + self.__descripcion + ", fechaCreacion=" + self.__fecha \
                + ", creador=" + self.__autor + ", rating=" + self.__rating + "]"
    
    @staticmethod
    def find(s: sirope.Sirope, codigo: str) -> "TeamDTO":
        return s.find_first(TeamDTO, lambda t: t.codigo == codigo)
    
    @staticmethod
    def findall(sirope):
        return list(sirope.filter(TeamDTO, lambda t: t))