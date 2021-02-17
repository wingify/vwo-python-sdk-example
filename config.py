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

AccountDetails = {
    'account_id': '',
    'sdk_key': '',
    # webhook_auth_key: Optional, used when webhooks is enabled
    # 'webhook_auth_key': ''
}

AbCampaignData = {
    'campaign_key': '',
    'campaign_goal_identifier': '',
    'user_id': '',
    'revenue_value': '',
    # custom_variables: Optional param, used for pre-segmentation
    # 'custom_variables': {}
}

FeatureRolloutData =  {
    'campaign_key': '',
    'user_id': '',
    # custom_variables: Optional param, used for pre-segmentation
    # 'custom_variables': {}
}

FeatureTestData = {
    'campaign_key': '',
    'campaign_goal_identifier': '',
    'revenue_value': '',
    'user_id': '',
    # custom_variables: Optional param, used for pre-segmentation
    # 'custom_variables': {}

    'string_variable_key': '',
    'integer_variable_key': '',
    'double_variable_key': '',
    'boolean_variable_key': '',
}

PushData = {
    'tag_key': '',
    'tag_value': '',
    'user_id': '',
}
