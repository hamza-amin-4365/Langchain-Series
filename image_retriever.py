from icrawler.builtin import GoogleImageCrawler

def download_images(keyword, max_num=10):
    google_crawler = GoogleImageCrawler(storage={'root_dir': f'./images/{keyword}'})
    google_crawler.crawl(keyword=keyword, max_num=max_num)

# Usage
input_keyword = input("Enter the keyword: ")
res = input_keyword
download_images(res, max_num=5)

# from icrawler.builtin import GoogleImageCrawler
# from icrawler import ImageDownloader
# import re

# class ByjusFilter(ImageDownloader):
#     def get_filename(self, task, default_ext):
#         url = task['file_url']
#         if 'byjus' in url.lower():
#             self.logger.info('Byju\'s image detected, skipping: %s', url)
#             return None
#         return super(ByjusFilter, self).get_filename(task, default_ext)

# def download_images(keyword, max_num=10):
#     google_crawler = GoogleImageCrawler(
#         downloader_cls=ByjusFilter,
#         storage={'root_dir': f'./images/{keyword}'}
#     )
#     google_crawler.crawl(
#         keyword=keyword + ' -site:byjus.com',  # Exclude byjus.com from search
#         max_num=max_num,
#     )

# # Usage
# if __name__ == "__main__":
#     while True:
#         search_topic = input("input ur query: ")
#         download_images(search_topic, max_num=5)
