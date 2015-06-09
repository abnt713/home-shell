__author__ = 'alisonbnt'

import glob
import json


class SchemeLoader:

    def __init__(self):
        self.scheme_rel = {}
        self.load_scheme()

    def load_scheme(self):
        if len(self.scheme_rel) <= 0:
            schemes_files = glob.glob('schemes/*.json')
            for scheme in schemes_files:
                with open(scheme) as data_file:
                    data = json.load(data_file)

                scheme_data = data['schemes']
                self.scheme_rel.update(scheme_data)

    def get_scheme(self, package):
        return self.scheme_rel[package]