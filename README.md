# cherrypie
A RESTful style web framework base on falcon

基于 falcon 的 RESTful web 框架 model层仿mongokit

# Installing
Install and update using pip:

```
pip install -r requirements.txt
```

# Exemple

```
gunicorn --workers=4 -k tornado  manage:app -b 127.0.0.1:8001

```