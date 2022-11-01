import requests
import json


from authentication import Authentication


class IGrequest:
    '''Class for making API calls to Instagram'''

    def __init__(self, auth: Authentication):
        
        self.ig_user_id = auth.user_id
        self.access_token = auth.access_token
        self.endpoint_base = 'https://graph.facebook.com/v14.0/'


    def __make_api_call(self, url, endpoint_params, type) :

        """GET/POST request to API"""
	
        if type == 'POST' : # post request
            data = requests.post(url, endpoint_params)
        else : # get request
            data = requests.get(url, endpoint_params)

        response = dict() # hold response info
        response['url'] = url 
        response['endpoint_params'] = endpoint_params #parameters for the endpoint
        response['json_data'] = json.loads( data.content ) # response data from the api
        

        return response

    def create_media_object(self, params):

        """ Returns media json response with media object id
            response['json_data']['id']
        """

        url =(f"{self.endpoint_base}/{self.ig_user_id}/media")

        endpoint_params = dict() # parameter to send to the endpoint
        endpoint_params['caption'] = params['caption']  # caption for the post
        endpoint_params['access_token'] = self.access_token # access token
        endpoint_params['is_carousel_item'] = params['is_carousel_item'] # carousel item
    
        if params['media_type']  == 'IMAGE': # posting image
            endpoint_params['image_url'] = params['media_url']  # url to the asset
        elif params['media_type'] == 'VIDEO':
            endpoint_params['media_type'] = params['media_type']  # specify media type
            endpoint_params['video_url'] = params['media_url']  # url to the asset
        else: # carousel
            endpoint_params['media_type'] = params['media_type']
            endpoint_params['children[]'] = params['children']
        return self.__make_api_call(url, endpoint_params, 'POST') # make the api call


    def get_media_object_status(self, params, ig_container_id):

        '''
           Request for media object status code, 'PROGRESS', 'FINISHED', 'ERROR'
        '''

        endpoint_params = dict() # parameter to send to the endpoint
        endpoint_params['fields'] = 'status_code' # fields to get back
        endpoint_params['access_token'] = self.access_token # access token
        
        url = f"{self.endpoint_base}/{ig_container_id}"
        
        response = self.__make_api_call(url, endpoint_params, 'GET')
        
        return response


    def publish_content(self, media_object_id,) :
        """ Publish content """
      

        url = f"{self.endpoint_base}/{self.ig_user_id}/media_publish" # endpoint url

        endpoint_params = dict() # parameter to send to the endpoint
        endpoint_params['creation_id'] = media_object_id # fields to get back
        endpoint_params['access_token'] = self.access_token # access token

        return self.__make_api_call( url, endpoint_params, 'POST' ) # make the api call


    def get_ig_api_limit(self) :
        """ Get the api limit 
        
        API Endpoint:
            ?fields=config,quota_usage
        
        """

        url = f"{self.endpoint_base}/{self.ig_user_id}/content_publishing_limit" # endpoint url

        endpoint_params = dict() # parameter to send to the endpoint
        endpoint_params['fields'] = 'config,quota_usage' # fields to get back
        endpoint_params['access_token'] = self.access_token # access token

        return self.__make_api_call(url, endpoint_params, 'GET') # make the api call