import logging
import time
import mimetypes
import logging

from ig_requests import IGrequest

class API:

    def __init__(self, auth=None):
        self.api = IGrequest(auth)
    

    def create_post(self, urls, caption):
        logging.info("Creating Instagram carousel object:")
        media_ids = []
        for url in urls:
            media_ids.append(self.__get_media_carousel_item_id(url))

        
        params = dict()
        params['media_type'] = "CAROUSEL"  # media type
        params['children'] = media_ids # Carousel post ids
        params['caption'] = caption
        params['is_carousel_item'] = False
        api_response = self.api.create_media_object(params)
        carousel_id = api_response['json_data']['id']
        object_status = 'IN_PROGRESS'

        while object_status != 'FINISHED':
            status_response = self.api.get_media_object_status(params, carousel_id)
            logging.info("Media object status: {}".format(object_status))
            object_status = status_response['json_data']['status_code']
            
            time.sleep(10)
            
        logging.info("Media object status: {}".format(object_status))
        
        self.id = carousel_id


    
    def __get_media_carousel_item_id(self, url):
        ''' Returns carousel media id '''

        logging.info("Creating Instagram media object:")

      
        # check media format
        mimetypes.init()
        media_type = mimetypes.guess_type(url)[0]

        if media_type != None: 
            media_type = media_type.split('/')[0].upper()

        if media_type != 'VIDEO' and media_type != 'IMAGE':
            raise TypeError(f"Unsupported media type: {media_type}") 
            

        params = dict()  
        params['media_type'] = media_type 
        params['media_url'] = url
        params['is_carousel_item']=True
        params['caption'] = ''

        api_response = self.api.create_media_object(params)
       
        media_id = api_response['json_data']['id']
        object_status = 'IN_PROGRESS'

        while object_status != 'FINISHED':
            
            status_response = self.api.get_media_object_status(params, media_id)
            logging.info("Media object status: {}".format(object_status))
            object_status = status_response['json_data']['status_code']
            time.sleep(10)
    
        
        logging.info("Media object status: {}".format(object_status))
        return media_id



    def publish(self, id):
        logging.info("Publishing to Instagram:")
        try:

            
            # PUBLISH
            publish_response = self.api.publish_content(self.id) # publish the post to instagram

            if 'error' in publish_response['json_data']:

                logging.error("Published media response error: {}, id: {}".format(publish_response['json_data']['error']['message'], self.id ))
                
    
        except Exception as e:
            print('error')
            logging.error("Error posting content: {}, error: {}".format(self.caption, e), exc_info=True)