"""ithome crawler: main class to handler crawler where can the process get right info on html
reference: https://github.com/scrapinghub/web-poet"""
from typing import List
import datetime
import parse
from web_poet import ItemWebPage, WebPage
from src.items import ArticleItem
from src.items import ContentItem
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
    def get_next_page_url(self) -> set:
        """get ironman next page url list"""
        url_list = self.xpath('//ul[@class="pagination"]/li/a/@href').extract()
        if not url_list:
            url_list = [f"{self.url}?page=1"]
        return set(url_list)

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
