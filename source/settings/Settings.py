import json


class Settings:
    @staticmethod
    def settings_save(settings: dict) -> None:
        with open('./settings.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(settings))
            f.close()

    @staticmethod
    def settings_get() -> dict:
        from os import path
        if path.exists('./settings.json'):
            with open('./settings.json', 'r', encoding='UTF-8') as f:
                return json.loads(f.read())
        return {}
