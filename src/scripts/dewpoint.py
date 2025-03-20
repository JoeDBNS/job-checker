from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def GetPostingsUrl(url_host, url_path):
    return url_host + url_path

def RunScan():
    url_host = 'https://www.dewpoint.com'
    url_path = '/careers/'
    job_postings = []

    with sync_playwright() as pw:
        print('TASK:\tBrowser Start')

        browser = pw.chromium.launch(headless=False, slow_mo=1000)
        # browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 690, 'height': 740})
        page = context.new_page()

        print('TASK:\tGoTo -->', GetPostingsUrl(url_host, url_path))
        page.goto(GetPostingsUrl(url_host, url_path))

        print('TASK:\tWait --> .bzOpening')
        page.mouse.wheel(0, 100) # triggers openings to load
        page.wait_for_selector('.bzOpening')
        print('TASK:\tFound --> .bzOpening')

        soup = BeautifulSoup(page.content(), features='html.parser')

        for posting in soup.select('.bzOpening'):
            name = posting.select_one('h2').contents[0]
            link = posting.select_one('a').get('href')
            type = posting.select_one('.bzType').text
            location = posting.select_one('.bzLocation').text

            job_postings.append([
                link,
                name,
                type,
                location
            ])

        print('TASK:\tBrowser Close')
        browser.close()

        ws_content = {
            'name': 'Dewpoint',
            'config': {
                'general': {
                    'add_headers': True
                },
                'columns': [
                    {
                        'label': 'Link',
                        'size': 30,
                        'filter': False,
                        'is_link': True
                    },
                    {
                        'label': 'Name',
                        'size': 0,
                        'filter': False,
                        'is_link': False
                    },
                    {
                        'label': 'Type',
                        'size': 0,
                        'filter': False,
                        'is_link': False
                    },
                    {
                        'label': 'Location',
                        'size': 0,
                        'filter': False,
                        'is_link': False
                    }
                ],
                'rows': {
                    'colors': []
                }
            },
            'data': job_postings
        }

        # Color headers row gray
        ws_content['config']['rows']['colors'].append(
            {
                'row_num': 0,
                'color_hex': 'd4d4d4'
            }
        )

    return ws_content