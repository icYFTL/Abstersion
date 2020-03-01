class StaticMethods:
    @staticmethod
    def get_percentage(a, b, digits=0):
        try:
            return str(StaticMethods.to_fixed(int(a) / int(b) * 100, digits)) + '%'
        except:
            return '0%'

    @staticmethod
    def to_fixed(numObj, digits=0):
        return f"{numObj:.{digits}f}"
