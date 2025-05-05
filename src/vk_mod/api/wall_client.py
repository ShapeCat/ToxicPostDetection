from .base_client import BaseAPIClient


class WallAPIClient(BaseAPIClient):
    def get_wall_posts(self, community_id:int|str, count=100) -> list[dict[str, str]]:
        params = {
            "domain": f"-{community_id}", 
            "count": count,
        }
        return self.get_request("wall.get", params)["items"]

    def get_post_by_id(self, post_id:int|str, community_id:int|str) -> dict[str, str]:
        params = {
            "posts": f"-{community_id}_{post_id}" 
        }
        return self.get_request("wall.getById", params)["items"][0]

    def get_post_comments(self, post_id:int, community_id:int, count:int=100) -> list[dict[str, str]]:
        params = {
            "owner_id": f"-{community_id}",
            "post_id": post_id,
            "count": count
        }
        return self.get_request("wall.getComments", params)["items"]

    def get_new_posts_since(self, community_id:int, since_timestamp:int) -> list[dict[str, str]]:
        posts = self.get_wall_posts(community_id)
        return [post for post in posts if post["date"]>since_timestamp]
