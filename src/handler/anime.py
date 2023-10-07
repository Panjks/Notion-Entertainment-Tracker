import requests
from bs4 import BeautifulSoup
from utils.log import logger
from datetime import datetime


class AnimeHandler(object):
    @classmethod
    def _get_bangumi_id(cls, keyword: str):
        url = f'https://bgm.tv/subject_search/{keyword}?cat=2'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        try:
            resp = requests.get(url, headers=headers)
        except Exception as err:
            logger.error(f"Get bangumi id failed. Error detail: {err}")
            return None

        html_content = resp.content.decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        result_list = soup.find_all('h3')
        link_element = result_list[0].find('a', class_='l')
        if link_element:
            link = link_element['href']
            return 'https://bgm.tv' + link

    @classmethod
    def _get_bangumi_info(cls, bangumi_link: str):
        url = bangumi_link
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        try:
            resp = requests.get(url, headers=headers)
        except Exception as err:
            logger.error(f"Get bangumi info failed. Error detail: {err}")
            return None

        ret = {}
        html_content = resp.content.decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get anime name.
        name_span = soup.find('span', class_='tip', string='中文名: ')
        if name_span:
            name = str(name_span.next_sibling).strip()
            ret['name'] = name

        # Get anime start date.
        date_span = soup.find('span', class_='tip', string='放送开始: ')
        if date_span:
            date = str(date_span.next_sibling).strip()
            date = cls.__date_format(date)
            ret['date'] = date

        # Get anime episode.
        episodes_span = soup.find('span', class_='tip', string='话数: ')
        if episodes_span:
            episodes = str(episodes_span.next_sibling).strip()
            try:
                ret['episodes'] = int(episodes)
            except Exception as err:
                logger.error("Get episodes err. Details: {}".format(err))
                ret['episodes'] = -1

        # Get anime cover.
        cover_tag = soup.find('img', class_='cover')
        if cover_tag:
            cover_url = cover_tag['src']
            ret["cover"] = 'http:' + str(cover_url)

        # Get anime score.
        rating_span = soup.find('span', property='v:average')
        if rating_span:
            rating = float(rating_span.text)
            ret["score"] = rating

        ret['url'] = bangumi_link

        return ret

    @classmethod
    def get_bangumi_details(cls, keyword: str) -> dict:
        bangumi_url = cls._get_bangumi_id(keyword)
        logger.info(f"Get bangumi url success. Url: {bangumi_url}")
        if bangumi_url:
            ret = cls._get_bangumi_info(bangumi_url)
            logger.info(f"Get bangumi details success. data: {ret}")
            return ret

    @classmethod
    def __date_format(cls, date_string):
        date_obj = datetime.strptime(date_string, "%Y年%m月%d日")
        return date_obj.strftime("%Y-%m-%d")
