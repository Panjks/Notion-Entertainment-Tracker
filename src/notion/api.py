from notion_client import Client
from utils.log import logger


class NotionApi(object):
    def __init__(self, auth_key: str, database_id: str):
        self.auth_key = auth_key
        self.database_id = database_id
        self.notion_client = Client(auth=self.auth_key)

    @staticmethod
    def page_properties_generate(name: str,
                                 entertainment_type: str,
                                 cover: str = None,
                                 status: str = None,
                                 score: int = None,
                                 date: str = None,
                                 url: str = None,
                                 episodes: int = None,
                                 ):
        """
        generate the page properties.
        :param name:
        :param entertainment_type:
        :param cover:
        :param status:
        :param score:
        :param date: YYYY-MM-DD
        :param url:
        :param episodes:
        :return:
        """
        page_data = {
            "Name": {"title": [{"text": {"content": name}}]},
            "Type": {"select": {"name": entertainment_type}},
        }

        if cover:
            page_data["Cover"] = {"files": [{'name': name + "-cover", 'type': 'external', 'external': {'url': cover}}]}

        if status:
            page_data["Status"] = {"status": {"name": status}}
        else:
            page_data["Status"] = {"status": {"name": "Not started"}}

        if score:
            page_data["Score"] = {"number": score}

        if date:
            page_data["Date"] = {"date": {"start": date}}

        if url:
            page_data["Url"] = {"url": url}

        if episodes:
            page_data["Episodes"] = {"rich_text": [{"type": "text", "text": {"content": str(episodes)}}]}

        logger.info(f"Generate page properties finished. page name: {name}")
        return page_data

    @staticmethod
    def page_icon_generate(entertainment_type: str):
        url = 'https://www.notion.so/icons/movie-clapboard-play_gray.svg'
        if entertainment_type == "Anime":
            url = 'https://www.notion.so/icons/tulip-name-tag_gray.svg'

        elif entertainment_type == 'Movie':
            url = 'https://www.notion.so/icons/movie-clapboard-play_gray.svg'

        elif entertainment_type == 'Game':
            url = 'https://www.notion.so/icons/video-game_gray.svg'

        icon_data = {
            'type': 'external',
            'external': {
                'url': url
            }
        }
        logger.info(f"Generate page icon finished. page type: {entertainment_type}")
        return icon_data

    def create_page(self, name: str,
                    entertainment_type: str,
                    cover: str = None,
                    status: str = None,
                    score: int = None,
                    date: str = None,
                    url: str = None,
                    episodes: int = None):

        properties = self.page_properties_generate(name, entertainment_type, cover, status, score, date, url, episodes)
        icon = self.page_icon_generate(entertainment_type)
        result = self.notion_client.pages.create(parent={"database_id": self.database_id}, properties=properties, icon=icon)
        logger.info(f"Create page success. page link: {result.get(url, '')}")
