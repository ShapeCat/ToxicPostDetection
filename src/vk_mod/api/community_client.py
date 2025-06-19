from .base_client import BaseAPIClient


class CommunityClient(BaseAPIClient):

    def get_info(self, group_id: str|None = None, fields:list[str]=[]) -> dict[str, str]:
        params = {
            "group_ids": group_id,
            "fields": ','.join(fields)
            } 
        return self.get_request("groups.getById", params)["groups"][0]

    def get_name(self, group_id: str|None = None) -> str:
        return self.get_info(group_id, ['screen_name'])["name"]

    def get_screen_name(self, group_id: str|None = None) -> str:
        return self.get_info(group_id, ['screen_name'])["screen_name"]
    
    def get_link(self, group_id: str|None = None) -> str:
        screen_name = self.get_screen_name(group_id)
        return f"https://vk.com/{screen_name}"
