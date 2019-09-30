import datetime
import feedparser
from time import mktime, time, sleep
import requests
import traceback
from urllib.request import build_opener, HTTPCookieProcessor, Request
import re

from scraper_const import feeds, cats, buzzwords

# Edit these dependant on the desired behaviour --------
URL_PROXY_PREFIX = "http://proxy.uchicago.edu/login?url="
RSS_USE_PREFIX = True

# -------------------------------------------------------

class Article:
    CSS_DIV_CLASS = 'Article'
    def __init__(self, post, **kwargs):
        self.raw_post = post
        self.journal = 'Article'
        self.journal_img = None
        self.use_proxy_prefix = False
        for kw, val in kwargs.items():
            setattr(self, kw, getattr(post, val, None))
        #Get the authors
        self.authors = ', '.join(a['name'] for a in post.authors if 'name' in a) if hasattr(post, 'authors') else None

        #Get the date
        self.date = datetime.date.today()
        for kw in ['published_parsed','date_parsed']:
            if hasattr(post, kw):
                self.date = datetime.date.fromtimestamp(mktime(getattr(post, kw)))
                break
            
    def build_html(self, preview = True):
        title, abstract = self.title, self.abstract
        html_img = ''
        if preview:
            try:
                preview = generate_dict(self.url)
                if any(ext in preview['image'] for ext in ['png', 'jpeg']):
                    html_img = '<img src="{}" ALIGN="left">'.format(preview['image'])
                title, abstract = preview['title'], preview['description']
            except:
                print("Failed to load preview for: {}".format(self.url))
                traceback.print_exc()
        
        # Remove some html tags from the abstract
        img_in_abstract = re.search("<img [\s\S]*?>", abstract)
        if not img_in_abstract is None:
            img_in_abstract = img_in_abstract.group()
            abstract = abstract.replace(img_in_abstract, '')
            if html_img == '':
                #TODO: Should check that there is not already a align parameter and remove
                # TODO: Adjust the height and width
                html_img = img_in_abstract[:-1] + ' align="left"' + '>'
                # html_img = img_in_abstract

        html = '<div class="{}">'.format(self.CSS_DIV_CLASS)
        html += '<div class="journal">{}<span>&nbsp;&nbsp;&nbsp;{}</span></div>'.format('<img src="{}">'.format(self.journal_img) if not self.journal_img is None else '',self.journal)
        html += '<a href="{}" target="_blank"><h3>{}</h3></a>'.format(URL_PROXY_PREFIX+self.url if self.use_proxy_prefix else self.url, title)
        html += html_img
        html += '{}<br>Date:<i>{}</i>\n<br><br>{}<br>'.format(self.authors, self.date, abstract)
        html += '<br><br><i>Buzzwords: {}</i><br>'.format(', '.join(self.get_relevant_buzzwords()))
        html += '<a href={} target="_blank">PDF</a></div>'.format(self.pdf) if hasattr(self, 'pdf') else "</div>"
        return html

    def get_relevant_buzzwords(self):
        results =[]
        text = ''
        for content in [self.title, self.abstract, self.authors]:
            text += content if not content is None else ''
        
        for word in buzzwords:
            if word.lower() in text.lower():
                results.append(word)
        return results
        
    def contains_buzzwords(self):
        return len(self.get_relevant_buzzwords()) > 0


class RSS_Articles(Article):
    CSS_DIV_CLASS = 'Article RSS'
    def __init__(self, post, feed, url='link', title='title', abstract='description', authors='author', **kwargs):
        super().__init__(post, url=url, title=title, abstract=abstract, authors=authors, **kwargs)
        self.feed = feed
        self.journal = feed.journal_name
        self.journal_img = feed.journal_img
        self.use_proxy_prefix = RSS_USE_PREFIX

    def build_html(self, preview=None):
        if preview is None:
            preview = not any(bad_ones in self.url for bad_ones in ['acsphotonics'])
        return super().build_html(preview=preview)

class ArXiV_Articles(Article):
    CSS_DIV_CLASS = 'Article ArXiV'
    def __init__(self, post, url='link', title='title', abstract='summary', **kwargs):
        super().__init__(post, url=url, title=title, abstract=abstract, **kwargs)
        self.journal = 'ArXiV'
        self.journal_img = 'img/arxiv.png'
        for ref in post.links:
            if ref['type'] == 'application/pdf':
                self.pdf = ref['href']
    def build_html(self, preview=False):
        return super().build_html(preview=preview)
        
        
        
def scrape_RSS(days):
    results = []
    today = datetime.date.today()
    datetosearch = today-datetime.timedelta(days=days)
    
    for feed in feeds:
        try:
            d = feedparser.parse(feed.url)
            for post in d.entries:
                a = RSS_Articles(post, feed)
                if a.date >= datetosearch and a.contains_buzzwords():
                    results.append(a)
        except:
            traceback.print_exc()
            print(post)
            print(post.authors)
            print("Failed to import feed: {}".format(feed.url))
    return results

def scrape_ArXiV(days):
    results = []
    today = datetime.date.today()
    datetosearch = today-datetime.timedelta(days=days+1)
    dates_str = [d.strftime('%Y%m%d%H%M') for d in [datetosearch,today]]
    
    # Build ArXiV query
    string = 'http://export.arxiv.org/api/query?search_query=('
    string += ('all:{}+OR+'*(len(buzzwords)-1)+'all:{})').format(*buzzwords)
    string += ('+AND+({}'+'+OR+{}'*(len(cats)-1)+')').format(*cats)
    string += '+AND+submittedDate:[{}+TO+{}]'.format(*dates_str)
    string += '&sortBy=submittedDate&max_results=10000'

    try:
        # Issue query
        feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
        feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'
        response = requests.get(string)
        response.encoding = 'utf-8'

        d = feedparser.parse(response.text)
        for post in d.entries:
            a = ArXiV_Articles(post)
            if a.contains_buzzwords():
                results.append(a)
    except:
        print("Failed to import from ArXiV")
        
    return results

