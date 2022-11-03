import re

from core.helpers import page_soup
from core.serializers import AddOnSer
from selenium.common.exceptions import TimeoutException

class BaseContentModel:
    def _fiels(self, fields):
        for key, value in fields.items():
            self.__setattr__(key, value)

class AddOn(BaseContentModel):
    def __init__(self, **kwargs):
        self._fiels(kwargs)

class Game(BaseContentModel):
    def __init__(self, **kwargs):
        self._fiels(kwargs)

    def _get_ld_exclusive(self):
        elems = page_soup.get_by_tag_and_class(self.link, 'm-additional-information', 'section')[0]
        launch_date_element = elems.find('li', text=re.compile('г.'))
        if launch_date_element:
            return launch_date_element.get_text()
        else:
            return None

    def get_launch_date(self):
        launch_date = None
        try:
            elems = page_soup.get_by_tag_and_class(self.link, 'ModuleColumn-module__col___WMOVN', 'div')
        except TimeoutException:
            launch_date = self._get_ld_exclusive()
            return launch_date
        launch_date_element = None

        for elem in elems:
            e = elem.find('h3',
                          {"class": 'typography-module__xdsBody1___2-8Fc'})
            if e:
                if e.get_text() == 'Дата выпуска':
                    launch_date_element = elem
        if launch_date_element:
            launch_date = page_soup.get_childs(element=launch_date_element, tag='div')[-1].get_text()
        return launch_date

    def get_add_ons(self, ):
        addons = []
        elems = page_soup.get_by_tag_and_class(self.link, 'ModuleColumn-module__col12___25_gD', 'div')
        add_on_elem = None
        for elem in elems:
            e = elem.find('h2', {"class": 'commonStyles-module__channelTitleText___3A5kE typography-module__xdsH6___RhUR_'})
            if e:
                if e.get_text() == 'Дополнения для этой игры':
                    add_on_elem = elem
        if add_on_elem:
            addons_elements = page_soup.get_childs(element=add_on_elem, tag='li')[:-1]
            for a in addons_elements:
                ser = AddOnSer(raw_data=a)
                data = ser.serialize()
                data['game'] = self.name
                addons.append(data)
        return addons





