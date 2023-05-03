import logging
import time
import mimetypes
import logging

from .ig_requests import IGrequest

class API:

    def __init__(self, auth=None):
        self.api = IGrequest(auth)



    def create_post(self, urls, caption):

        if urls == None:
            raise ValueError("No media provided")
        
        if len(urls) > 1:

            media_id = self.__create_carousel_post(urls, caption)

        else:
            media_id = self.__create_single_post(urls[0], caption)
            

        self.__publish(media_id)

    def __create_single_post(self,url, caption):

        return self.__get_media_item_id(url, False, caption)
        


    
    def __create_carousel_post(self,urls, caption):

        logging.info("Creating Instagram carousel object:")
        media_ids = []
        for url in urls:
            media_ids.append(self.__get_media_item_id(url, True, ''))

        
        params = dict()
        params['media_type'] = "CAROUSEL"  # media type
        params['children'] = media_ids # Carousel post ids
        params['caption'] = caption
        params['is_carousel_item'] = False
        api_response = self.api.create_media_object(params)
        print(api_response)
        post_id = api_response['json_data']['id']
        object_status = 'IN_PROGRESS'

        while object_status != 'FINISHED':
            status_response = self.api.get_media_object_status(params, post_id)
            logging.info("Media object status: {}".format(object_status))
            object_status = status_response['json_data']['status_code']
            
            time.sleep(10)
            
        logging.info("Media object status: {}".format(object_status))
        
        return post_id


    
    def __get_media_item_id(self, url, is_carousel, caption):
        ''' Returns media id '''

        logging.info("Creating Instagram media object:")

      
        # check media format
        mimetypes.init()
        media_type = mimetypes.guess_type(url)[0]

        if media_type != None: 
            media_type = media_type.split('/')[0].upper()

        if media_type != 'VIDEO' and media_type != 'IMAGE':
            raise Exception(f"Unsupported media type: {media_type}") 
            

        params = dict()  
        params['media_type'] = media_type 
        params['media_url'] = url
        params['is_carousel_item']=is_carousel
        params['caption'] = caption

        api_response = self.api.create_media_object(params)
        print(api_response)

        if 'error' in api_response['json_data']:
            raise ValueError(api_response['json_data']['error']['message'])
        media_id = api_response['json_data']['id']
        object_status = 'IN_PROGRESS'

        while object_status != 'FINISHED':
            
            status_response = self.api.get_media_object_status(params, media_id)
            logging.info("Media object status: {}".format(object_status))
            object_status = status_response['json_data']['status_code']
            time.sleep(10)
    
        
        logging.info("Media object status: {}".format(object_status))
        return media_id



    def __publish(self, id):
        logging.info("Publishing to Instagram:")
        try:

            
            # PUBLISH
            publish_response = self.api.publish_content(id) # publish the post to instagram

            if 'error' in publish_response['json_data']:

                logging.error("Published media response error: {}, id: {}".format(publish_response['json_data']['error']['message'], self.id ))
                
    
        except Exception as e:
            print('error')
            logging.error("Error posting content: {}, error: {}".format(self.caption, e), exc_info=True)