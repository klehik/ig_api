
import logging
from ig_api.authentication import Authentication
from ig_api.instagram_api import API
from ig_api.access_token import AccessTokenRefresh


logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)        
logger.addHandler(ch)