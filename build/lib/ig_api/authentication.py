
from http import client

from dotenv import load_dotenv
import os
class Authentication:

    def __init__(self, env_path):
        load_dotenv(env_path)
        self.env_path = env_path
        self.ig_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID") # instagram_Account_id
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.ig_app_id = os.getenv("CLIENT_ID") #client_id
        self.client_secret = os.getenv("CLIENT_SECRET")# client secret
        self.page_id = os.getenv("PAGE_ID") # facebook page id
        self.username = os.getenv("IG_USERNAME") # ig username
	    

	    
