# -*- coding: utf-8 -*

import sys
import unicodedata


class ParsingException(Exception):
    reason = ''
    
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return  self.reason
