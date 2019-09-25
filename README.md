## VWO Python SDK Example

[vwo-python-sdk](https://github.com/wingify/vwo-python-sdk) allows you to A/B Test your Website at server-side.

This repository provides a basic demo of how server-side works with VWO Python SDK.

### Requirements

- python >= 2.7.0 and < 3.0.0

### Documentation

Refer [VWO Official Server-side Documentation](https://developers.vwo.com/reference#server-side-introduction)

### Scripts

1. Install dependencies

```
pip install -r requirements.txt
```

2. Update your app with your settings present in config.py

```python
account_id = 'REPLACE_THIS_WITH_CORRECT_VALUE'
sdk_key = 'REPLACE_THIS_WITH_CORRECT_VALUE'

ab_campaign_key = 'REPLACE_THIS_WITH_CORRECT_VALUE'
ab_campaign_goal_identifeir = 'REPLACE_THIS_WITH_CORRECT_VALUE'
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
vwo_client_instance = vwo.VWO(settings_file)
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

### LICENSE

```text
    MIT License

    Copyright (c) 2019 Wingify Software Pvt. Ltd.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
```
