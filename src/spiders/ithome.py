# pylint: disable=too-few-public-methods, unused-argument, super-init-not-called, arguments-differ, arguments-differ, line-too-long
"""ithome crawler"""
from typing import List
import datetime
import scrapy
import parse
from web_poet import ItemWebPage, WebPage
from src.items import ArticleItem
from src.items import ContentItem
from src.items import IthomeIronManItem


class HomePage(WebPage):
    def get_all_user_ironman_url(self) -> list:
        """get each user ironman page url from 2022ironman page"""
        return self.xpath('//div[@class="list-card"]//div[@class="col-md-10"]//a[@class="contestants-list__title title"]/@href').extract()

class UserHomePage(WebPage):
    """ithome ironman user home page extract logic"""
    @property
    def get_next_page_url(self) -> list:
        """get ironman next page url list"""
        return self.xpath('//ul[@class="pagination"]/li/a/@href').extract()

class ArticlePage(ItemWebPage):
    """ithome ironman user article extract logic"""
    @property
    def content_list(self) -> list:
        """get article session object list"""
        return self.xpath('//div[@class="qa-list profile-list ir-profile-list"]')

    def to_item(self) -> List[ArticleItem]:
        items_list = []
        for content in self.content_list:
            profile_list = content.xpath('.//div[@class="profile-list__condition"]//span[@class="qa-condition__count"]/text()').extract()
            aritle_url = content.xpath('.//h3[@class="qa-list__title"]/a/@href').extract_first().strip()
            user_info  = parse.parse("https://ithelp.ithome.com.tw/users/{user_id}/ironman/{ironman_id}", self.url.split('?', maxsplit=1)[0])
            content_info = parse.parse("https://ithelp.ithome.com.tw/articles/{article_id}", aritle_url)
            item = {
                "user_id": user_info['user_id'],
                "ironman_id": user_info['ironman_id'],
                "title": content.xpath('.//a[@class="qa-list__title-link"]/text()').extract_first().strip(),
                "like": profile_list[0],
                "comment":  profile_list[1],
                "view": profile_list[2],
                "article_id": content_info['article_id'],
                "article_url": aritle_url,
                "create_datetime": datetime.datetime.strptime(
                    content.xpath('.//a[@class="qa-list__info-time"]/@title').extract_first().strip(),
                    '%Y-%m-%d %H:%M:%S'
                    )
            }
            items_list.append(ArticleItem(**item))
        return items_list

class ContentPage(ItemWebPage):
    """ithome ironman user content extract logic"""

    def to_item(self) -> ContentItem:
        content_session = self.xpath('.//div[@class="qa-markdown"]')
        return ContentItem(text = ''.join(content_session.xpath(
            './/h3/text()| .//p/text() | .//li/text()'
        ).extract()).strip())

class IthomeSpider(scrapy.Spider):
    """main function"""
    name = 'ithome'
    allowed_domains = ['ithelp.ithome.com.tw']
    start_urls = [
        'https://ithelp.ithome.com.tw/2022ironman/signup/list?group=devops&page=1',
        #'https://ithelp.ithome.com.tw/2022ironman/signup/list?group=devops&page=2',
        #'https://ithelp.ithome.com.tw/2022ironman/signup/list?group=devops&page=3',
    ]

    def parse(self, response, homepage: HomePage):
        for user_ironman_page_url in homepage.get_all_user_ironman_url():
            yield response.follow(
                user_ironman_page_url,
                callback=self.parse_title,
            )

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
      
