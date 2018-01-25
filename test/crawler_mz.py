# Crawler Test For Beauty Pics
# Dependency Requests Modules
# Python 3.6.3
import urllib.request
import re


class CrawlerMZ(object):

    # 初始化方法
    # 创建完对象后会自动被调用
    def __init__(self):
        self.DONE_HREF_LIST = []

    @staticmethod
    def get_page_data(page_url):
        user_agent = """Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0)
                        Gecko/20100101 Firefox/57.0"""
        header = {'User-Agent': user_agent, 'Accept': '*/*'}
        req = urllib.request.Request(url=page_url, headers=header)
        resp = urllib.request.urlopen(req)
        data = resp.read()
        return data

    @staticmethod
    def get_image_urls(html_content):
        # image_urls = re.findall(r'http://images.+\.jpg', htmlContent)
        prefix_url = "http://mm.chinasareview.com/wp-content/uploads/"
        image_urls = re.findall(
            'src="(' + prefix_url + r'\w{5}/\d{2}/\d{2}/\d{2}.jpg)"',
            str(html_content)
        )
        return image_urls

    @staticmethod
    def get_href_urls(html_content):
        href_url_list = re.findall(
            r'<a href="(http://www.meizitu.com/a/\d+.html)"',
            str(html_content)
        )
        return href_url_list

    # 下载页面中的图片
    def load_index(self, url_index):
        image_index = 1
        print("开始下载页面: ", url_index)
        index_page_data = self.get_page_data(url_index)
        href_url_list = self.get_href_urls(index_page_data)
        for href_url in href_url_list:
            try:
                print("开始处理网页中的链接: ", href_url)
                if self.DONE_HREF_LIST.count(href_url) < 1:
                    page_data = self.get_page_data(href_url)
                    image_url_list = self.get_image_urls(page_data)
                    for imgPath in image_url_list:
                        try:
                            print("正在下载图片: ", imgPath)
                            image_name = "C:/WorkCenter/_Temp/PyDownload/" + \
                                str(image_index) + ".jpg"
                            # urllib.request.urlretrieve(imgPath, image_name)
                            file = open(image_name, 'wb')
                            file.write(self.get_page_data(imgPath))
                            file.close()
                            image_index += 1
                            # URL添加到已处理列表
                            self.DONE_HREF_LIST.append(href_url)
                        except IOError:
                            print("Oops! IOError.line 61.Arise.")
                            continue
            except IOError:
                print("Oops! IOError.line 64.Arise.")
                continue


if __name__ == "__main__":
    CrawlerMZ = CrawlerMZ()
    # 循环73页 下载每一页的图片链接
    more_cnt = 1
    while more_cnt <= 73:
        try:
            base_page_url = "http://www.meizitu.com/a/more_"
            base_page_url += str(more_cnt) + ".html"
            more_cnt += 1
            CrawlerMZ.load_index(base_page_url)
        except IOError:
            print("Oops! IOError.line 77s.Arise.")
            continue
    print("All Done!")
