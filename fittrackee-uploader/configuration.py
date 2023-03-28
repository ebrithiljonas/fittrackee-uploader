import json
import os
from config_path import ConfigPath

class Configuration:

    config = {}
    server_url = ""
    email = ""
    token = ""
    folder = ""
    uploaded_folder = ""
    move_after_upload = False
    add_info_to_file_name = False
    add_stats = True

    def __init__(self):
        conf_path = ConfigPath( 'FitTrackee_Uploader', 'ebrithiljonas', '.json' )
        self.path = os.path.join(conf_path.saveFolderPath(mkdir=True), 'config.json')

        if os.path.isfile(self.path):
            with open(self.path) as conf_file:
                self.config = json.load(conf_file)
                self.server_url = self.config['server_url']
                self.email = self.config['email']
                self.token = self.config['token']
                self.folder = self.config['folder']
                self.uploaded_folder = self.config['uploaded_folder']
                self.move_after_upload = self.config['move_after_upload']
                self.add_info_to_file_name = self.config['add_info_to_file_name']
                self.add_stats = self.config['add_stats']

    def saveConfig(self):
        self.config['server_url'] = self.server_url
        self.config['email'] = self.email
        self.config['token'] = self.token
        self.config['folder'] = self.folder
        self.config['uploaded_folder'] = self.uploaded_folder
        self.config['move_after_upload'] = self.move_after_upload
        self.config['add_info_to_file_name'] = self.add_info_to_file_name
        self.config['add_stats'] = self.add_stats

        json_conf = json.dumps(self.config, indent=4)
        with open(self.path, "w") as outfile:
            outfile.write(json_conf)