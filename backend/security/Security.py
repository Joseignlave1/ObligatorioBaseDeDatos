import datetime
import pytz
import jwt
from backend.config.config import JWT_KEY

class Security():

    tz = pytz.timezone("America/Montevideo")
    @classmethod
    def generate_jwt_token(cls, user):
        payload = {
            #Fecha de creacion del token
            'iat': datetime.datetime.now(tz = cls.tz),
            # Fecha de expiracion del token
            'exp': datetime.datetime.now(tz = cls.tz) + datetime.timedelta(minutes= 30),
            'email': user['email']
        }

        #Creacion del token JWT
        token = jwt.encode(payload,JWT_KEY, algorithm = "HS256")

        return token