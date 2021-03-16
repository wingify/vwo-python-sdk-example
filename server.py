# Copyright 2019-2021 Wingify Software Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import json
import threading
from flask import jsonify

import vwo
from flask import Flask, jsonify, render_template, request, abort, make_response
from vwo import LOG_LEVELS, UserStorage

try:
    from dev_config import (AbCampaignData, AccountDetails, FeatureRolloutData,
                    FeatureTestData, PushData)
except:
    from config import (AbCampaignData, AccountDetails, FeatureRolloutData,
                    FeatureTestData, PushData)
from util import get_random_user

app = Flask(__name__)

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

def update_sdk_settings_file(is_via_webhook=False):
    global vwo_client_instance
    global settings_file

    if vwo_client_instance:
        settings_file = vwo_client_instance.get_and_update_settings_file(AccountDetails.get('account_id'), 
                                                AccountDetails.get('sdk_key'), 
                                                is_via_webhook)

def flush_callback(err, events):
    print(err)
    print(events)

class Integrations(object):
    def __init__(self):
        pass

    def callback(self, properties):
        print(properties)

def init_sdk():
    global vwo_client_instance
    global settings_file

    new_settings_file = vwo.get_settings_file(AccountDetails.get('account_id'), AccountDetails.get('sdk_key'))

    # Uncomment below code to read settings_file from local settingsFile.json

    # with open('test_settings_file.json') as json_file:
    #     new_settings_file = json.dumps(json.load(json_file))

    print('settingsFile fetched')

    if new_settings_file != settings_file:
        settings_file = new_settings_file

        print('VWO SDK instance created')
        vwo_client_instance = vwo.launch(
            settings_file,
            # Enable UserStorage and add code in get and set method
            # user_storage = user_storage_instance
            # Enable custom logger to check how it works
            # logger = CustomLogger()
            log_level = LOG_LEVELS.DEBUG,
            # uncomment batch_events to enable event batching
            # batch_events={
            #     'events_per_request': 5,
            #     'request_time_interval': 60,
            #     'flush_callback': flush_callback
            # }
            # integrations=Integrations()
        )

init_sdk()
# set_interval(update_sdk_settings_file, POLL_TIME)


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/ab')
def ab_campaign():
    req_user_id = request.args.get('userId')

    if req_user_id == None:
        user_id = AbCampaignData.get('user_id') or get_random_user()
    else:
        user_id = str(req_user_id)

    variation_name = vwo_client_instance.activate(AbCampaignData.get('campaign_key'),
                                                  user_id,
                                                  custom_variables=AbCampaignData.get('custom_variables'))

    if variation_name:
      is_part_of_campaign = True
    else:
      is_part_of_campaign = False

    vwo_client_instance.track(AbCampaignData.get('campaign_key'),
                              user_id,
                              AbCampaignData.get('campaign_goal_identifier'),
                              revenue_value=AbCampaignData.get('revenue_value'))

    return render_template(
        'ab.html',
        user_id = user_id,
        campaign_type = "Visual-AB",
        is_part_of_campaign = is_part_of_campaign,
        variation_name = variation_name,
        ab_campaign_key = AbCampaignData.get('campaign_key'),
        ab_campaign_goal_identifier = AbCampaignData.get('campaign_goal_identifier'),
        custom_variables = json.dumps(AbCampaignData.get('custom_variables'), sort_keys = True, indent = 4, separators = (',', ': ')),
        settings_file = json.dumps(json.loads(settings_file), sort_keys = True, indent = 4, separators = (',', ': '))
    )


@app.route('/feature-rollout')
def feature_rollout_campaign():
    req_user_id = request.args.get('userId')

    if req_user_id == None:
        user_id = FeatureRolloutData.get('user_id') or get_random_user()
    else:
        user_id = str(req_user_id)

    is_user_part_of_feature_rollout_campaign = vwo_client_instance.is_feature_enabled(FeatureRolloutData.get('campaign_key'),
                                                                                      user_id,
                                                                                      custom_variables=FeatureRolloutData.get('custom_variables'))

    return render_template(
        'feature-rollout.html',
        campaign_type = "Feature-rollout",
        user_id = user_id,
        is_user_part_of_feature_rollout_campaign = is_user_part_of_feature_rollout_campaign,
        feature_rollout_campaign_key = FeatureRolloutData.get('campaign_key'),
        custom_variables = json.dumps(FeatureRolloutData.get('custom_variables'), sort_keys = True, indent = 4, separators = (',', ': ')),
        settings_file = json.dumps(json.loads(settings_file), sort_keys = True, indent = 4, separators = (',', ': '))
    )


