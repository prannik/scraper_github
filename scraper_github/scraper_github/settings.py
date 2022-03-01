import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


BOT_NAME = 'scraper_github'
SPIDER_MODULES = ['scraper_github.spiders']
NEWSPIDER_MODULE = 'scraper_github.spiders'

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    "scraper_github.pipelines.ScraperGithubPipeline": 300,
}

DATABASE = {
    "drivername": "postgresql",
    "host": env('DATABASE_HOST'),
    "port": env('DATABASE_PORT'),
    "username": env('DATABASE_USER'),
    "password": env('DATABASE_PASSWORD'),
    "database": env('DATABASE_NAME'),
}

LOG_LEVEL = "INFO"
