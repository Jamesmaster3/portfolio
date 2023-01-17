import requests
from bs4 import BeautifulSoup
import pprint


def loop_pages(pages):
    res_list = []
    page = 1
    for x in range(0, pages):
        res_list.append(requests.get(
            f'https://news.ycombinator.com/news?p={page}').text)
        page = page + 1
    return " ".join(res_list)



def create_custom_hn(links, subtext):
    hnl = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        if href.startswith('item'):
            href = f'https://news.ycombinator.com/{href}'
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hnl.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hnl)


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def run_hackernews(pages):
    soup = BeautifulSoup(loop_pages(pages), 'html.parser')
    links = soup.select('.titleline > a')
    subtext = soup.select('.subtext')
    return create_custom_hn(links, subtext)


if __name__ == '__main__':
    pprint.pprint(run_hackernews(2))