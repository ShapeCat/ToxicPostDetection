import time, requests
from typing import Generator
from .base_client import BaseAPIClient



class LongPollClient(BaseAPIClient):
    def _get_longpoll_server(self, community_id: str) -> tuple[str, str, str]:
        """
        Get the LongPoll server for a community.

        Args:
            community_id (int): The ID of the community.

        Returns:
            tuple[str, str, str]: A tuple of the LongPoll server key, URL and timestamp.
        """
        response = self.get_request("groups.getLongPollServer", {"group_id": community_id})
        return response["key"], response["server"], response["ts"]

    def listen(self, community_id: str, warmup: bool = True) -> Generator[list, None, None]:
        """
        Listen to the LongPoll server for a community.

        Args:
            community_id (str): The ID of the community.
            warmup (bool, optional): Whether to perform a warmup request. Defaults to True.

        Yields:
            Generator[list, None, None]: A generator of updates. Each update is a list of at least two elements: the update type and the update data.
        """
        key, server, ts = self._get_longpoll_server(community_id)
        if warmup:
            try:
                warmup_params = {
                    'act': 'a_check',
                    'key': key,
                    'ts': ts,
                    'wait': 0
                }
                response = requests.get(server, params=warmup_params, timeout=5)
                response.raise_for_status()
                data = response.json()
                ts = data['ts']
            except Exception as e:
                print(f"[Warmup] Ошибка: {e}")

        while True:
            try:
                longpoll_params = {
                    'act': 'a_check',
                    'key': key,
                    'ts': ts,
                    'wait': 25
                }
                response = requests.get(server, params=longpoll_params, timeout=30)
                response.raise_for_status()
                data = response.json()
            except (requests.exceptions.Timeout):
                time.sleep(5)
                continue

            if 'failed' in data:
                if data['failed'] == 1:
                    ts = data['ts'] 
                else:
                    key, server, ts = self._get_longpoll_server(community_id)
                continue

            ts = data['ts']            
            for update in data.get('updates', []):
                yield update
