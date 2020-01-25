#! /usr/bin/env python 

class BaseTask:
    """
    A base task is a minimal definition on what is to be downloaded
    """

    def __init__(self):
        self.name = ""
        self.downloader_type = ""
        self.expanded = ""