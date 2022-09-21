# pylint: disable=no-member, no-self-argument
"""ithome extract data item"""
import datetime
import pydantic

class ArticleItem(pydantic.BaseModel):
    """ithome aritcle info"""
    user_id: int
    ironman_id: int
    title: str
    like: int = 0
    comment: int = 0
    view: int = 0
    article_id: int
    article_url: pydantic.HttpUrl
    create_datetime: datetime.datetime

class ContentItem(pydantic.BaseModel):
    """ithome content info"""
    text: str

class IthomeIronManItem(ArticleItem,ContentItem):
    """ithome article and content info"""
    source: str = "ithome_iron_man_item"

class IthomeUserInfoItem(pydantic.BaseModel):
    """ithome user info"""
    source: str = "ithome_user_info_item"
    user_id: int
    user_name: str
    ithome_level: str
    ithome_point: int
    user_viewed: int
    user_followed: int
    ask_question: int
    article: int
    answer: int
    invitation_answer: int
    best_answer: int
