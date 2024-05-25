# python serveur-api 

import hug
import jwt
import base64
import string, random


@hug.cli()
@hug.local()
@hug.response_middleware()
def CORS(request, response, resource):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.set_header(
        'Access-Control-Allow-Headers',
        'Authorization,Keep-Alive,User-Agent'
        'If-Modified-Since,Cache-Control,Content-Type'
    )
    response.set_header(
        'Access-Control-Expose-Headers',
        'Authorization,Keep-Alive,User-Agent,'
        'If-Modified-Since,Cache-Control,Content-Type'
    )
    if request.method == 'OPTIONS':
        response.set_header('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Api-Key')
        response.set_header('Access-Control-Max-Age', 604800)
        response.set_header('Content-Type', 'text/plain charset=UTF-8')
        response.set_header('Content-Length', 0)
        response.status_code = hug.HTTP_204

################################# ERROR #################################

@hug.not_found(output=hug.output_format.html)
def not_found_handler():
    return "<html><head><title>Vous &ecirc;tes perdu ?</title></head><body><h1>Perdu sur l'Internet ?</h1><h2>Pas de panique, on va vous aider !</h2><strong><pre>    * <----- vous &ecirc;tes ici</pre></strong></body></html>"

################################# PUBLIC #################################

# HELLO
@hug.get('/hello')
def say_hello():
    return "hello"

# TEXT
@hug.get('/text')
def say_text(msg: hug.types.text, hug_timer=3):
    return msg

################################# BASIC #################################

# AUTHENTIFICATION BASIC
authentication = hug.authentication.basic(hug.authentication.verify('user', 'pass'))
@hug.get("/authenticated", requires=authentication)
def basic_auth_api_call(user: hug.directives.user):
    return "Successfully authenticated with user: {0}".format(user)

# RETURN A TOKEN
@hug.authentication.basic
@hug.get('/token_generation', requires=authentication)
def token_gen_call(user: hug.directives.user):
    """Authenticate and return a token"""
    secret_key = "MY SECRET KEY - PLEASE CHANGE"
    return {"user" : format(user), "key": secret_key, "token" : jwt.encode({'user': format(user), "admin": "true"}, secret_key, algorithm='HS256')}

################################# TOKEN #################################

# VERIFY TOKEN
def token_verify(token):
    print("token : " + token[6:])
    username="user"
    password="pass"
    return {"username": username, "password": password}

# AUTHENTIFICATION TOKEN
token_key_authentication = hug.authentication.token(token_verify)
@hug.authentication.token
@hug.get("/token_authenticated", requires=token_key_authentication)
def token_auth_call(user: hug.directives.user):
    return "Authenticated with token"

################################# API #################################                      

class APIUser(object):
    """A minimal example of a rich User object"""

    def __init__(self, user_id, api_key):
        self.user_id = user_id
        self.api_key = api_key


def api_key_verify(api_key):
    magic_key = "5F00832B-DE24-4CAF-9638-C10D1C642C6C"
    if api_key == magic_key:
        user_id="user"
        # Success!
        return APIUser(user_id, api_key)
    else:
        # Invalid key
        return None

api_key_authentication = hug.authentication.api_key(api_key_verify)

@hug.authentication.api_key
@hug.post("/key_authenticated", requires=api_key_authentication)
def basic_auth_api_call(user: hug.directives.user):
    return "Authenticated with key"

################################# CLI #################################

hug.API("api").http.server()

if __name__ == '__main__':
    api.interface.cli()

################################# END #################################