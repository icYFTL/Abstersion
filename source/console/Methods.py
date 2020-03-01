class Methods:

    @staticmethod
    def console_clear() -> None:
        import sys
        import os
        os.system('cls') if sys.platform == 'win32' else os.system('clear')
