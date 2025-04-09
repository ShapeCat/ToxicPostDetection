import requests
from typing import Dict, Any
from .exceptions import VKAPIError


class BaseAPIClient:
    url = 'https://api.vk.com/method/'
    api_version = 5.199

    def __init__(self, access_token:str,  community_token:str, service_key:str) -> None:
        self.access_token = access_token 
        self.community_token = community_token
        self.service_key = service_key

    def post_request(self, method:str, params:Dict[str, Any], access_token:str=None) -> Dict[str, str]:
        params.update({
            'access_token': access_token if access_token  else self.access_token,
            'v': self.api_version
        })
        
        response = requests.post(self.url+method, params=params)
        response.raise_for_status()
        json_response = response.json()
        
        if 'error' in json_response:
            error = json_response['error']
            raise VKAPIError(f"There is an error while calling VK API {method} method: {error['error_msg']}({error['error_code']})")          
        return json_response.get('response')
    
    def get_request(self, method:str, params:Dict[str, Any], access_token:str=None) -> Dict[str, str]:
        params.update({
            'access_token': access_token if access_token  else self.access_token,
            'v': self.api_version
        })
        
        response = requests.get(self.url+method, params=params)
        response.raise_for_status()
        json_response = response.json()
        
        if 'error' in json_response:
            error = json_response['error']
            raise VKAPIError(f"There is an error while calling VK API {method} method: {error['error_msg']}({error['error_code']})")               
        return json_response.get('response')
