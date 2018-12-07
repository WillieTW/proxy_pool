import requests
import re

class ProxyWebsite(object):
    def __init__(self, url, pattern, ip_pos, port_pos):
        self.url = url
        self.pattern = pattern
        self.ip_pos = ip_pos
        self.port_pos = port_pos


class Crawler(object):
    @staticmethod
    def get_html(proxy_website):
        try:
            rsp = requests.get(proxy_website.url)
            return (0, rsp.text)
        except Exception as e:
            return (-1, e) 


class Extractor(object):
    @staticmethod
    def get_data(proxy_website, html):
        try:
            pattern = re.compile(proxy_website.pattern, re.M|re.S )  
            return  map(lambda x:(x[proxy_website.ip_pos], x[proxy_website.port_pos]), pattern.findall(html)) 
        except Exception as e:
            return (-1, e) 


class Validator(object):
    @staticmethod
    def get_baidu(ip, port):
        try:
            proxies = {'http': 'http://%s:%s' %(ip, port), 'https': 'http://%s:%s' %(ip, port)}
            http_valid_result  = False
            rsp = requests.get('http://www.baidu.com', proxies = proxies, verify=False, timeout=(10, 60))
            if rsp.status_code == 200:
                http_valid_result  = True
            rsp = requests.get('https://www.baidu.com', proxies = proxies, verify=False, timeout=(10, 60))
            if rsp.status_code == 200:
                https_valid_result  = True
            return (0, (http_valid_result, https_valid_result)) 
        except Exception as e:
            return (-1, e) 

class Data(object):
    def __init__(self, ip, port, http_enable, https_enable):
        self.ip = ip
        self.port = port
        self.http_enable = http_enable
        self.https_enable = https_enable


if __name__ == '__main__':
    proxy_website = ProxyWebsite('https://www.kuaidaili.com/ops/', '<td data-title="IP">(.*?)</td>(.*?)<td data-title="PORT">(.*?)</td>(.*?)<td data-title="类型">(.*?)</td>', 0, 2)

    ret_code, ret_value = Crawler.get_html(proxy_website)

    ret_list = Extractor.get_data(proxy_website, ret_value)

    for i in ret_list:
        print (Validator.get_baidu(i[0], i[1]))


