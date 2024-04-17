import re
from urllib.parse import urlparse
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

    # Soup object made out of current URL html content
    soup = bs(resp.raw_response.content, 'html.parser')
    # Strips the url to only include http: or https:
    url_protocol = url.split("/")[0]
    # All anchor tags in current URL
    a_links = soup.find_all('a')
    domain = urlparse(url).netloc
    links = []

    for tag in a_links:
        # Error handling for anchor with no href attribute
        try:
            cur_url = tag['href']
        except:
            continue # continue crawling 
        # if the protocol is missing
        if (tag['href'][0:2]) == '//':
            # add protocol to relative link
            cur_url = url_protocol + tag['href']
        elif ((tag['href'][0]) == '/'): # else if it is a relative link using the same base url
            cur_url = domain + tag['href']
        # elif ((tag['href'][0] != "#") and not (tag['href'].startswith("http") or tag['href'].startswith("https"))):
        #     cur_url = url + tag['href']

        if is_valid(cur_url):
            links.append(cur_url)

    # TODO: check domain/paths
    # *.ics.uci.edu/*
    # *.cs.uci.edu/*
    # *.informatics.uci.edu/*
    # *.stat.uci.edu/*
    # TODO: check if there is a href
    # TODO: lxml parsing?
    # TODO: include or not include php?
    #print(links)

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
        return any(domain in url for domain in valid_domains) and not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
