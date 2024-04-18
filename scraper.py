import re
from urllib import robotparser
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    if resp.status != 200:
        print(resp.error)
        return list()
    
    # TODO: crawl delay?
    # TODO: iter.parse

    robots_file = url + '/robots.txt'
    rp = robotparser.RobotFileParser(robots_file)
    rp.read()
    if not rp.can_fetch("IR US24 23141678,14782048", url):
        return list()


    # Soup object made out of current URL html content
    soup = bs(resp.raw_response.content, 'lxml')
    # All anchor tags in current URL
    a_links = soup.find_all('a')
    links = []

    for tag in a_links:
        # Error handling for anchor with no href attribute
        try:
            cur_url = tag['href']
        except:
            continue # continue to next link

        # If href tag is empty string
        if len(tag['href']) == 0:
            continue
        
        # Join the relative path to the base path to create an absolute path
        cur_url = urljoin(url, cur_url)

        # TODO: optimize?
        if rp.can_fetch("IR US24 23141678,14782048", cur_url) and is_valid(cur_url):
            links.append(cur_url)

    return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    # TODO: optimize?
    valid_domains = ['.ics.uci.edu', '.cs.uci.edu', '.informatics.uci.edu', '.stat.uci.edu']
    
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return any(domain in url for domain in valid_domains) and (not '#' in url) and not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|php|r"
            + r"|png|tiff?|mid|mp2|mp3|mp4|bib"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
