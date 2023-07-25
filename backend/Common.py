from flask import jsonify


class Resp:
    def success(msg="ok", body=None):
        return jsonify(
            {
                'code': 0,
                'msg': msg,
                'body': body
            }
        )

    def error(msg="error", body=None, code=-1):
        return jsonify(
            {
                'code': code,
                'msg': msg,
                'body': body
            }
        )


class Config:
    authcode = '142876'
    SECRET_KEY = 'a5438326-0363-463a-a058-e33d768c440b'
    APP_HOST = '127.0.0.1'
    APP_PORT = 5001
    APP_DEBUG = True

    GPU_Node = {
        'tk节点': 'http://proxy.light.catop.top:7202/main'
    }

    DB = {
        "HOST": "49.233.19.76",
        "PORT": 9002,
        "USERNAME": "nlp",
        "PASSWORD": "MTpicNAzL4dxRP6i",
        "DATABASE":"nlp"

    }
