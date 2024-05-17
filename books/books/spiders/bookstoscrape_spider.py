import scrapy


class BookstoscrapeSpider(scrapy.Spider):
    name = "bookstoscrape"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

        # Each 'article' element in the Page represents a book
        for article in response.xpath("//article"):
            book = {}

            # Title
            book_title = article.xpath(".//h3/a/@title").get()
            book["BookTitle"] = book_title

            # Price
            book_price = article.xpath(".//div/p/text()").get()
            book["BookPrice"] = book_price

            # Book Image Url
            image_href = article.xpath(".//div/a/img/@src").get()
            book["BookImageUrl"] = response.urljoin(image_href)

            # Book Details Page Url
            book_details_href = article.xpath(".//div/a/@href").get()
            book["BookDetailsPageUrl"] = response.urljoin(book_details_href)

            yield book

        next_page_selector = response.css(".next")
        if next_page_selector:
            href_content = next_page_selector.xpath(".//a/@href").get()
            next_page_url = response.urljoin(href_content)
            yield scrapy.Request(next_page_url, callback=self.parse)
