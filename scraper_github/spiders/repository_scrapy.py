import scrapy

from scraper_github.items import ScraperGithubItem


class GitHubSpider(scrapy.Spider):
    name = 'parsing'
    allowed_domains = ['github.com']

    def __init__(self, path='', **kwargs):
        links = []
        with open(path) as file:
            for line in file:
                links.append(line)
        self.start_urls = links
        super().__init__(**kwargs)

    def parse(self, response, **kwargs):
        rep_link = response.css('a.UnderlineNav-item ::attr(href)')[1].get()
        if 'orgs' in rep_link.split('/'):
            yield response.follow(rep_link, callback=self.parse_org)
        else:
            yield response.follow(rep_link, callback=self.parse_person)

    def parse_person(self, response):
        repositories = response.css('h3.wb-break-all a::attr(href)').getall()
        for link in repositories:
            yield response.follow(link, callback=self.parse_repository)
        link = response.css('div.BtnGroup a::attr(href)').getall()
        link_text = response.css('div.BtnGroup a::text').getall()
        if len(link) > 0:
            if link_text[-1] == 'Next':
                yield response.follow(link[-1], callback=self.parse_person)

    def parse_org(self, response):
        repositories = response.css('h3.wb-break-all a::attr(href)').getall()
        for link in repositories:
            yield response.follow(link, callback=self.parse_repository)

        link = response.css('a.next_page ::attr(href)').get()
        link_text = response.css('a.next_page ::text').get()

        if link_text == 'Next':
            yield response.follow(link, callback=self.parse_org)

    def parse_repository(self, response):
        context = ScraperGithubItem()

        author = response.url.split('/')[-2]
        title = response.url.split('/')[-1]
        about = response.css('div.BorderGrid-cell p::text').get()
        if about is not None:
            about = about.strip()
        else:
            about = 'No description, website, or topics provided.'

        stars = response.css('span.Counter.js-social-count ::attr(title)').get()
        stars = int(stars.replace(',', '')) if ',' in stars else int(stars)
        forks = response.css('span.Counter ::attr(title)').get()
        forks = int(forks.replace(',', '')) if ',' in forks else int(forks)
        watching = response.css('div.mt-2 strong::text')[1].get()
        watching = watching.replace('.', '') * 1000 if '.' in watching else watching
        watching = int(watching.replace('k', '')) * 1000 if 'k' in watching else int(watching)
        commits = response.css('span.d-none.d-sm-inline strong::text').get()
        commits = int(commits.replace(',', '')) if ',' in commits else int(commits)

        last_commit = response.css("div.css-truncate.css-truncate-overflow.color-fg-muted a::text").getall()
        if len(last_commit) == 0:
            last_commit = {}
        else:
            last_commit = {
                'author': last_commit[0],
                'name': ''.join(last_commit[1:]),
                'date': response.css
                ("a.Link--secondary.ml-2 ::attr(datetime)").get().replace("T", " ").replace("Z", " ").strip()
            }

        last_releases = response.css('span.css-truncate.css-truncate-target.text-bold.mr-2 ::text').getall()
        if len(last_releases) == 0:
            releases = 0
            last_releases = {}
        else:
            releases = response.css('h2.h4.mb-3 span::text').get()
            commits = int(releases.replace(',', '')) if ',' in releases else int(releases)
            last_releases = {
                'name': last_releases[0],
                'date_releases':
                    response.css
                    ('div.text-small.color-fg-muted ::attr(datetime)').get().replace('T', ' ').replace('Z', ' ').strip()
            }

        context['author'] = author
        context['title'] = title
        context['about'] = about
        context['url'] = response.url
        context['stars'] = stars
        context['forks'] = forks
        context['watching'] = watching
        context['commits'] = commits
        context['last_commits'] = last_commit
        context['releases'] = releases
        context['last_releases'] = last_releases

        yield context