@app.route('/feature-test')
def feature_campaign():
    req_user_id = request.args.get('userId')

    if req_user_id == None:
        user_id = FeatureTestData.get('user_id') or get_random_user()
    else:
        user_id = str(req_user_id)

    is_user_part_of_feature_campaign = vwo_client_instance.is_feature_enabled(FeatureTestData.get('campaign_key'), user_id)

    vwo_client_instance.track(FeatureTestData.get('campaign_key'),
                              user_id,
                              FeatureTestData.get('campaign_goal_identifier'),
                              revenue_value=FeatureTestData.get('revenue_value'),
                              custom_variables=FeatureTestData.get('custom_variables'))

    string_variable = vwo_client_instance.get_feature_variable_value(FeatureTestData.get('campaign_key'),
                                                                     FeatureTestData.get('string_variable_key'),
                                                                     user_id,
                                                                     custom_variables=FeatureTestData.get('custom_variables'))
    integer_variable = vwo_client_instance.get_feature_variable_value(FeatureTestData.get('campaign_key'),
                                                                     FeatureTestData.get('integer_variable_key'),
                                                                     user_id,
                                                                     custom_variables=FeatureTestData.get('custom_variables'))
    boolean_variable = vwo_client_instance.get_feature_variable_value(FeatureTestData.get('campaign_key'),
                                                                     FeatureTestData.get('boolean_variable_key'),
                                                                     user_id,
                                                                     custom_variables=FeatureTestData.get('custom_variables'))
    double_variable = vwo_client_instance.get_feature_variable_value(FeatureTestData.get('campaign_key'),
                                                                     FeatureTestData.get('double_variable_key'),
                                                                     user_id,
                                                                     custom_variables=FeatureTestData.get('custom_variables'))

    return render_template(
        'feature-test.html',
        user_id = user_id,
        campaign_type = "Feature-test",
        is_user_part_of_feature_campaign = is_user_part_of_feature_campaign,
        feature_campaign_key = FeatureTestData.get('campaign_key'),
        feature_campaign_goal_identifier = FeatureTestData.get('campaign_goal_identifier'),
        string_variable = string_variable,
        integer_variable = integer_variable,
        boolean_variable = boolean_variable,
        double_variable = double_variable,
        custom_variables = json.dumps(FeatureTestData.get('custom_variables'), sort_keys = True, indent = 4, separators = (',', ': ')),
        settings_file = json.dumps(json.loads(settings_file), sort_keys = True, indent = 4, separators = (',', ': '))
    )


@app.route('/push')
def push_api():
    req_user_id = request.args.get('userId')

    if req_user_id == None:
        user_id = PushData.get('user_id') or get_random_user()
    else:
        user_id = str(req_user_id)

    result = vwo_client_instance.push(PushData.get('tag_key'), PushData.get('tag_value'), user_id)

    return render_template(
        'push.html',
        user_id = user_id,
        tag_key = PushData.get('tag_key'),
        tag_value = PushData.get('tag_value'),
        result = result,
        settings_file = json.dumps(json.loads(settings_file), sort_keys = True, indent = 4, separators = (',', ': '))
    )

@app.route('/webhook', methods=['POST'])
def webhook():
    print('\nWEBHOOK TRIGGERED, {body}, \nWebhook Auth Key: {webhook_auth_key}'
        .format(body=request.json, webhook_auth_key=request.headers.get('x-vwo-auth'))
        )

    WEBHOOK_AUTH_KEY = AccountDetails.get('webhook_auth_key')
    if WEBHOOK_AUTH_KEY and request.headers.get('x-vwo-auth'):
        if WEBHOOK_AUTH_KEY != request.headers.get('x-vwo-auth'):
            print('Webhook api authentication failed')
            return make_response(jsonify({'status': 'failure', 'message': 'webhook api authentication failed'}), 200)
        else:
            print('Webhook api authentication successful')
    else:
        print('Skipping authentication as missing webhook authentication key')

    update_sdk_settings_file(True)
    return make_response(jsonify({'status': 'success', 'message': 'settings updated successfully'}), 200)




@app.route("/flush-events")
def flush_events():
    mode = request.args.get("mode")
    vwo_client_instance.flush_events(mode=mode)
    return jsonify({'success':True})


if __name__ == '__main__':
    app.run(debug = True)
