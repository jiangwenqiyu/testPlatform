from flask_httpauth import HTTPBasicAuth
from itsdangerous import Serializer



a = Serializer('ji ni tai mei')
b = a.serializer.dumps('123')
print(bytes.decode(b))


