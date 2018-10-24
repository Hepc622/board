#!/usr/bin/ python
# vim: set fileencoding:utf-8


from flask import Flask, send_file
from module.config import Config
from module.controller import bc
conf = Config().conf
app = Flask(__name__)
app.register_blueprint(bc)


@app.route("/")
@app.route("/index.html")
def device_machining():
    return send_file("templates/index.html")

@app.route("/device")
@app.route("/deviceUnusual.html")
def device_unusual():
    return send_file("templates/deviceUnusual.html")

@app.route("/person")
@app.route("/personUnusual.html")
def person_unusual():
    return send_file("templates/personUnusual.html")



# 跳转到404页面
@app.errorhandler(404)
def err(error):
    return send_file("templates/404.html")


def main():
    web = conf.get("web");
    app.run(host=web.get('host'), port=web.get('port'), debug=web.get("debug"))

if __name__ == '__main__':
    main()