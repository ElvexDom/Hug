# Virtual Environnement

```bash

# install python env
python3 -m venv .venv
source .venv/bin/activate (Linux)
or
.venv\Scripts\activate.bat (Windows)

# install hug-api-rest
pip3 install hug -U
pip3 install setuptools
pip3 install pyjwt

```

## Dev launch

```bash

# load python env
source .venv/bin/activate (Linux)
or
.venv\Scripts\activate.bat (Windows)

# start server
hug -f serveur-api/HUG-entry.py
or
python3 serveur-api

```

### Command

```bash

#GET

http://localhost:8000/hello
http://localhost:8000/text?msg=my_message

http://localhost:8000/authenticated

http://localhost:8000/token_generation
http://localhost:8000/token_authenticated

# POST

http://localhost:8000/key_authenticated

```
