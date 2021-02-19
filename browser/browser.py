from bs4 import BeautifulSoup
from collections import deque
from colorama import init, deinit
from colorama import Fore
import os
import requests
import sys

init(autoreset=True)

# remove the directory you created
class TextBrowser:
    """A simple text based browser."""

    def __init__(self):
        self.browser_history = deque()  # stack to hold the websites visited by client.
        self.directory = ''    # directory to store all the webpage visited by client
        self.previous_page = ''         # stores the previous page visited by client.

    def is_valid(self, url):
        """Check if the domain is valid."""
        domains = url.split('.')
        if domains and len(domains[-1]) == 3:
            return True
        return False

    def websites_directory(self):
        """Make directory if directory exists return the absolute path to the directory.
        else list of direcotry files and folder."""
        if os.access(self.directory, os.F_OK):  # check if the directory exists.
            return os.listdir(self.directory)  # return path and content of directory.
        os.mkdir(self.directory)
        return None

    def cache_page(self, website, page_html):
        """Create a file with the page name and save it's html/text."""
        with open(f'{os.path.join(self.directory, website)}.txt',
                  mode='w', encoding='utf-8') as file:
            file.write(page_html)

    def is_cached(self, site):
        """Return boolean if file is saved.
        :argument site : Domain Name of the site being searched.

        :return: Boolean True or False"""
        for file in self.websites_directory():
            if file == site:
                return True
        return False

    def parse_html(self, resp):
        """Return text of the passed html.

        :argument resp : response object returned from requesting the site
        :return: string
        """

        html_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol']
        text = []
        soup = BeautifulSoup(resp.content, 'html.parser')
        # for removing any duplicate string
        for tag in soup.find_all(html_tags):
            for string in tag.stripped_strings:
                if string not in text:
                    if tag.name == 'a':
                        text.append(Fore.BLUE + string)
                    else:
                        text.append(string)

        return '\n'.join(text)

    def get_page(self, req_url):
        """Request for the page and return the text version of response,
        if there is any."""
        response = requests.get(req_url)
        if response.status_code == 200:
            return self.parse_html(response)
        else:
            print('[ERROR]: UNABLE TO RETRIEVE PAGE!.')
            return ''

    def add_history(self, page_name):
        """Add the page to history stack."""
        self.browser_history.append(page_name)

    def get_previous_page(self):
        """Return the last added page if the stack is not empty."""
        if self.browser_history:
            return self.browser_history.pop()
        return ''

    def show_page(self, domain):
        """Check if the page is cached if not request the page and cache it."""
        page = domain[0:domain.index('.')]

        if self.is_cached(page):
            # print('Cached page.'.center(50, '-'))
            with open(os.path.join(self.directory, page),
                      mode='r', encoding='utf-8') as file:
                for line in file:   # Only print the first 200 bytes.
                    print(line.strip())
        else:
            # print('Requesting page'.center(50, '-'))
            url = f'https://{domain}'
            text_page = self.get_page(url)
            print(text_page)
            self.cache_page(page, text_page)

    def browse(self):
        """Take url and print the response"""
        # print('Starting browser'.center(50, '-'))
        self.directory = sys.argv[1]  # take the directory name
        self.websites_directory()

        # browser loop
        while True:
            user_input = input('Search (domain or "exit"-> exit): ')

            if user_input == 'exit':
                deinit()
                break
            elif user_input == 'back':
                prev_page = self.get_previous_page()
                if prev_page:   # check if there was a previous page.
                    self.show_page(prev_page)
            elif self.is_valid(user_input):
                self.show_page(user_input)
                self.add_history(self.previous_page)
                self.previous_page = user_input     # change the previous page to the current page.
            else:
                print('[ERROR]: Incorrect URL')

        # print('Closing browser'.center(50, '-'))

b = TextBrowser()
b.browse()
