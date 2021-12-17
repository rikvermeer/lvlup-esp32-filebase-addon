from esp32 import NVS
import json

class Config(NVS):
    namespace = 'lvlup'
    json_key = 'config'
    json_length_key = 'config_length'
    __config = {}
    
    config_file = '/config/default.json'
    
    default_config = {
#        'wifiSSID': 'Stichting De Melkweg',
#        'wifiPSK': 'melkweggast',
#        'server': 'c4c.lvl-up.dev',
#        'tls': True,
#        'tls_params': {},
    }
    
    def __init__(self, config=None):
        super().__init__(self.namespace)
        config = config if config else self.default_config
        self.__config.update(config)
        try:
            self.__config.update(self.from_file())
        except Exception as e:
            print('Couldnt load json file:\n', e)
        
        try:
           self.__config.update(self.load_NVS())
        except Exception as e:
            print('Couldnt load NVS:\n', e)
        
        self.commit()
        
    def load_NVS(self):
        clength = self.get_i32(self.json_length_key)

        barr = bytearray(clength)
        lread = self.get_blob(self.json_key, barr)

        if lread != clength:
            print(lread, clength, 'do not match')
            raise Exception()

        return json.loads(barr)
    
    def from_NVS(self):
        clength = self.get_i32(self.json_length_key)

        barr = bytearray(clength)
        lread = self.get_blob(self.json_key, barr)

        if lread != clength:
            print(lread, clength, 'do not match')
            raise Exception()

        self.__config = json.loads(barr)
    
    def to_NVS(self):
        self.commit()

    def from_file(self):
        with open(self.config_file, 'r') as f:
            print('loading config file', self.config_file)
            cfg = f.read()
            return json.loads(cfg)
        
    def load_file(self, autocommit=False):
        self.__config = from_file()
        if autocommit:
            self.commit()
    
    def to_file(self, config):
        with open(self.config_file, 'w+') as f:
            print('storing config file', self.config_file)
            json.dump(config, f)
    
    def store_file(self):
        self.to_file(self.config)
        
    @property
    def config(self):
        return self.__config
    
    @config.setter
    def config(self, config):
        self.__config = config
    
    @property
    def keys(self):
        return self.config.keys()
    
    def commit(self, config=None):
        config = config if config else self.config
        jconfig = json.dumps(config)
        lconfig = len(jconfig)
        print('Committing: ', self.json_key, lconfig, '\n', jconfig)
        self.set_blob(self.json_key, jconfig)
        self.set_i32(self.json_length_key,lconfig)
        super().commit()
