import datetime
import pytz
import jwt
from backend.config.config import JWT_KEY

class Security():

    tz = pytz.timezone("America/Montevideo")

    @classmethod
    def generate_jwt_token(cls, user):
        if 'correo' not in user or not user['correo']:
            raise ValueError("El usuario debe tener un correo para generar el token JWT")

        payload = {
            #Fecha de creacion del token
            'iat': datetime.datetime.now(tz = cls.tz),
            # Fecha de expiracion del token
            'exp': datetime.datetime.now(tz = cls.tz) + datetime.timedelta(minutes= 30),
            'email': user['correo'],
            'sub': user['correo']
        }
        #Creacion del token JWT
        token = jwt.encode(payload,JWT_KEY, algorithm = "HS256")

        return token