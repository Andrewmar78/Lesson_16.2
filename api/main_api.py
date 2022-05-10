from flask import Flask, jsonify
from utils import get_users_all

app = Flask(__name__)


@app.route("/api/users")
def get_all_users_json():
    """API для возврата всех пользователей в JSON"""
    data = get_users_all()
    return jsonify(data)


# if __name__ == '__main__':
#     app.run(debug=True)

