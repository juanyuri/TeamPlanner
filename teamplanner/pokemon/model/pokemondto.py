import sirope
import werkzeug.security as safe

class PokemonDTO:
    def __init__(self, id, especie, num_pokedex, nivel, move1, move2, tipo):
        self.__id = id
        self.__especie = especie
        self.__nivel = nivel
        self.__num_pokedex = num_pokedex
        self.__pctg_uso = 0.0
        self.__move1 = move1
        self.__move2 = move2
        self.__tipo = tipo
    
    @property
    def especie(self):
        return self.__especie
    
    @especie.setter
    def especie(self, nuevo):
        self.__especie = nuevo
    
    @property
    def num_pokedex(self):
        return self.__num_pokedex
    
    @num_pokedex.setter
    def num_pokedex(self, nuevo):
        self.__num_pokedex = nuevo
    
    @property
    def nivel(self):
        return self.__nivel
    
    @nivel.setter
    def nivel(self, nuevo):
        self.__nivel = nuevo
    
    @property
    def move1(self):
        return self.__move1
    
    @move1.setter
    def move1(self, nuevo):
        self.__move1 = nuevo
    
    @property
    def move2(self):
        return self.__move2
    
    @move2.setter
    def move2(self, nuevo):
        self.__move2 = nuevo
    
    @property 
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, nuevo):
        self.__tipo = nuevo
    
    @property 
    def pctg_uso(self):
        return self.__pctg_uso
    
    @pctg_uso.setter
    def pctg_uso(self, nuevo):
        self.__pctg_uso = nuevo
    
    
    def __str__(self):
        return "Pokemon [especie=" + self.__especie + ", Num Pokedex=" + self.__num_pokedex + ", uso (%)=" + str(self.__pctg_uso) \
                + ", Mov. 1= " + self.__move1 + ", Mov. 2= " + self.__move2 + "]"
    
    
    @staticmethod
    def find(s: sirope.Sirope, especie: str) -> "PokemonDTO":
        return s.find_first(PokemonDTO, lambda t: t.especie == especie)
    
    
    @staticmethod
    def findall(sirope):
        return list(sirope.filter(PokemonDTO, lambda t: t))