## VWO Python SDK Example

[vwo-python-sdk](https://github.com/wingify/vwo-python-sdk) allows you to A/B Test your Website at server-side.

This repository provides a basic demo of how server-side works with VWO Python SDK.

### Requirements

- python 2.7+

### Documentation

Refer [VWO Official FullStack Documentation](https://developers.vwo.com/reference#fullstack-introduction)

### Scripts

1. Install dependencies

```
pip install -r requirements.txt
```

2. Update your app with your settings present in `config.py`

```python
AccountDetails = {
    'account_id': '',
    'sdk_key': '',
}

AbCampaignData = {
    'campaign_key': '',
    'campaign_goal_identifier': '',
    'user_id': '',
    'revenue_value': '',
    # custom_variables: Optional param, used for pre-segmentation
}

FeatureRolloutData =  {
    'campaign_key': '',
    'user_id': '',
    # custom_variables: Optional param, used for pre-segmentation
}

FeatureTestData = {
    'campaign_key': '',
    'campaign_goal_identifier': '',
    'revenue_value': '',
    'user_id': '',
    # custom_variables: Optional param, used for pre-segmentation

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
```

3. Run application

```
python server.py
```

### Basic usage

**Importing and Instantiation**

```python
import vwo

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.launch(settings_file)
```

**API usage**

```python
# activate API
variation_name = vwo_client_instance.activate(ab_campaign_key, user_id)

# get_variation_name API
variation_name = vwo_client_instance.get_variation_name(ab_campaign_key, user_id)

# track API
vwo_client_instance.track(ab_campaign_key, user_id, ab_campaign_goal_identifeir, revenue_value)
```

**Log Level** - pass log level to SDK

```python
import vwo
from vwo import LogLevels

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.VWO(settings_file, log_level = LogLevels.DEBUG)
```

**Custom Logger** - implement your own logger method

```python
import vwo

class CustomLogger:
   def log(self, level, message):
      print(level, message)
      # ...write to file or database or integrate with any third-party service

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.VWO(settings_file, logger = CustomLogger())
```

**User Storage Service**

```python
import vwo
from vwo import UserStorage

class user_storage(UserStorage):
  def get(self, user_id, campaign_key):
    # ...code here for getting data
    # return data

  def set(self, user_storage_data):
    # ...code to persist data

user_storage_instance = user_storage()

settings_file = vwo.get_settings_file(account_id, sdk_key)
vwo_client_instance = vwo.VWO(settings_file, user_storage = user_storage_instance)
```

## License

[Apache License, Version 2.0](https://github.com/wingify/vwo-python-sdk-example/blob/master/LICENSE)

Copyright 2019-2021 Wingify Software Pvt. Ltd.