def build_html(articles, html_header=""):
    articles.sort(key=lambda a: a.date, reverse=True)
    t0 = time()
    pre_html = """
<html>
<head>
    <title>ScraperBot Results</title>
    <link rel="stylesheet" href="scraperbot.css">
</head>
"""
    body_html = '\n'.join(a.build_html() for a in articles)
    post_html = "</div></body></html>"
    pre_html += "<div class='stats'>Took {:.1f}s to generate the page</div>".format(time()-t0)
    pre_html += html_header
    pre_html += '<div class="Container">\n<h1>ScraperBot Results</h1>\n'
    return pre_html + body_html + post_html

def scrape(days):
    t0 = time()
    rss = scrape_RSS(days) 
    t1 = time()
    arxiv = scrape_ArXiV(days)
    header  = "<div class='stats'>RSS feeds -- Found {} articles. Took {:.1f}s</div>\n".format(len(rss),t1-t0)
    header += "<div class='stats'>ArXiV -- Found {} articles. Took {:.1f}s</div>\n".format(len(arxiv),time()-t1)
    html = build_html(rss+arxiv, header)
    return rss+arxiv, html





"""
The following is a slightly modified version of the link_preview package which can be found here:
https://github.com/aakash4525/py_link_preview/blob/master/link_preview/link_preview.py

I've copied it here to:
    1. Limit the use of external pakages
    2. Make the url request compatible with some of the journals (ie: set user agent and enable cookie)
"""

def generate_dict(url):
    '''
        returns dictionary containing elements of link_preview:
            dict_keys :
                'title' : '',
                'description': '',
                'image': '',
                'website': ''
        if Exception occurs, it raises Exception of urllib.request module.
    '''
    return_dict = {}
    try:
        #----------------------------------  MODIFIED CODE  --------------------------------------
        opener = build_opener(HTTPCookieProcessor())
        html = opener.open(Request(
                            url, 
                            data=None, 
                            headers={
                                'User-Agent': 'Mozilla'
                            }
        ), timeout=30).read().decode('utf-8')
        #----------------------------------------------------------------------------------------
        meta_elems = re.findall('<[\s]*meta[^<>]+og:(?:title|image|description)(?!:)[^<>]+>', html)
        og_map = map(return_og, meta_elems)
        og_dict = dict(list(og_map))
    
    #     title
        try:
            return_dict['title'] = og_dict['og.title']
        except KeyError:
            return_dict['title'] = find_title(html)
    
    #     description
        try:
            return_dict['description'] = og_dict['og.description']
        except KeyError:
            return_dict['description'] = find_meta_desc(html)
    
    #     website
        return_dict['website'] = find_host_website(url)
    
    #     Image
        try:
            return_dict['image'] = og_dict['og.image']
        except KeyError:
            image_path = find_image(html)
            if 'http' not in image_path:
                image_path = 'http://' + return_dict['website'] + image_path
            return_dict['image'] = image_path
        
        return return_dict
    
    except Exception as e:
        'Raises Occurred Exception'
        raise e

def return_og(elem):
    '''
        returns content of og_elements
    '''
    content = re.findall('content[\s]*=[\s]*"[^<>"]+"', elem)[0]
    p = re.findall('"[^<>]+"', content)[0][1:-1]
    if 'og:title' in elem:
        return ("og.title", p)
    elif 'og:image' in elem and 'og:image:' not in elem:
        return ("og.image", p)
    elif 'og:description' in elem:
        return ("og.description", p)
    
def find_title(html):
    '''
        returns the <title> of html
    '''
    try:
        title_elem = re.findall('<[\s]*title[\s]*>[^<>]+<[\s]*/[\s]*title[\s]*>', html)[0]
        title = re.findall('>[^<>]+<', title_elem)[0][1:-1]
    except:
        title = ''
    return title

def find_meta_desc(html):
    '''
        returns the description (<meta name="description") of html
    '''
    try:
        meta_elem = re.findall('<[\s]*meta[^<>]+name[\s]*=[\s]*"[\s]*description[\s]*"[^<>]*>', html)[0]
        content = re.findall('content[\s]*=[\s]*"[^<>"]+"', meta_elem)[0]
        description = re.findall('"[^<>]+"', content)[0][1:-1]
    except:
        description = ''
    return description

def find_image(html):
    '''
        returns the favicon of html
    '''
    try:
        favicon_elem = re.findall('<[\s]*link[^<>]+rel[\s]*=[\s]*"[\s]*shortcut icon[\s]*"[^<>]*>', html)[0]
        href = re.findall('href[\s]*=[\s]*"[^<>"]+"', favicon_elem)[0]
        image = re.findall('"[^<>]+"', href)[0][1:-1]
    except:
        image = ''
    return image

def find_host_website(url):
    '''
        returns host website from the url
    '''
    return list(filter(lambda x: '.' in x, url.split('/')))[0]



"""
This handles the execution from a coomand line
"""

import webbrowser, os, sys

#Remove previous results
try:
    os.remove("results.htm")
except:
    pass

#Check if a specific number of days is to be scraped
days_to_scrape = 1
if len(sys.argv) > 1:
    try:
        days_to_scrape = int(sys.argv[1])
    except:
        pass
print("Searching through the last {} days...".format(days_to_scrape))

#Do the thing
a, html = scrape(days_to_scrape)
with open("results.htm", 'w+') as f:
    f.write(html.encode('ascii', 'ignore').decode('ascii'))

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
webbrowser.get(chrome_path).open("results.htm")
