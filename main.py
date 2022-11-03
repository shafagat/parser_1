from urllib import request
from bs4 import BeautifulSoup

from core.helpers import get_game_card
from core.models import Game
from core.selenium import SeleniumBrowser
from core.serializers import GameSer
import csv


url_1 = "https://www.xbox.com/ru-ru/games/all-games"

class Main:

    def handle(self):
        sel = SeleniumBrowser(url_1)
        sel.activate()
        sel.open_main_page()
        all_cards = []

        for i in range(1, 25):
            if i > 1:
                pagination_element = sel.get_paginate_number_element(i)
                sel.click_to_button(pagination_element)
            soup = sel.get_page_source()
            games = soup.find('div', {"class": "gameDivsWrapper"})
            cards = list(filter(get_game_card, list(games.findChildren("div" , recursive=False))))
            all_cards.extend(cards)

        games = []
        adons = []
        sel.quit()

        for card in all_cards:
            ser = GameSer(raw_data=card)
            ser.serialize()
            game_obj = Game(**ser.clean_data)

            game_obj.launch_date = game_obj.get_launch_date()

            adons.extend(game_obj.get_add_ons())
            games.append(game_obj.__dict__)

        self.save(games)
        self.save(adons)

    def save(self, data):
        with open('mycsvfile.csv', 'w') as f:

            w = csv.DictWriter(f, data[0].keys)
            w.writeheader()
            w.writerows(data)

main = Main()
main.handle()