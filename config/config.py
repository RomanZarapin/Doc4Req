import os
import pathlib
from dotenv import load_dotenv

config = dict()

load_dotenv()

config['root_path'] = str(pathlib.Path(__file__).parent.parent)
config['log_path'] = 'logs'
config['sleep_sec'] = 3
config['secret'] = os.getenv('JWT_HASH_SECRET')
config['access_token_lifetime'] = os.getenv('JWT_ACCESS_TOKEN_LIFETIME')
config['refresh_token_lifetime'] = os.getenv('JWT_REFRESH_TOKEN_LIFETIME')
config['studio_secret'] = 'a6u)_f*@yhpjdnarneamz+q--gce_)5k=i6^3xq$u4re=$p%6-'
config['db'] = None
config['base_url'] = 'http://0.0.0.0'
config['timezone'] = 'UTC'
