from __future__ import print_function
import vwo
from vwo import UserStorage, LogLevels

from config import *

import json
import threading

from util import get_random_user
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

from vwo import logger

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

POLL_TIME = 10
vwo_client_instance = None
settings_file = None

# User Storage Service Example
client_db = {}
class user_storage(UserStorage):
  def get(self, user_id, campaign_key):
    # Search in client_db
    return client_db.get((user_id, campaign_key))

  def set(self, user_storage_data):
    # Store in client_db against tuple of userId and campaignKey
    client_db[(user_storage_data['userId'], user_storage_data['campaignKey'])] = user_storage_data

user_storage_instance = user_storage()


def init_sdk():
    global vwo_client_instance
    global settings_file

    # new_settings_file = vwo.get_settings_file(account_id, sdk_key)
    with open('test_settings_file.json') as json_file:
        new_settings_file = json.dumps(json.load(json_file))

    print('settingsFile fetched')

    if new_settings_file != settings_file:
        settings_file = new_settings_file

        print('VWO SDK instance created')
        vwo_client_instance = vwo.VWO(
            settings_file,
            # Enable UserStorage and add code in get and set method
            # user_storage = user_storage_instance
            # Enable custom logger to check how it works
            # logger = CustomLogger()
            log_level = LogLevels.DEBUG
        )

init_sdk()
# set_interval(init_sdk, POLL_TIME)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/ab')
def ab_campaign():
    print(ab_campaign_key)
    req_user_id = request.args.get('userId')

    if req_user_id == None:
        user_id = get_random_user()
    else:
        user_id = str(req_user_id)

    print(user_id)

    variation_name = vwo_client_instance.activate(ab_campaign_key, user_id)

    if variation_name:
      is_part_of_campaign = True
    else:
      is_part_of_campaign = False

    revenue_value = 1234
    vwo_client_instance.track(ab_campaign_key, user_id, ab_campaign_goal_identifier, revenue_value)

    return render_template(
        'ab.html',
        user_id = user_id,
        campaign_type = "Visual-AB",
        is_part_of_campaign = is_part_of_campaign,
        variation_name = variation_name,
        ab_campaign_key = ab_campaign_key,
        ab_campaign_goal_identifier = ab_campaign_goal_identifier,
        settings_file = json.dumps(json.loads(settings_file), sort_keys = True, indent = 4, separators = (',', ': '))
    )

@app.route('/feature-rollout')
def feature_rollout_campaign():
    print(feature_rollout_campaign_key)
    req_user_id = request.args.get('userId')

    if req_user_id == None:
        user_id = get_random_user()
    else:
        user_id = str(req_user_id)

    print(user_id)

    is_user_part_of_feature_rollout_campaign = vwo_client_instance.is_feature_enabled(feature_rollout_campaign_key, user_id)

    return render_template(
        'feature-rollout.html',
        campaign_type = "Feature-rollout",
        user_id = user_id,
        is_user_part_of_feature_rollout_campaign = is_user_part_of_feature_rollout_campaign,
        feature_rollout_campaign_key = feature_rollout_campaign_key,
        settings_file = json.dumps(json.loads(settings_file), sort_keys = True, indent = 4, separators = (',', ': '))
    )

@app.route('/feature-test')
def feature_campaign():
    print(feature_campaign_key)
    req_user_id = request.args.get('userId')

    if req_user_id == None:
        user_id = get_random_user()
    else:
        user_id = str(req_user_id)

    print(user_id)
    is_user_part_of_feature_campaign = vwo_client_instance.is_feature_enabled(feature_campaign_key, user_id)
    print(is_user_part_of_feature_campaign)
    revenue_value = 1234
    vwo_client_instance.track(feature_campaign_key, user_id, feature_campaign_goal_identifier, revenue_value)

    string_variable = vwo_client_instance.get_feature_variable_value(feature_campaign_key, string_variable_key, user_id)
    integer_variable = vwo_client_instance.get_feature_variable_value(feature_campaign_key, integer_variable_key, user_id)
    boolean_variable = vwo_client_instance.get_feature_variable_value(feature_campaign_key, boolean_variable_key, user_id)
    double_variable = vwo_client_instance.get_feature_variable_value(feature_campaign_key, double_variable_key, user_id)

    return render_template(
        'feature-test.html',
        user_id = user_id,
        campaign_type = "Feature-test",
        is_user_part_of_feature_campaign = is_user_part_of_feature_campaign,
        feature_campaign_key = feature_campaign_key,
        feature_campaign_goal_identifier = feature_campaign_goal_identifier,
        string_variable = string_variable,
        integer_variable = integer_variable,
        boolean_variable = boolean_variable,
        double_variable = double_variable,
        settings_file = json.dumps(json.loads(settings_file), sort_keys = True, indent = 4, separators = (',', ': '))
    )

if __name__ == '__main__':
    app.run(debug = True)
