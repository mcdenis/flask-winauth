Windows Authentication for Flask
================================

Flask extension allowing easy retrieval of basic information about a user
authenticated with Microsoft IIS' Windows Authentication.

Installation
------------
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
`flask-winauth`.

```
pip install git+https://github.com/mcdenis/flask-winauth.git
```

In the IIS `web.config` file, configure the HTTP Platform Handler to forward the
authentication token to the Python process.

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <httpPlatform forwardWindowsAuthToken="true">
    </httpPlatform>
  </system.webServer>
</configuration>
```
(Configuration items not relevant to `flask-winauth` excluded for clarity.)

Usage
-----

Simply access the `flask_winauth.current_user` global from within a view
function or anywhere else with a request context.

```py
from flask import Flask
from flask_winauth import current_user

app = Flask(__name__)

@app.route("/")
def greet_user():
    return f"<p>Hello, {current_user.name}!</p>"
```

Remark on Quality
--------------

This software was originally developed for specific applications and is not yet
tested for general usage.