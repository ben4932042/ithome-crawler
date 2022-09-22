# pylint: disable=too-few-public-methods, unused-argument, super-init-not-called, arguments-differ, arguments-differ, line-too-long, abstract-method
"""ithome crawler: main function to define crawler process flow"""
import scrapy
from src.handlers import HomePage, UserPage, UserHomePage, ArticlePage, ContentPage
from src.items import IthomeIronManItem, IthomeUserInfoItem


class IthomeSpider(scrapy.Spider):
    """main function"""
    name = 'ithome'
    allowed_domains = ['ithelp.ithome.com.tw']

    def start_requests(self):
        """overwrite start request method"""
        _start_url = 'https://ithelp.ithome.com.tw/2022ironman/signup/list'
        _group = 'devops'
        for url in [f"{_start_url}?group={_group}&page={page+1}" for page in range(3)]:
            yield scrapy.Request(url=url, callback=self.parse_home)

    def parse_home(self, response, homepage: HomePage):
        """get ithome 2022ironman user url
        sample: https://ithelp.ithome.com.tw/2022ironman/signup/list?group=devops&page=1"""
        for user_ironman_page_url in homepage.get_all_user_ironman_url():
            yield response.follow(
                user_ironman_page_url,
                callback=self.parse_user_home,
            )
        for user_url in homepage.get_all_user_url():
            yield response.follow(
                user_url,
                callback=self.parse_user_info,
            )

    def parse_user_info(self, response, content: UserPage) -> IthomeUserInfoItem:
        """sample: https://ithelp.ithome.com.tw/users/20151613"""
        yield content.to_item()

    def parse_user_home(self, response, homepage: UserHomePage):
        """get page1 item and yield to page 2 and page 3 if exist
        example: https://ithelp.ithome.com.tw/users/20151613/ironman/5333"""
        for next_page_url in homepage.get_next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse_article)

    def parse_article(self, response, content: ArticlePage):
        """page 2 and page 3 get article info process
        example: https://ithelp.ithome.com.tw/users/20151613/ironman/5333?page=2"""
        for item in content.to_item():
            yield response.follow(
                url=item.article_url,
                callback=self.parse_content,
                meta = {'article': item}
            )

    def parse_content(self, response, content: ContentPage) -> IthomeIronManItem:
        """get content text process
        example: https://ithelp.ithome.com.tw/articles/10287199"""
        content_obj = content.to_item()
        article_obj = response.meta['article']

        yield IthomeIronManItem(**content_obj.dict(), **article_obj.dict())
