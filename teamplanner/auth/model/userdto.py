import sirope
import flask_login
import werkzeug.security as safe

class UserDTO(flask_login.UserMixin):
    def __init__(self, nombre, email, password):
        self.__nombre = nombre
        self.__email = email
        self.__password = password
        
    def __str__(self):
        return "Equipo [nombre=" + self.__nombre + ", email=" + \
            self.__email + ", contraseña=" + self.__password + "]"
    
    @property
    def email(self):
        return self.__email
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def password(self):
        return self.__password

    def get_id(self):
        return self.nombre
    
    def chk_password(self, password):
        return safe.check_password_hash(self.__password, password)
    
    @staticmethod
    def current_user():
        usr = flask_login.current_user
        
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
            
        return usr

    
    @staticmethod
    def find(s: sirope.Sirope, nombre: str) -> "UserDTO":
        return s.find_first(UserDTO, lambda u: u.nombre == nombre)