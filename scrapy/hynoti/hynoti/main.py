from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

    
def m():
    process = CrawlerProcess(get_project_settings())
    process.crawl('cse', domain='cs.hanyang.ac.kr')
    process.crawl('bs', domain='biz.hanyang.ac.kr')
    process.start() # the script will block here until the crawling is finished
    
def crawl():
    p = Process(target=m)
    p.start()
    p.join()
    print('crawl fin.')

def start_scheduler():
    scheduler = BlockingScheduler()
    t = CronTrigger(day_of_week='mon-fri', hour='12, 17', timezone='Asia/Seoul')
    scheduler.add_job(crawl, trigger=t)

    print('scheduler running,,')
    scheduler.start()

if __name__ == '__main__':
    start_scheduler()