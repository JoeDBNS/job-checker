from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import modules.module_xlsx_maker as xm


def GetPostingsUrlByPage(url_host, url_path, page):
    return url_host + url_path + str(page)

def RunScan():
    url_host = 'https://www.governmentjobs.com'
    url_path = '/careers/michigan?department[0]=State%20Police&department[1]=Technology%2C%20Management%20and%20Budget&department[2]=House%20of%20Representatives&sort=PositionTitle%7CAscending&page='
    page_number = 1
    job_postings = [
        [
            'link',
            'label',
            'department',
            'category',
            'location',
            'type',
            'pay',
            'posted_on',
            'closes_in_x',
            'closes_in_type',
            'is_new'
        ]
    ]

    with sync_playwright() as pw:
        print('TASK:\tBrowser Start')

        # browser = pw.chromium.launch(headless=False, slow_mo=1000)
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 690, 'height': 740})
        page = context.new_page()

        print('TASK:\tGoTo -->', GetPostingsUrlByPage(url_host, url_path, page_number))
        page.goto(GetPostingsUrlByPage(url_host, url_path, page_number))

        print('TASK:\tWait --> #job-postings-number')
        page.wait_for_selector('#job-postings-number')

        print('TASK:\tWait --> .list-item')
        page.wait_for_selector('.list-item')

        soup = BeautifulSoup(page.content(), features='html.parser')

        # This number is usually wrong but I do not know why - !!!!
        total_postings = int(soup.select_one('#job-postings-number').text)
        total_postings_per_page = len(soup.select('.list-item'))

        total_pages = total_postings // total_postings_per_page

        if ((total_postings % total_postings_per_page) > 0):
            total_pages += 1

        # Bad fix for broken posting count display - !!!!
        total_pages = 20

        for posting in soup.select('.list-item'):
            posting_details_top = posting.select_one('.list-meta').contents
            posting_details_top = [i for i in posting_details_top if i != '\n']

            posting_details_bottom = posting.select_one('.list-published').contents
            posting_details_bottom = [i for i in posting_details_bottom if i != '\n']

            # Handling 'new' Postings
            if (posting.select_one('.new-job-label')):
                is_posting_new = True
            else:
                is_posting_new = False

            # Handling no-close Postings
            if (len(posting_details_bottom) == 1):
                closes_in_x = 99
                closes_in_type = ''
            else:
                # Handling Continuous Postings
                if (posting_details_bottom[2].contents[0].find('Continuous') != -1):
                    posting_details_bottom[2].contents[0] = 'Continuous'
                    closes_in_x = 99
                    closes_in_type = 'Continuous'
                else:
                    closes_in_x = posting_details_bottom[2].contents[0].split(' ')[2]
                    closes_in_type = posting_details_bottom[2].contents[0].split(' ')[-1]

            job_postings.append([
                url_host + posting.select_one('h3').select_one('a').get('href'),
                posting.select_one('h3').text.replace('\\n', '').replace('\nNew', '').strip(),
                posting_details_top[3].contents[0].replace('\\n', '').strip(),
                posting_details_top[2].contents[0].replace('\\n', '').replace('Category: ', '').strip(),
                posting_details_top[0].text.replace('\\n', '').strip(),
                posting_details_top[1].contents[0].replace('\\n', '').strip(),
                posting_details_top[1].contents[2].replace('\\n', '').strip(),
                posting_details_bottom[0].contents[0].contents[0],
                closes_in_x,
                closes_in_type,
                is_posting_new
            ])

        print('\n\nGathering Postings...', len(job_postings) - 1)

        for page_number in range(1, total_pages):
            print('TASK:\tGoTo -->', GetPostingsUrlByPage(url_host, url_path, page_number))
            page.goto(GetPostingsUrlByPage(url_host, url_path, page_number))

            print('TASK:\tWait --> .list-item')
            try:
                page.wait_for_selector('.list-item')
            except:
                break

            soup = BeautifulSoup(page.content(), features='html.parser')

            for posting in soup.select('.list-item'):
                posting_details_top = posting.select_one('.list-meta').contents
                posting_details_top = [i for i in posting_details_top if i != '\n']

                posting_details_bottom = posting.select_one('.list-published').contents
                posting_details_bottom = [i for i in posting_details_bottom if i != '\n']

                # Handling 'new' Postings
                if (posting.select_one('.new-job-label')):
                    is_posting_new = True
                else:
                    is_posting_new = False

                # Handling no-close Postings
                if (len(posting_details_bottom) == 1):
                    closes_in_x = 99
                    closes_in_type = ''
                else:
                    # Handling Continuous Postings
                    if (posting_details_bottom[2].contents[0].find('Continuous') != -1):
                        posting_details_bottom[2].contents[0] = 'Continuous'
                        closes_in_x = 99
                        closes_in_type = 'Continuous'
                    else:
                        closes_in_x = posting_details_bottom[2].contents[0].split(' ')[2]
                        closes_in_type = posting_details_bottom[2].contents[0].split(' ')[-1]

                job_postings.append([
                    url_host + posting.select_one('h3').select_one('a').get('href'),
                    posting.select_one('h3').text.replace('\\n', '').replace('\nNew', '').strip(),
                    posting_details_top[3].contents[0].replace('\\n', '').strip(),
                    posting_details_top[2].contents[0].replace('\\n', '').replace('Category: ', '').strip(),
                    posting_details_top[0].text.replace('\\n', '').strip(),
                    posting_details_top[1].contents[0].replace('\\n', '').strip(),
                    posting_details_top[1].contents[2].replace('\\n', '').strip(),
                    posting_details_bottom[0].contents[0].contents[0],
                    closes_in_x,
                    closes_in_type,
                    is_posting_new
                ])

            page_number += 1

            print('Gathering Postings...', len(job_postings) - 1)

            # Bad fix for broken posting count display - DOESNT WORK IF REAL TOTAL IS A MULTIPLE OF 10 - !!!!
            if (len(soup.select('.list-item')) < 10):
                break

        print('TASK:\tBrowser Close')
        browser.close()

        column_colors = ['d4d4d4']
        for posting in job_postings[1:]:
            if posting[10]:
                column_colors.append('6DFA91')
            else:
                column_colors.append('FFFFFF')

        column_sizes = [
            34,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ]

        print('TASK:\tBuild .xlsx File')
        xm.BuildXlsxFile('som_jobs', job_postings, column_colors, column_sizes)