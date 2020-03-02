import vk_api

from Config import Config


class VkAPI:
    def __init__(self):
        if not Config.vk_access_token:
            _token = input('Give me your access token\n> ')
            while len(_token) != 85:
                _token = input('Give me your access token\n> ')

            Config.vk_access_token = _token

        self.vk = vk_api.VkApi(token=Config.vk_access_token)

    def add_newsfeed_ban(self, user_ids: list) -> None:
        self.vk.method('newsfeed.addBan', {'user_ids': ','.join(user_ids)})

    def friends_get(self) -> dict:
        return self.vk.method('friends.get', {'count': 10000})

    def get_newsfeed_banlist(self) -> dict:
        return self.vk.method('newsfeed.getBanned')

    def unban_newsfeed(self, user_ids: list) -> None:
        self.vk.method('newsfeed.deleteBan', {'user_ids': ','.join(user_ids)})

    def stories_ban(self, user_ids: list) -> None:
        self.vk.method('stories.banOwner', {'owners_ids': ','.join(user_ids)})

    def get_stories_banlist(self) -> dict:
        return self.vk.method('stories.getBanned')

    def stories_unban(self, user_ids: list) -> None:
        self.vk.method('stories.unbanOwner', {'owners_ids': ','.join(user_ids)})

    def get_out_requests(self) -> dict:
        return self.vk.method('friends.getRequests', {'count': 1000, 'out': 1})
