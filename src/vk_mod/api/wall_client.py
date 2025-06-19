from .base_client import BaseAPIClient
from typing import Literal

class WallClient(BaseAPIClient):
    def __init__(self,
                 community_token: str,
                 access_token: str
                 ) -> None:
        super().__init__(community_token)
        self.access_token = access_token

    def get_all(self,
                community_id: str,
                count: int=100,
                filter: Literal["suggests", "postponed", "owner", "others", "all", "donut"]="all"
                ) -> list[dict[str, str]]:      
        params = {
            "domain": f"-{community_id}", 
            "count": count,
            "filter": filter
        }
        return self.get_request("wall.get", params, self.access_token)["items"]

    def get_by_id(self,
                  community_id: str,
                  post_id: str
                  ) -> dict[str, str]:
        params = {
            "posts": f"-{community_id}_{post_id}" 
        }
        return self.get_request("wall.getById", params, self.access_token)["items"][0]

    def get_comments(self,
                     community_id: int,
                     post_id: int, 
                     count: int=100
                     ) -> list[dict[str, str]]:
        params = {
            "owner_id": f"-{community_id}",
            "post_id": post_id,
            "count": count
        }
        return self.get_request("wall.getComments", params, self.access_token)["items"]

    def get_all_since(self,
                      community_id:int,
                      since_timestamp:int
                      ) -> list[dict[str, str]]:
        posts = self.get_all(community_id)
        return [post for post in posts if post["date"]>since_timestamp]

    def delete(self,
               community_id: str,
               post_id: str
               ) -> int:
        params = {
            "owner_id": f"-{community_id}",
            "post_id": post_id
        }
        return self.post_request("wall.delete", params, access_token=self.access_token)