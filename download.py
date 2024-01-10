import wget
import os
import re


class Download:
    def __init__(self):
        self.pattern = r"[\/\\\:\*\?\"\<\>\|]"

    def rm_unavail_char(self, old_name):
        new_title = re.sub(self.pattern, "", old_name)
        return new_title

    def download_track(self, url, f_name):
        file_name = rm_unavail_char(f_name)
        wget(url, f'download{os.sepline}{file_name}')
