# srv-dash-flask-ext
one liner flask extension the integrate your app to [srv-dash](https://github.com/bariyu/srv-dash)

example usage:
```python
from flask import Flask
from flask_srv_dash import SrvDashExtension

app = Flask(__name__)
SrvDashExtension(app, '<your_app_name>', '<your_srv_dash_base_url>', auth_enabled=False, auth_key='<your_auth_key')

```
