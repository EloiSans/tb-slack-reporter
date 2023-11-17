# tb-slack-reporter
This package helps you send Pytorch's TensorBoard's results into your Slack. 
The main dependency is [tbparse](https://pypi.org/project/tbparse/).
Is not published to Pypi yet, because it is a **work in progress**

## Installation
```bash
pip install git+https://github.com/EloiSans/tb-slack-reporter
```

## Usage
1. Save the `SLACK_BOT_TOKEN` as an environment variable. (example using .env)
2. Instance the class

```python
import os

from dotenv import load_dotenv
from torch.utils.tensorboard import SummaryWriter
from tb_slack_reporter import SlackReporter

load_dotenv()

logdir = "<PATH TO SAVE THE TENSORBOARD'S LOG>"
tb_writer = SummaryWriter(log_dir=logdir)
reporter = SlackReporter(logdir, os.environ['SLACK_BOT_TOKEN'], default_channel="<channel_id>")
```
3. Call the method `.send_scalars` every time you want to be reported
```python
...
if epoch % 100 == 0:
    reporter.send_scalars()
...
```
This is the most basic use, read the following tips for advanced usage
## Tips
### 1. Personalize the save path
By default, the images are stored in `./.tb-slack-tb_slack_reporter`, add this to `.gitignore` or write your desired path.

### 2. Default message
You can set a default message in the instance of the class `SlackReporter(..., default_message="<MY MESSAGE>")`,
that will be sent in every message. If you want to personalize each message you can pass it in the `.send_scalars` call
```python
...
if epoch % 100 == 0:
    reporter.send_scalars(..., message="<MY COOL MESSAGE>")
...
```

### 3. Default channel
You can pass another channel_id to `.send_scalars` method to send the message to a particular channel, skipping the default one
```python
...
if epoch % 100 == 0:
    reporter.send_scalars(..., channel="<MY PARTICULAR CHANNEL>")
...
```

### 4. Sub-paths
Due to your log_dir's structure you may want to have the reporter being aware of all the directory, but send the children paths in different messages.
You can use `sub_path` parameter to go deeper on your log_dir path
```python
...
if epoch % 100 == 0:
    reporter.send_scalars(..., sub_path="<MY PARTICULAR PATH>")
...
```

### 5. Exclude tags
If there are TensorBoard tags that you don't want to report, add them in a set in the parameter `exclude_tags`
```python
...
if epoch % 100 == 0:
    reporter.send_scalars(..., exclude_tags=set(["tag_1", "tag_2"]))
...
```

## Need more help?
You need to generate a Slack app to get the `SLACK_BOT_TOKEN`. Look at [this documentation](https://api.slack.com/tutorials/uploading-files-with-python) for a detailed config 
