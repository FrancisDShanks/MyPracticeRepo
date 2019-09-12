from urllib.error import URLError
from urllib.request import urlopen
import re
import ssl
import pymongo


def decode_page(page_bytes, charsets=('utf-8',)):
        page_html = None
        for charset in charsets:
                try:
                        page_html = page_bytes.decode(charset)
                        break
                except UnicodeDecodeError as e:
                        print(e)
                        pass
        return page_html

def get_page_html(seed_url, *, retry_times=3, charsets=('utf-8',)):
        page_html = None
        try:
                page_html = decode_page(urlopen(seed_url).read(), charsets)
        except URLError:
                if retry_times > 0:
                        return get_page_html(seed_url, 
                                retry_times=retry_times - 1, 
                                charsets=charsets)
        return page_html


def get_matched_parts(page_html, pattern_str, pattern_ignore_case=re.I):
        pattern_regex = re.compile(pattern_str, pattern_ignore_case)
        return pattern_regex.findall(page_html) if page_html else []
                        

def build_mongo_document(links_list):
        link_pattern = r'href="(.*?)"'
        title_pattern = r'target="_blank">(.*?)</a>'
        result = []
        for link in links_list:
                tmp_dict = {'a_tag': link}
                tmp_dict['link'] = get_matched_parts(link, link_pattern)[0]
                tmp_dict['title'] = get_matched_parts(link, title_pattern)[0]        
                result.append(tmp_dict)
        return result



def start_crawler(seed_url, match_pattern, *, max_depth=-1):
        conn = pymongo.MongoClient('127.0.0.1', 27017)
        db = conn.test
        my_set = db.test_set
        title = []
        try:
                url_list = [seed_url]
                visited_url_list = {seed_url: 0}
                while url_list:
                        current_url = url_list.pop(0)
                        depth = visited_url_list[current_url]
                        print('visiting %s page!' % str(current_url), depth)
                        if depth != max_depth:
                                page_html = get_page_html(current_url, charsets=('utf-8', 'gbk', 'gb2312'))
                                links_list = get_matched_parts(page_html, match_pattern)
                                param_list = build_mongo_document(links_list)
                                
                                for p in param_list:
                                        link = p['link']
                                        t = p['title']
                                        title.append(t)
                                        '''
                                        if  link not in visited_url_list:
                                                visited_url_list[link] = depth + 1
                                                url_list.append(link)
                                        '''
                                

                                if param_list:
                                        my_set.insert_many(param_list)
                                else:
                                        print('Nothing has been saved!')
        except pymongo.errors.PyMongoError as e:
                print(e)
                pass
        finally:
                pass


def main():
        ssl._create_default_https_context = ssl._create_unverified_context
        url = 'http://sports.sohu.com/nba_a.shtml'
        pattern = r'<a[^>]+href=["\']http://www.sohu.com/a/.*?["\'].*?</a>'
        start_crawler(url,
                pattern,
                max_depth=2)
         

if __name__ == '__main__':
        main()