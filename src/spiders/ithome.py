# pylint: disable=too-few-public-methods, unused-argument, super-init-not-called, arguments-differ, arguments-differ, line-too-long, abstract-method
"""ithome crawler"""
from typing import List
import datetime
import scrapy
import parse
from web_poet import ItemWebPage, WebPage
from src.items import ArticleItem
from src.items import ContentItem
from src.items import IthomeIronManItem
from src.items import IthomeUserInfoItem


class HomePage(WebPage):
    def get_all_user_ironman_url(self) -> list:
        """get each user ironman page url from 2022ironman page"""
        return self.xpath('//div[@class="list-card"]//div[@class="col-md-10"]//a[@class="contestants-list__title title"]/@href').extract()

    def get_all_user_url(self) -> list:
        return [url.split('/ironman', maxsplit=1)[0] for url in self.get_all_user_ironman_url()]

class UserPage(WebPage):
    def to_item(self) -> IthomeUserInfoItem:
        """get ithome user info"""
        profile_list = self.xpath('.//ul[@class="list-inline profile-nav__list"]/li/a/span/text()').extract()
        return IthomeUserInfoItem(
            user_id = parse.parse("https://ithelp.ithome.com.tw/users/{user_id}", self.url)['user_id'],
            user_name = self.xpath('.//div[@class="profile-header__name"]/text()').extract_first().strip(),
            ithome_level = self.xpath('.//div[@class="profile-header__text"]/text()').extract_first().strip().split(" ‧ ", maxsplit=1)[0],
            ithome_point = self.xpath('.//div[@class="profile-header__text"]/a/text()').extract_first().strip(),
            user_viewed = self.xpath('//span[@class="profile-header__view-num"]/text()').extract_first(),
            user_followed = self.xpath('//span[@class="profile-header__follow-num"]/text()').extract_first(),
            ask_question = profile_list[0],
            article = profile_list[1],
            answer = profile_list[2],
            invitation_answer = profile_list[3],
            best_answer = profile_list[4],
        )

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

    def start_requests(self):
        """overwrite start request method"""
        _start_url = 'https://ithelp.ithome.com.tw/2022ironman/signup/list'
        _group = 'devops'
        for url in [f"{_start_url}?group={_group}&page={page+1}" for page in range(3)]:
            yield scrapy.Request(url=url, callback=self.parse_home)

    def parse_home(self, response, homepage: HomePage):
        # for user_ironman_page_url in homepage.get_all_user_ironman_url():
        #     yield response.follow(
        #         user_ironman_page_url,
        #         callback=self.parse_title,
        #     )
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
