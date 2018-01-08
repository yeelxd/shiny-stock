# Crawler Test For Beauty Pics
# Dependency Requests Modules
# Python 3.6.3
import urllib.request
import re

DONE_HREF_LIST = []


def get_page_data(page_url):
    user_agent = """Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0)
                    Gecko/20100101 Firefox/57.0"""
    header = {'User-Agent': user_agent, 'Accept': '*/*'}
    req = urllib.request.Request(url=page_url, headers=header)
    resp = urllib.request.urlopen(req)
    data = resp.read()

    return data


def get_image_urls(html_content):
    # image_urls = re.findall(r'http://images.+\.jpg', htmlContent)
    prefix_url = "http://mm.chinasareview.com/wp-content/uploads/"
    image_urls = re.findall(
        'src="(' + prefix_url + r'\w{5}/\d{2}/\d{2}/\d{2}.jpg)"',
        str(html_content)
    )
    return image_urls


def get_href_urls(html_content):
    href_url_list = re.findall(
        r'<a href="(http://www.meizitu.com/a/\d+.html)"',
        str(html_content)
    )
    return href_url_list


def load_index(url_index):
    image_index = 1
    print("开始下载页面: ", url_index)
    index_page_data = get_page_data(url_index)
    href_url_list = get_href_urls(index_page_data)
    for href_url in href_url_list:
        try:
            print("开始处理网页中的链接: ", href_url)
            if DONE_HREF_LIST.count(href_url) < 1:
                page_data = get_page_data(href_url)
                image_url_list = get_image_urls(page_data)
                for imgPath in image_url_list:
                    try:
                        print("正在下载图片: ", imgPath)
                        image_name = "C:/WorkCenter/_Temp/PyDownload/" + \
                            str(image_index) + ".jpg"
                        # urllib.request.urlretrieve(imgPath, image_name)
                        file = open(image_name, 'wb')
                        file.write(get_page_data(imgPath))
                        file.close()
                        image_index += 1
                        # URL添加到已处理列表
                        DONE_HREF_LIST.append(href_url)
                    except IOError:
                        print("Oops! IOError.line 61.Arise.")
                        continue
        except IOError:
            print("Oops! IOError.line 64.Arise.")
            continue


# 循环73页 下载每一页的图片链接
moreCount = 1
while moreCount <= 73:
    try:
        basePageUrl = "http://www.meizitu.com/a/more_"
        basePageUrl += str(moreCount) + ".html"
        moreCount += 1
        load_index(basePageUrl)
    except IOError:
        print("Oops! IOError.line 77s.Arise.")
        continue
print("All Done!")
