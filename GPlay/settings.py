BOT_NAME = 'GPlay'

SPIDER_MODULES = ['GPlay.spiders']
NEWSPIDER_MODULE = 'GPlay.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'GPlay.pipelines.SqlitePipeline': 300,
}

FEED_EXPORT_ENCODING = 'utf-8'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'