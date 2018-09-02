# cherrypie
A RESTful style Web framework base on Falcon

基于[Falcon](http://falconframework.org/#sectionDesign) 的 RESTful Web 框架 Model层仿[MongoKit](https://github.com/namlook/mongokit)

# Installing
Install and update using pip:

```
pip install -r requirements.txt
```

# Exemple

```
gunicorn --workers=4 -k tornado  manage:app -b 127.0.0.1:8001

```