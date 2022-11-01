import os
import requests
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from .authentication import Authentication


class AccessTokenRefresh:

    def __init__(self, auth: Authentication) -> None:
        self.auth = auth

    def refresh_long_lived_access_token(self):
        auth = self.auth
        api_version = "v13.0"
        

        url = f"https://graph.facebook.com/{api_version}/oauth/access_token?grant_type=fb_exchange_token&client_id={auth.ig_app_id}&client_secret={auth.client_secret}&fb_exchange_token={auth.access_token}" 
        

        try:
            res = requests.get(url)
            data = res.json()
            
            new_access_token = data['access_token']

            
            os.environ["ACCESS_TOKEN"] = new_access_token
            

            dotenv.set_key(auth.env_path, "ACCESS_TOKEN", os.environ["ACCESS_TOKEN"])
        except Exception as e:
                logging.error("Error refreshing IG access_token, error: {}".format(e), exc_info=True)




        
        
    def get_access_token_exp_date(self):
        """ 
            Get info on an access token 
        
        """
        auth = self.auth

        url = f"https://graph.facebook.com/debug_token?input_token={auth.access_token}&access_token={auth.access_token}"
        
        response = requests.get(url)
        data = response.json()
        return data['data']['expires_at']

        
                

    def access_token_is_expiring(self):
        expires_at = self.get_access_token_exp_date()
        exp_date = datetime.utcfromtimestamp(expires_at)
        delta = timedelta(days=7)


        return (exp_date - delta) < datetime.now()




    def access_token_check(self):
        if self.access_token_is_expiring():
            logging.info("Access token is expiring, refreshing token")
            self.refresh_long_lived_access_token()
            load_dotenv(self.auth.env_path)
        else:
            logging.info("Valid IG access token")