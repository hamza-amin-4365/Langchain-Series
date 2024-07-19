from icrawler.builtin import GoogleImageCrawler,BaiduImageCrawler,BingImageCrawler
import time
import random

def DownloadImages(keyword, max_num=10):
    google_crawler = BingImageCrawler(
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=1,
        storage={'root_dir': f'./images/{keyword}'})
    
    try:
        google_crawler.crawl(
            keyword=keyword, 
            max_num=max_num,
            min_size=(200,200),
            max_size=None,
            file_idx_offset=0
        )
        time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
    except Exception as e:
        print(f"An error occurred while crawling for '{keyword}': {str(e)}")

# Usage
input_keyword = input("Enter the keyword: ")
DownloadImages(input_keyword, max_num=10)

