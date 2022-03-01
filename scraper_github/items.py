from scrapy import Field, Item


class ScraperGithubItem(Item):
    author = Field()
    title = Field()
    about = Field()
    url = Field()
    stars = Field(serialiser=int)
    forks = Field(serialiser=int)
    watching = Field(serialiser=int)
    commits = Field(serialiser=int)
    last_commits = Field(serialiser=dict)
    releases = Field(serialiser=int)
    last_releases = Field(serialiser=dict)
