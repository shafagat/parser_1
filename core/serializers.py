class GameSer:
    fiels = ('name', 'price', 'discount', 'discount_price', 'link')

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.clean_data = {}

    def serialize(self):
        for f in GameSer.fiels:
            func = f'self._get_{f}()'
            try:
                self.clean_data[f] = eval(func)
            except AttributeError:
                raise Exception(f'Нет функции с названием {func}')
        return self.clean_data

    def _get_name(self):
        name_element = self.raw_data.find('h3', {"class": 'x1GameName'})
        if not name_element:
            raise Exception(f'Не удалось определить название')
        return name_element.get_text()

    def _get_price(self):
        price_element = self.raw_data.find('span', {"class": 'textpricenew x-hidden-focus'})
        if not price_element:
            raise Exception(f'Не удалось определить цену')
        return price_element.get_text()

    def _get_discount(self):
        discount_element = self.raw_data.find('span', {"class": 'x-screen-reader'})
        if not discount_element:
            return False
        return True

    def _get_discount_price(self):
        discount_element = self.raw_data.find('span', {"class": 'x-screen-reader'})
        if not discount_element:
            return False
        return discount_element.get_text()

    def _get_link(self):
        link_element = self.raw_data.find('a', {"class": 'gameDivLink'})
        if not link_element:
            raise Exception(f'Не удалось определить ссылку')
        return link_element.attrs['href']

class AddOnSer:
    fiels = ('name', 'price',)

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.clean_data = {}

    def serialize(self):
        for f in AddOnSer.fiels:
            func = f'self._get_{f}()'
            try:
                self.clean_data[f] = eval(func)
            except AttributeError:
                raise Exception(f'Нет функции с названием {func}')
        return self.clean_data

    def _get_name(self):
        name_element = self.raw_data.find('span', {"class": 'ProductCard-module__title___3iwfs'})
        if not name_element:
            raise Exception(f'Не удалось определить название')
        return name_element.get_text()

    def _get_price(self):
        name_element = self.raw_data.find('p', {"class": 'ProductCard-module__price___Ocr3o'})
        if not name_element:
            raise Exception(f'Не удалось определить название')
        return name_element.get_text()