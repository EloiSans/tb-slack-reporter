import os
from datetime import datetime as dt
from os.path import join

import matplotlib.pyplot as plt
from slack import WebClient
from tbparse import SummaryReader


class SlackReporter(object):
    def __init__(self, logdir: str, slack_bot_token: str, default_channel: str,
                 save_path: str = "./.tb-slack-tb_slack_reporter", default_message: str = ""):
        self.logdir = logdir
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)
        self.default_channel = default_channel
        self.client = WebClient(slack_bot_token)
        self.default_message = default_message if default_message else f"This are the results at {dt.now().strftime('%Y-%m-%d %H:%M')}"

    def send_scalars(self, message: str = "", channel: str = "", sub_path: str = "", exclude_tags: set = None):
        if exclude_tags is None:
            exclude_tags = set()
        channel = channel if channel else self.default_channel
        message = message if message else self.default_message

        reader = SummaryReader(join(self.logdir, sub_path), extra_columns={'dir_name'})
        df = reader.scalars
        allowed_tags = set(df.tag.unique()) - exclude_tags
        for tag in allowed_tags:
            df_aux = df[df['tag'] == tag].copy()
            df_aux['dir_name'] = [y.replace(tag.replace('/', '_'), '').replace('_', '') for y in df_aux['dir_name']]
            fig, ax = plt.subplots()
            plt.title(tag)
            for k, grp in df_aux.groupby(['dir_name']):
                label = str(k).replace("'", "").replace(",", "")[1:-1]
                ax = grp.plot(ax=ax, kind='line', x='step', y='value', label=label)
            image_path = join(self.save_path, f"{tag.replace('/', '_')}.png")
            plt.savefig(image_path)
            upload_file = self.client.files_upload(channels=channel, title=tag, file=image_path,
                                                   initial_comment=message)
            print(upload_file)
