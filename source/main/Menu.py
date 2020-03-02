import json
import os
import sys

import hues

from source.console.Methods import Methods
from source.settings.Settings import Settings
from source.static.StaticData import StaticData


class Menu(object):
    @staticmethod
    def init():
        if len(sys.argv) > 1:
            if sys.argv[1] == '--auto':
                Menu.__infinity()
                os._exit(0)

        templ = '''Menu:
1 - Set safe-list of friends (txt/manually)
2 - Set options for news blocking
3 - Start
4 - Work always
5 - Clear ban-list
0 - Exit'''
        while True:
            _input = input(templ + '\n> ')
            while _input not in ['1', '2', '3', '4', '5', '0']:
                _input = input(templ + '\n> ')

            if _input == '1':
                Menu.__set_safe_list()
            elif _input == '2':
                Menu.__set_options()
            elif _input == '3':
                Menu.__start()
            elif _input == '4':
                Menu.__start(False)
            elif _input == '5':
                Menu.__banlist_clear()
            elif _input == '0':
                os._exit(0)

    @staticmethod
    def __set_safe_list() -> None:
        import re
        print('Note: file data formats like:\n123456\n123456\n...')
        _choice = input('Give me path of file or type it manually in format *1234325, 1234314, ...*\n> ')
        _data = None
        while not os.path.exists(_choice) and not re.findall('[0-9]+,?', _choice.replace(' ', '')):
            _choice = input('Give me path of file or type it manually in format *1234325, 1234314, ...*\n> ')

        if os.path.exists(_choice):
            with open(_choice, 'r', encoding='UTF-8') as f:
                _data = f.read().split('\n')
                f.close()
        else:
            _data = _choice.replace(' ', '').split(',')

        _temp = Settings.settings_get()
        _temp['safe_zone'] = _data

        Settings.settings_save(_temp)

        Methods.console_clear()
        hues.success(f'Done!\n{len(_data)} users has been added to safe zone!')

    @staticmethod
    def __set_options() -> None:
        if not os.path.exists('./settings.json'):
            with open('./settings.json', 'w', encoding='UTF-8') as f:
                f.write(json.dumps(StaticData.defaultSettings))
                f.close()
        else:
            StaticData.defaultSettings = json.loads(open('./settings.json', 'r', encoding='UTF-8').read())

        _nf = input('Newsfeed Ban (y/n)\n> ').lower()
        while _nf != 'y' and _nf != 'n':
            _nf = input('Newsfeed Ban (y/n)\n> ').lower()

        _sr = input('Stories Ban (y/n)\n> ').lower()
        while _sr != 'y' and _sr != 'n':
            _sr = input('Stories Ban (y/n)\n> ').lower()

        # _mb = input('Messages sending to you ban (y/n)\n> ').lower()
        # while _mb != 'y' and _nf != 'n':
        #     _mb = input('Messages sending to you ban (y/n)\n> ').lower()

        StaticData.defaultSettings['newsfeedBan'] = True if _nf == 'y' else False
        StaticData.defaultSettings['messagesBan'] = False  # True if _mb == 'y' else False
        StaticData.defaultSettings['storiesBan'] = True if _sr == 'y' else False

        Settings.settings_save(StaticData.defaultSettings)

        Methods.console_clear()
        hues.success('Done!')

    @staticmethod
    def __start(manual=True) -> None:
        from source.main.Main import Main
        if manual:
            Main.routine()
        else:
            Menu.__infinity()

    @staticmethod
    def __infinity():
        from source.main.Main import Main
        from time import sleep
        hues.warn('Endless mode activated')
        while True:
            try:
                Main.routine(False)
                hues.log('Sleep for 600 sec.')
                sleep(600)
            except KeyboardInterrupt:
                Methods.console_clear()
                break

    @staticmethod
    def __banlist_clear() -> None:
        from source.vkApi.VkAPI import VkAPI
        from source.static.StaticMethods import StaticMethods

        vk = VkAPI()

        _ban_list = vk.get_newsfeed_banlist()['members']
        _ban_list = list([str(x) for x in _ban_list])
        __init_count = len(_ban_list)

        hues.warn(f'Banlist will be clear.\nContinue? (y/n)')
        _choice = input('> ').lower()
        while _choice != 'y' and _choice != 'n':
            _choice = input('> ').lower()

        if _choice == 'n':
            Methods.console_clear()
            return

        while len(_ban_list) > 0:
            hues.log(
                f'[Newsfeed] Progress: {StaticMethods.get_percentage(abs(__init_count - len(_ban_list)), __init_count)}')
            vk.unban_newsfeed(_ban_list[:100])
            del (_ban_list[:100])

        _ban_list = vk.get_stories_banlist()['items']
        _ban_list = list([str(x) for x in _ban_list])
        __init_count = len(_ban_list)

        while len(_ban_list) > 0:
            hues.log(
                f'[Stories] Progress: {StaticMethods.get_percentage(abs(__init_count - len(_ban_list)), __init_count)}')
            vk.stories_unban(_ban_list[:100])
            del (_ban_list[:100])

        Methods.console_clear()
        hues.success('Friends unmuted')
