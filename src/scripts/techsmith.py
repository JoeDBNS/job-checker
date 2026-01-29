from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def GetPostingsUrl(url_host, url_path):
    return url_host + url_path

def RunScan():
    url_host = 'https://www.techsmith.com'
    url_path = '/careers/open-positions/'
    job_postings = []

    with sync_playwright() as pw:
        print('TASK:\tBrowser Start')

        # browser = pw.chromium.launch(headless=False, slow_mo=1000)
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 690, 'height': 740})
        page = context.new_page()

        print('TASK:\tGoTo -->', GetPostingsUrl(url_host, url_path))
        page.goto(GetPostingsUrl(url_host, url_path))

        print('TASK:\tWait --> .careers')
        page.wait_for_selector('.careers')
        print('TASK:\tFound --> .careers')

        soup = BeautifulSoup(page.content(), features='html.parser')

        for posting in soup.select('.careers-position'):
            name = posting.select('p')[0].contents[0].contents[0]
            description = posting.select('p')[1].contents[0]
            link = posting.select_one('a').get('href')

            job_postings.append([
                url_host + link,
                name,
                description
            ])

        print('TASK:\tBrowser Close')
        browser.close()

        ws_content = {
            'name': 'Techsmith',
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
                        'label': 'Description',
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