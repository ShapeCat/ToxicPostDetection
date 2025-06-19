from .base_client import BaseAPIClient


class UserClient(BaseAPIClient):
    def get_info(self,
                 user_id: str,
                 fields: list[str] = []
                 ) -> dict[str, str]:
        params = {
            "user_ids": user_id,
            "fields": ','.join(fields)
            } 
        return self.get_request("users.get", params)[0]

    def get_name(self, user_id: str) -> str:
        user_data = self.get_info(user_id, ['first_name', 'last_name']) 
        return f"{user_data['first_name']} {user_data['last_name']}"

    def get_screen_name(self, user_id: str) -> str:
        return self.get_info(user_id, ["domain"])["domain"]
    
    def get_link(self, user_id: str) -> str:
        screen_name = self.get_screen_name(user_id)
        return f"https://vk.com/{screen_name}"
