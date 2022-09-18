# pylint: disable=no-member
"""ithome extract data item"""
import datetime
import pydantic


class IthomeContentInfoItem(pydantic.BaseModel):
    """ithome content data"""
    title: str
    like: int = 0
    comment: int = 0
    view: int = 0
    url: pydantic.HttpUrl
    create_datetime: datetime.datetime
