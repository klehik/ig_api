import os
import requests
import dotenv
import logging
from datetime import datetime, timedelta
from .authentication import Authentication


class AccessTokenRefresh:

    def __init__(self, auth: Authentication) -> None:
        self.auth = auth


    def refresh_access_token(self):
        # updates short lived access token to long lived
        auth = self.auth
        
            
        url = f'https://graph.facebook.com/v15.0/oauth/access_token?grant_type=fb_exchange_token&client_id={auth.ig_app_id}&client_secret={auth.client_secret}&fb_exchange_token={auth.access_token}' 
        

        try:
            response = requests.get(url)
            print(response)
            data = response.json()
            print(data)
            new_access_token = data['access_token']
            expires_in = round(data['expires_in'] / 86400, None)

            logging.info('New long-lived access token: {}'.format(new_access_token))
            logging.info('Access token is valid for: {} days'.format(expires_in))
            
            os.environ['ACCESS_TOKEN'] = new_access_token
            

            dotenv.set_key(auth.env_path, 'ACCESS_TOKEN', os.environ['ACCESS_TOKEN'])
        except Exception as e:
                logging.error('Error refreshing IG access_token, error: {}'.format(e), exc_info=True)

        
        
    """ def get_access_token_exp_date(self):
        auth = self.auth
        url = f'https://graph.facebook.com/debug_token?input_token={auth.access_token}&access_token={auth.access_token}'
        
        response = requests.get(url)
        data = response.json()
        
        return data['data']['expires_at']
        

        
                

    def access_token_is_expiring(self):
            
        expires_at = self.get_access_token_exp_date() 
        exp_date = datetime.utcfromtimestamp(expires_at)
        logging.info('Access token is expiring at: {}'.format(exp_date))
        delta = timedelta(days=40)
        return (exp_date - delta) < datetime.now()
        




    def access_token_refresh(self):
        
        try: 
            if self.access_token_is_expiring():
                logging.info('Access token is expiring soon, refreshing token')
                self.refresh_access_token()
                dotenv.load_dotenv(self.auth.env_path)
            else:
                logging.info('Valid IG access token')

        except Exception as e:
                logging.error('Error debugging access token, error: {}'.format(e))
                return None """