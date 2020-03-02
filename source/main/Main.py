import json
import os

import hues

from source.console.Methods import Methods
from source.settings.Settings import Settings
from source.vkApi import VkAPI


class Main:
    @staticmethod
    def routine(manual=True) -> None:
        Methods.console_clear()
        vk = VkAPI()
        _settings = None
        if os.path.exists('./settings.json'):
            with open('./settings.json') as f:
                try:
                    _settings = json.loads(f.read())
                except Exception:
                    hues.error('Bad settings')
                    os.remove('./settings.json')
                    os._exit(-1)
                hues.success('Settings loaded.')

        _settings = Settings.settings_get()
        if manual:
            if not _settings.get('safe_zone'):
                hues.warn('No users in safe zone.\nContinue? (y/n)')
                _choice = input('> ').lower()
                while _choice != 'y' and _choice != 'n':
                    hues.warn('No users in safe zone.\nContinue? (y/n)')
                    _choice = input('> ').lower()
                if _choice == 'n':
                    Methods.console_clear()
                    return

        _ban_list = []
        from copy import copy
        from source.static.StaticMethods import StaticMethods

        _friends = vk.friends_get()
        _friends['items'] += vk.get_out_requests()['items']
        for _friend in _friends['items']:
            if str(_friend) not in _settings['safe_zone']:
                _ban_list.append(_friend)
        _ban_list = list([str(x) for x in _ban_list])

        if _settings['newsfeedBan']:
            if manual:
                hues.warn(f'{len(_ban_list)} your friends (and out requests) will be affected.\nContinue? (y/n)')
                _choice = input('> ').lower()
                while _choice != 'y' and _choice != 'n':
                    _choice = input('> ').lower()

                if _choice == 'n':
                    Methods.console_clear()
                    return

            __init_count = len(_ban_list)

            _temp = copy(_ban_list)

            while len(_temp) > 0:
                if manual:
                    hues.log(
                        f'[Newsfeed] Progress: {StaticMethods.get_percentage(abs(__init_count - len(_temp)), __init_count)}')
                vk.add_newsfeed_ban(_temp[:100])
                del (_temp[:100])

        if _settings['messagesBan']:
            pass

        if _settings['storiesBan']:
            _temp = copy(_ban_list)
            __init_count = len(_temp)

            while len(_temp) > 0:
                if manual:
                    hues.log(
                        f'[Stories] Progress: {StaticMethods.get_percentage(abs(__init_count - len(_temp)), __init_count)}')
                vk.stories_ban(_temp[:100])
                del (_temp[:100])

        if manual:
            Methods.console_clear()
        hues.success('Work done!')
