from fastapi import APIRouter, Depends
from pydantic import BaseModel
from notion.api import NotionApi
from handler.anime import AnimeHandler
from handler.game import GameHandler
from conf import NOTION_ACCESS_KEY, NOTION_DATABASE_ID
from router import auth
from utils.log import logger


class ItemInfo(BaseModel):
    type: str
    keyword: str


class ResponseModel(BaseModel):
    code: int
    data: str


router = APIRouter()
notion_api = NotionApi(NOTION_ACCESS_KEY, NOTION_DATABASE_ID)


@router.post("/create_item", response_model=ResponseModel)
async def create_item(data: ItemInfo, current_user: auth.User = Depends(auth.get_current_active_user)):
    if data.type == 'Anime':
        anime_data = AnimeHandler.get_bangumi_details(data.keyword)
        notion_api.create_page(entertainment_type='Anime', **anime_data)
        logger.info(f"{current_user.username} has create an Anime item. keyword: {data.keyword}")
        return {"code": 0, "data": "success."}

    elif data.type == 'Game':
        game_data = GameHandler.get_game_details(data.keyword)
        notion_api.create_page(entertainment_type='Game', **game_data)
        logger.info(f"{current_user.username} has create an Game item. keyword: {data.keyword}")
        return {"code": 0, "data": "success."}

