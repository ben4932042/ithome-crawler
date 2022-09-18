# pylint: disable=too-few-public-methods, unused-argument, super-init-not-called, arguments-differ, arguments-differ, line-too-long
"""ithome crawler"""
from typing import List
import datetime
import scrapy
from web_poet import ItemWebPage, WebPage
from src.items import IthomeContentInfoItem


class HomePage(WebPage):
    """ithome ironman user home page extract logic"""
    @property
    def get_next_page_url(self) -> list:
        """get ironman next page url list"""
        return self.xpath('//ul[@class="pagination"]/li/a/@href').extract()

class ContentPage(ItemWebPage):
    """ithome ironman user content extract logic"""
    @property
    def content_list(self) -> list:
        """get content session object list"""
        return self.xpath('//div[@class="qa-list profile-list ir-profile-list"]')

    def to_item(self) -> List[IthomeContentInfoItem]:
        items_list = []
        for content in self.content_list:
            profile_list = content.xpath('.//div[@class="profile-list__condition"]//span[@class="qa-condition__count"]/text()').extract()
            item = {
                "title": content.xpath('.//a[@class="qa-list__title-link"]/text()').extract_first().strip(),
                "like": profile_list[0],
                "comment":  profile_list[1],
                "view": profile_list[2],
                "url": self.url,
                "create_datetime": datetime.datetime.strptime(
                    content.xpath('.//a[@class="qa-list__info-time"]/@title').extract_first().strip(),
                    '%Y-%m-%d %H:%M:%S'
                    )
            }
            items_list.append(IthomeContentInfoItem(**item))
        return items_list

class IthomeSpider(scrapy.Spider):
    """main function"""
    name = 'ithome'

    def __init__(self, ironman_man_page: str):
        if not ironman_man_page:
            raise scrapy.exceptions.CloseSpider('Lost input url.')
        self.ironman_man_page = ironman_man_page

    def start_requests(self):
        """start request from self.ironman_man_page"""
        yield scrapy.Request(
            url=self.ironman_man_page,
            callback=self.parse
        )

    def parse(self, response, homepage: HomePage, content: ContentPage) -> IthomeContentInfoItem:
        """get page1 item and yield to page 2 and page 3 if exist"""
        page_url_list = homepage.get_next_page_url
        for next_page_url in set(page_url_list):
            yield response.follow(
                url=next_page_url,
                callback=self.parse_content,
            )

        for item in content.to_item():
            yield item

    def parse_content(self, response, content: ContentPage) -> IthomeContentInfoItem:
        """page 2 and page 3 get item process"""
        for item in content.to_item():
            yield item
