import requests
from bs4 import BeautifulSoup
from utils.log import logger
from datetime import datetime
import re


class GameHandler(object):
    @classmethod
    def _get_game_info(cls, keyword: str):
        url = f"https://zh.wikipedia.org/wiki/{keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        try:
            resp = requests.get(url, headers=headers)
        except Exception as err:
            logger.error(f"Get game info failed. Error detail: {err}")
            return None

        ret = {}
        html_content = resp.content.decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get game name.
        name = soup.find('h1').text
        ret['name'] = name

        # Get game release date.
        release_info = soup.find('th', text='发行日').find_next_sibling('td')
        release_date = release_info.find('div', class_='plainlist').find('li').text.replace('全球：', '').strip()

        if release_date:
            ret['date'] = cls.__date_format(release_date)

        # Get game episode.
        ret['episodes'] = 1

        # Get game cover.
        file_description = soup.find('a', class_='mw-file-description')
        cover_img = file_description.find('img', class_='mw-file-element')['src']

        if cover_img:
            ret["cover"] = 'https:' + str(cover_img)

        # Get game score.
        metacritic_row = soup.find('td', text='Metacritic')
        metacritic_score = metacritic_row.find_next_sibling('td').text
        score = int(re.search(r'\d+', metacritic_score).group()) / 10
        ret["score"] = score

        ret['url'] = resp.url

        return ret

    @classmethod
    def get_game_details(cls, keyword: str) -> dict:
        ret = cls._get_game_info(keyword)
        logger.info(f"Get game details success. data: {ret}")
        return ret

    @classmethod
    def __date_format(cls, date_string):
        date_obj = datetime.strptime(date_string, "%Y年%m月%d日")
        return date_obj.strftime("%Y-%m-%d")

