# -*- coding: utf-8 -*-
from urllib import parse  # python3

from scrapy.http import Request

from ArticleSpider.items import *
from ArticleSpider.utils.commom import *


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 1.获取文章列表页中的文章url交给scrapy下载后进行解析
        # 2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse

        # 解析列表页中的所有文章交给scrapy下载后进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")

        for post_node in post_nodes:
            img_url = post_node.xpath('img/@src').extract_first("")
            post_url = post_node.xpath('@href').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": img_url},
                          callback=self.parse_detail)

        # 提取下一页并交给scrapy下载
        next_urls = response.xpath(
            '//a[@class="next page-numbers"]/@href').extract()[0]
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)




    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        # front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        # # 提取文章的具体字段
        # title = response.xpath(
        #     '//div[@class="entry-header"]/h1/text()').extract()[0]
        # create_date = response.xpath(
        #     '//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace("·", "").strip()
        # vote = response.xpath(
        #     '//span[contains(@class,"vote-post-up")]/text()').extract()[0]
        # comment_nums = response.xpath(
        #     '//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').extract()[0]
        # tags = response.xpath(
        #     '//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # content = response.xpath('//div[@class="entry"]').extract()[0]
        #
        # match_re = re.match('.*(\d+).*', comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["url"] = response.url
        # article_item["vote"] = vote
        # article_item["front_image_url"] = [front_image_url]
        # article_item["comment_nums"] = comment_nums
        # article_item["content"] = content
        # article_item["tags"] = tags

        # 通过item loader加载item
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()

        yield article_item