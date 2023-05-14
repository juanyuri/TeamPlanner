import sirope
import flask_login
import werkzeug.security as safe

class UserDTO(flask_login.UserMixin):
    def __init__(self, email, password):
        self.__email = email
        self.__password = password
        
    def __init__(self, nombre, email, password):
        self.__nombre = nombre
        self.__email = email
        self.__password = password
    
    @property
    def email(self):
        return self.__email
    
    @property
    def nombre(self):
        return self.__nombre

    def get_id(self):
        return self.email
    
    def chk_password(self, password):
        return safe.check_password_hash(self._password, password)
    
    @staticmethod
    def current_user():
        usr = flask_login.current_user
    
    @staticmethod
    def find(s: sirope.Sirope, email: str) -> "UserDTO":
        return s.find_first(UserDto, lambda u: u.email == email)