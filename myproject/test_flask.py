# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
     return "Flask hälsar dig välkommen till TDP003"
if __name__ == "__main__":
     app.run()
