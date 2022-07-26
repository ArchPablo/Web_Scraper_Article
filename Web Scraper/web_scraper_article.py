import requests
import string
from bs4 import BeautifulSoup
import os

URL = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'


class Scraper:
    files = []

    def __init__(self, url, category="News", page=1):
        self.url = url
        self.category = category
        self.status_url = 0
        self.page = page
        self.links = []
        self.page_content = []
        self.names = []
        self.format_names = []

    def parser(self):
        for p in range(1, self.page + 1):
            self.links = []
            self.page_content = []
            self.names = []
            self.format_names = []
            os.chdir(r'C:\Users\doria\PycharmProjects\Web Scraper\Web Scraper\task')
            os.mkdir(f'Page_{p}')
            os.chdir(rf'C:\Users\doria\PycharmProjects\Web Scraper\Web Scraper\task\Page_{p}')
            print('The current working directory is', os.getcwd())
            url_page = self.url + f'&page={p}'
            soup = self.requests(url_page)
            if self.status_url == 1:
                self.get_link(soup)
                self.get_text()
                self.format_name()
                self.create_txt()

    def requests(self, link):
        r = requests.get(link)
        self.check_status(r.status_code)
        if self.status_url == 1:
            soup = BeautifulSoup(r.content, "html.parser")
            return soup

    def check_status(self, status):
        if status == 200:
            page_content = requests.get(URL).content
            file = open('source.html', 'wb')
            file.write(page_content)
            file.close()
            self.status_url = 1
        else:
            self.status_url = 0
            print(f'The URL returned {status}')

    def get_name(self, link):
        soup = self.requests(link)
        name_article = soup.find('h1', class_="c-article-magazine-title").text
        self.names.append(name_article)

    def get_link(self, soup):
        news_article_links = soup.find_all('span', {'class': 'c-meta__type'}, text=self.category)
        for news_article in news_article_links:
            anchor = news_article.find_parent('article').find('a', {'data-track-action': 'view article'})
            link = 'https://www.nature.com' + anchor.get('href')
            self.links.append(link)
            self.get_name(link)

    def get_text(self):
        for link in self.links:
            soup = self.requests(link)
            print(link)
            try:
                content = soup.find('div', class_="c-article-body u-clearfix").text
                byte_content = bytes(content, encoding='utf-8')
                self.page_content.append(byte_content)
            except AttributeError:
                self.page_content.append(b'The article is available only by paid subscription.')

    def format_name(self):
        for name in self.names:
            name = ''.join(let for let in name if let not in string.punctuation)
            format_name = name.replace(' ', '_')
            self.format_names.append(format_name)

    def create_txt(self):
        for index in range(0, len(self.links)):
            name_file = self.format_names[index]
            file = open(f'{name_file}.txt', 'wb')
            file.write(self.page_content[index])
            file.close()
            self.files.append(file)
        print(f'Saved articles:  {self.files}')


if __name__ == '__main__':
    num_page = int(input("enter number of pages:"))
    category_article = input('enter category')
    scraper_news = Scraper(URL, category=category_article, page=num_page)
    scraper_news.parser()
