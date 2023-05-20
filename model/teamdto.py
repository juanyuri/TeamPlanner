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
    
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def fecha(self):
        return self.__fecha
    
    @property
    def autor(self):
        return self.__autor
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    @property
    def rating(self):
        return self.__rating
    
    def __str__(self):
        return "Equipo [id=" + self.__codigo + ", descripcion=" + self.__descripcion + ", fechaCreacion=" + self.__fecha \
                + ", creador=" + self.__autor + ", rating=" + self.__rating + "]"
    
    @staticmethod
    def find(s: sirope.Sirope, codigo: str) -> "TeamDTO":
        return s.find_first(TeamDTO, lambda t: t.codigo == codigo)
    
    @staticmethod
    def findall(sirope):
        return list(sirope.filter(TeamDTO, lambda t: t))