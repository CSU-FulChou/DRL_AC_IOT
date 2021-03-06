'''
Author: Ful Chou
Date: 2021-03-22 12:04:41
LastEditors: Ful Chou
LastEditTime: 2021-03-31 10:37:22
FilePath: /RL-Adventure-2/http_server.py
Description: What this document does
'''



from flask import Flask, app
from flask.globals import request
from a2c_train import get_status_return_model_parameters
from a2c_train import a2c_env_param
from gae_tran import gae_env_param
from gae_tran import gae_update_model
from atari_tran import atari_state_model_params
from ddpg_train import ddpg_policy_update
import numpy as np
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hellollll'


@app.route('/atari/ac', methods=['POST'])
def atari_status_model():
    data = json.loads(request.data)
    return atari_state_model_params(data)


@app.route('/get_a2c_env_param')
def get_a2c_env_param():
    return json.dumps(a2c_env_param)


@app.route('/sendStatus', methods=['POST'])
def sendStatus():
    data = request.data
    data = json.loads(data)
    parameters = get_status_return_model_parameters(status=data)
    return json.dumps(parameters)


@app.route('/get_gae_env_param')
def get_gae_env_param():
    return json.dumps(gae_env_param)


@app.route('/gae_update_model', methods=['POST'])
def _gae_update_model():
    data = request.data
    data = json.loads(data)
    parameters = gae_update_model(status=data)
    return json.dumps(parameters)


@app.route('/ddpg_policy_update', methods=['GET'])
def _ddpg_policy_update():
    parameters = ddpg_policy_update()
    return json.dumps(parameters)


@app.route('/add2replay_buffer', methods=['POST'])
def _add2replay_buffer():
    data = request.data
    data = json.loads(data)
    state = np.array(data['state'])
    action = np.array(data['action'])
    reward = float(data['reward'])
    next_state = np.array(data['next_state'])
    done = bool(data['done'])
    from ddpg_train import replay_buffer
    replay_buffer.push(state, action, reward, next_state, done)
    return 'success'


@app.route('/ddpg_update', methods=['GET'])
def _ddpg_update():
    from ddpg_train import ddpg_update
    ddpg_update()
    return 'success'


if __name__ == '__main__':
    # macos local ip: 192.168.199.128
    app.run(host='0.0.0.0', port=5000, debug=True)
