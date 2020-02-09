import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from googlesearch import search
import argparse

def printmd(string):
    display(Markdown(string))

def get_hymnal_url(title):
    for result in search(title, tld='com', lang='en', num=10, start=0, stop=50, pause=2.0):
        if 'hymnary' in result:
            return result

def get_hymn_lyrics(site, hymn_number=None, url=None, file_name=None):
    if site == 'christian study':
        if (hymn_number < 100) & (hymn_number >= 10):
            hymn_number = f'0{hymn_number}'
        elif (hymn_number < 10):
            hymn_number = f'00{hymn_number}'
        url = f'http://www.christianstudy.com/data/hymns/text/life{hymn_number}.html'
        response = requests.get(url)
        response.encoding = 'big5'
        soup = BeautifulSoup(response.text, "html.parser")

        for p in soup.findAll('p'):
            lyrics = str(p.findAll('font'))
            lyrics = lyrics.replace('<li>', '').replace('</li>', '')
            lyrics = lyrics.replace('<ol>', '').replace('</ol>', '')
            lyrics = lyrics.replace('<br/>', '')
            lyrics = lyrics.replace('<font size="1">', '').replace('</font>', '').replace('<font size="+2">', '')
            lyrics = lyrics.replace('[', '').replace(']', '').replace(',', '')
            if lyrics is not None:
                with open(file_name, 'a', encoding='utf-8') as f:
                    f.write(lyrics)
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for p in soup.findAll('p'):
            try:
                if p.contents[0][0].isdigit():
                    lyrics = str(p)
                    lyrics = lyrics.replace('<br/>', '')
                    lyrics = lyrics.replace('<p>', '').replace('</p>', '')
                    if lyrics is not None:
                        with open(file_name, 'a') as f:
                            f.write(lyrics)
                            f.write('\n')
            except:
                pass




def get_hymn_titles(url=f'http://www.christianstudy.com/lifehymns.html'):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    hymn_titles = {}
    for tr in soup.findAll('tr'):
        for td in tr.findAll('td'):
            try:
                if (str(td.contents[0].split('.')[0]).isdigit()):
                    for small in td.findAll('small'):
                        temp_title = small.contents[0]
                    hymn_titles[int(str(td.contents[0].split('.')[0]))] = temp_title
            except Exception as e:
                pass
    return hymn_titles

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def main(hymn_numbers):
    file_name = f'lyrics_for_{hymn_numbers.replace(",", "_")}.txt'
    with open(file_name, 'w') as f:
        f.write('Lyrics for Hymns\n')
    hymn_titles = get_hymn_titles()
    hymn_numbers = hymn_numbers.split(',')
    hymn_numbers = [int(x) for x in hymn_numbers]
    for hymn_number in hymn_numbers:
        get_hymn_lyrics(site='christian study', hymn_number=hymn_number, file_name=file_name)

    for hymn_number in hymn_numbers:
        with open(file_name, 'a') as f:
            f.write('\n')
            f.write(hymn_titles[hymn_number])
            f.write('\n')
        url = get_hymnal_url(title=hymn_titles[hymn_number] + ' hymn')
        get_hymn_lyrics(site='hymnal', url=url, file_name=file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hymns', help='hymn number (e.g. 1,100,34)')

    args = parser.parse_args()
    main(args.hymns)
