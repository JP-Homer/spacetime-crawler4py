from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
from scraper import visited_defrags, longest_info, word_frequency


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()
    
    # gather report after crawler finishes
    with open("report.txt", "w") as file:
        file.write("1. " + str(len(visited_defrags)) + " unique pages found.\n")
        file.write("2. The longest page is " + longest_info["longest_page"] + " with " + str(longest_info["longest_page_num"]) + " words.\n")
        file.write("3. The 50 most common words are: \n")
        for counter, (key, value) in enumerate(sorted(word_frequency.items(), key = lambda x: x[1], reverse=True)):
            file.write(f"{key} -> {value}\n")
            if counter >= 49:
                break


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
