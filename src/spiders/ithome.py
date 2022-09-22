# pylint: disable=too-few-public-methods, unused-argument, super-init-not-called, arguments-differ, arguments-differ, line-too-long, abstract-method
"""ithome crawler"""
import scrapy
from src.handlers import HomePage, UserPage, UserHomePage, ArticlePage, ContentPage
from src.items import ArticleItem, IthomeIronManItem


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
        for user_ironman_page_url in homepage.get_all_user_ironman_url():
            yield response.follow(
                user_ironman_page_url,
                callback=self.parse_title,
            )
        for user_url in homepage.get_all_user_url():
            yield response.follow(
                user_url,
                callback=self.parse_user_info,
            )

    def parse_user_info(self, response, content: UserPage):
        yield content.to_item()

    def parse_title(self, response, homepage: UserHomePage, content: ArticlePage) -> ArticleItem:
        """get page1 item and yield to page 2 and page 3 if exist"""
        page_url_list = homepage.get_next_page_url
        for next_page_url in set(page_url_list):
            yield response.follow(
                url=next_page_url,
                callback=self.parse_article,
            )

        for item in content.to_item():
            yield response.follow(
                url=item.article_url,
                callback=self.parse_content,
                meta = {'article': item}
            )

    def parse_article(self, response, content: ArticlePage) -> ArticleItem:
        """page 2 and page 3 get item process"""
        for item in content.to_item():
            yield item

    def parse_content(self, response, content: ContentPage) -> IthomeIronManItem:
        """page 2 and page 3 get item process"""
        content_obj = content.to_item()
        article_obj = response.meta['article']

        yield IthomeIronManItem(**content_obj.dict(), **article_obj.dict())
