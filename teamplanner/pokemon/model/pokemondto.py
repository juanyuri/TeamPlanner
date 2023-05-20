import sirope
import werkzeug.security as safe

class PokemonDTO:
    def __init__(self, id, especie, num_pokedex, nivel, move1, move2, tipo):
        self.__id = id
        self.__especie = especie
        self.__num_pokedex = num_pokedex
        self.__pctg_uso = 0.0
        self.__move1 = move1
        self.__move2 = move2
        self.__tipo = tipo
    
    @property
    def especie(self):
        return self.__especie
    
    @property
    def num_pokedex(self):
        return self.__num_pokedex
    
    @property
    def nivel(self):
        return self.__nivel
    
    @property
    def move1(self):
        return self.__move1
    
    @property
    def move2(self):
        return self.__move2
    
    
    def __str__(self):
        return "Pokemon [especie=" + self.__especie + ", Num Pokedex=" + self.__num_pokedex + ", uso (%)=" + str(self.__pctg_uso) \
                + ", movimiento 1=" + self.__move1 + "]"
    
    @staticmethod
    def find(s: sirope.Sirope, codigo: str) -> "PokemonDTO":
        return s.find_first(PokemonDTO, lambda t: t.codigo == codigo)
    
    @staticmethod
    def findall(sirope):
        return list(sirope.filter(PokemonDTO, lambda t: t))