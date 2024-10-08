from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = 'https://www.governmentjobs.com/careers/michigan?department[0]=State%20Police&department[1]=Technology%2C%20Management%20and%20Budget&sort=PositionTitle%7CAscending'


# import nest_asyncio;
# nest_asyncio.apply()

# pw = sync_playwright.start()

# chrome = pw.chromium.launch(headless=False)

# page = chrome.new_page()

# page.goto(url)


with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    page.goto(url)

    page.wait_for_selector(".job-table-title")

    print(page.content())

    soup = BeautifulSoup(page.content())
    parsed = []
    for item in soup.select(".tw-tower div[data-target]"):
        parsed.append({
            'title': item.select_one('h3').text,
            'url': item.select_one('.tw-link::attr(href)').attrs.get("href"),
            'username': item.select_one('.tw-link').text,
            'tags': [tag.text for tag in item.select('.tw-tag')],
            'viewers': item.select_one('.tw-media-card-stat').text,
        })
