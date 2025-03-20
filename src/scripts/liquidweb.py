from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def GetPostingsUrl(url_host, url_path):
    return url_host + url_path

def RunScan():
    url_host = 'https://jobs.jobvite.com'
    url_path = '/liquidweb'
    job_postings = []

    with sync_playwright() as pw:
        print('TASK:\tBrowser Start')

        # browser = pw.chromium.launch(headless=False, slow_mo=1000)
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 690, 'height': 740})
        page = context.new_page()

        print('TASK:\tGoTo -->', GetPostingsUrl(url_host, url_path))
        page.goto(GetPostingsUrl(url_host, url_path))

        print('TASK:\tWait --> .jv-job-list')
        page.wait_for_selector('.jv-job-list')
        print('TASK:\tFound --> .jv-job-list')

        soup = BeautifulSoup(page.content(), features='html.parser')

        entities = []

        for entity in soup.select('h3'):
            entities.append(entity.contents[0])

        for i_group, posting_group in enumerate(soup.select('.jv-job-list')):
            for i_posting, posting in enumerate(posting_group.select('tr')):
                try:
                    posting.select_one('td').contents[0]

                    name = posting.select_one('a').contents[0]
                    link = url_host + posting.select_one('a').get('href')
                    location = posting.select_one('.jv-job-list-location').text.replace('\n', '').replace('            ', ' ').replace('         ', ' ').strip()
                    entity = entities[i_group]

                    job_postings.append([
                        link,
                        entity,
                        name,
                        location
                    ])

                except:
                    pass

        print('TASK:\tBrowser Close')
        browser.close()

        ws_content = {
            'name': 'Liquid Web',
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
                        'label': 'Entity',
                        'size': 0,
                        'filter': False,
                        'is_link': False
                    },
                    {
                        'label': 'Name',
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