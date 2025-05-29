from flask import jsonify

class APIResponse:
    @staticmethod
    def success(data=None, message="Success"):
        return jsonify({
            "code": 1,
            "message": message,
            "data": data
        }), 200

    @staticmethod
    def error(message, status_code=400):
        return jsonify({
            "code": 0,
            "message": message,
            "data": None
        }), status_code