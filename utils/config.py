import json
import os
import sys
from configparser import ConfigParser, NoSectionError, NoOptionError


class Config:
    def __init__(self):
        self.credential_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
        self.credential_file = 'config'

        self.config = ConfigParser()
        try:
            with open('%s/%s' % (self.credential_path, self.credential_file)) as f:
                self.config.read_file(f)
        except IOError:
            print('ERROR: %s/%s not found' % (self.credential_path, self.credential_file))
            sys.exit(1)

        try:
            self.client_id = self.config.get('Trakt', 'client_id')
        except (NoSectionError, NoOptionError):
            print('ERROR: %s not setup - missing client_id' % self.credential_file)
            sys.exit(1)

        try:
            self.username = self.config.get('Trakt', 'username')
        except (NoSectionError, NoOptionError):
            print('ERROR: %s not setup - missing username' % self.credential_file)
            sys.exit(1)

        try:
            self.client_secret = self.config.get('Trakt', 'client_secret')
        except (NoSectionError, NoOptionError):
            print('ERROR: %s not setup - missing client_secret' % self.credential_file)
            sys.exit(1)

        try:
            user_ids = self.config.get('Plex', 'user_ids')
        except (NoSectionError, NoOptionError):
            print('ERROR: %s not setup - missing user_ids' % self.credential_file)
            sys.exit(1)
        self.user_ids = [int(n) for n in user_ids.split(',')]

        try:
            self.autorization = self.config.get('Trakt', 'authorization')
            self.autorization =  json.loads(self.autorization)
        except (NoSectionError, NoOptionError):
            print('INFO: %s not setup - missing autorization' % self.credential_file)

    def set_value(self, section, option, value):
        self.config.set(section, option, value)

    def write_settings(self):
        """Write config back to settings file"""
        try:
            with open('%s/%s' % (self.credential_path, self.credential_file), 'w') as f:
                self.config.write(f)
        except IOError:
            print('ERROR: unable to write to %s/%s' % (self.credential_path, self.credential_file))
            sys.exit(1)

    def __str__(self):
        return "{\nclient_id: %s,\nusername: %s,\nclient_secret: %s,\nuser_ids: %s\n}" % (self.client_id, self.username, self.client_secret, self.user_ids)
