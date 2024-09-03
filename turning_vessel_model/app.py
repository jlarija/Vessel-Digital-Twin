from flask import Flask
from flask_cors import CORS
import numpy as np
from fe_ek import predict
from vessel import Vessel

app = Flask(__name__)
CORS(app)


@app.route("/sim")
def hello_world():
    timestamp, x_state, x_hat, theta, theta_hat = predict(
        t_tot=80,
        ti=0,
        dt=0.01,
        u_input=np.array([1, 0], dtype=float))

    new_dict = {}

    for i in range(len(timestamp)):
        inner_dict = {}
        inner_dict['x'] = x_state[i][0]
        inner_dict['y'] = x_state[i][1]
        inner_dict['psi'] = x_state[i][2]
        inner_dict['u'] = x_state[i][3]
        inner_dict['v'] = x_state[i][4]
        inner_dict['r'] = x_state[i][5]
        inner_dict['t'] = timestamp[i]
        new_dict[i] = inner_dict

    return (new_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4999, debug=True)
