from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url_host = 'https://www.governmentjobs.com'
url_path = '/careers/michigan?department[0]=State%20Police&department[1]=Technology%2C%20Management%20and%20Budget&sort=PositionTitle%7CAscending&page='
page_number = 1

job_postings = []


def GetPostingsUrlByPage(page):
    return url_host + url_path + str(page)


with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context(viewport={'width': 690, 'height': 740})
    page = context.new_page()


    page.goto(GetPostingsUrlByPage(page_number))
    soup = BeautifulSoup(page.content(), features='html.parser')

    page.wait_for_selector('#job-postings-number')

    # This number is usually wrong but I do not know why !!!!
    total_postings = int(soup.select_one('#job-postings-number').text)
    total_postings_per_page = len(soup.select('.list-item'))

    total_pages = total_postings // total_postings_per_page

    if ((total_postings % total_postings_per_page) > 0):
        total_pages += 1


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

        job_postings.append({
            'is_new': is_posting_new,
            'label': posting.select_one('h3').text.replace('\\n', '').strip(),
            'location': posting_details_top[0].text.replace('\\n', '').strip(),
            'type': posting_details_top[1].contents[0].replace('\\n', '').strip(),
            'pay': posting_details_top[1].contents[2].replace('\\n', '').strip(),
            'category': posting_details_top[2].contents[0].replace('\\n', '').strip(),
            'department': posting_details_top[3].contents[0].replace('\\n', '').strip(),
            'posted_on': posting_details_bottom[0].contents[0].contents,
            'closes_in_x': closes_in_x,
            'closes_in_type': closes_in_type,
            'link': url_host + posting.select_one('h3').select_one('a').get('href')
        })


    for page_number in range(1, total_pages):
        page.goto(GetPostingsUrlByPage(page_number))
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

            job_postings.append({
                'is_new': is_posting_new,
                'label': posting.select_one('h3').text.replace('\\n', '').strip(),
                'location': posting_details_top[0].text.replace('\\n', '').strip(),
                'type': posting_details_top[1].contents[0].replace('\\n', '').strip(),
                'pay': posting_details_top[1].contents[2].replace('\\n', '').strip(),
                'category': posting_details_top[2].contents[0].replace('\\n', '').strip(),
                'department': posting_details_top[3].contents[0].replace('\\n', '').strip(),
                'posted_on': posting_details_bottom[0].contents[0].contents,
                'closes_in_x': closes_in_x,
                'closes_in_type': closes_in_type,
                'link': url_host + posting.select_one('h3').select_one('a').get('href')
            })

        page_number += 1



    print(job_postings)


    browser.close()