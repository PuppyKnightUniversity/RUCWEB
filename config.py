import configparser
import os

class Config(object):

    def __init__(self, config_file='config.init'):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.init")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8')

    def get(self, section, name, strip_blank=True, strip_quote=True):
        s = self._config.get(section, name)
        if strip_blank:
            s = s.strip()
        if strip_quote:
            s = s.strip('"').strip("'")

        return s

    def getboolean(self, section, name):
        return self._config.getboolean(section, name)



if __name__ == "__main__":
    TestConfig = Config()
    print(TestConfig.get('messenger', 'sckey'))


