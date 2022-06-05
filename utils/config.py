import os
import sys
from configparser import ConfigParser, NoSectionError, NoOptionError


class Config:
    def __init__(self):
        self.credential_path = os.path.dirname(os.path.realpath(__file__))
        self.credential_file = 'config'

        self.config = ConfigParser()
        try:
            with open('%s/%s' % (credential_path, credential_file)) as f:
                self.config.read_file(f)
        except IOError:
            print('ERROR: %s/%s not found' % (credential_path, credential_file))
            sys.exit(1)

        try:
            self.client_id = self.config.get('Trakt', 'client_id')
        except (NoSectionError, NoOptionError):
            print('ERROR: %s not setup - missing client_id' % credential_file)
            sys.exit(1)

        try:
            self.username = self.config.get('Trakt', 'username')
        except (NoSectionError, NoOptionError):
            print('ERROR: %s not setup - missing username' % credential_file)
            sys.exit(1)

        try:
            self.client_secret = self.config.get('Trakt', 'client_secret')
        except (NoSectionError, NoOptionError):
            print('ERROR: %s not setup - missing client_secret' % credential_file)
            sys.exit(1)

        try:
            user_ids = self.config.get('Plex', 'user_ids')
        except (NoSectionError, NoOptionError):
            print('ERROR: %s not setup - missing user_ids' % self.credential_file)
            sys.exit(1)
        self.user_ids = user_ids.split(',')

    def write_settings(self):
        """Write config back to settings file"""
        try:
            with open('%s/%s' % (self.credential_path, self.credential_file), 'w') as f:
                self.config.write(f)
        except IOError:
            print('ERROR: unable to write to %s/%s' % (self.credential_path, self.credential_file))
            sys.exit(1)