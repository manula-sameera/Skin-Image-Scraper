import os
import time
import re
import unittest

import cloudscraper
from bs4 import BeautifulSoup

# Configuration
PATCH_VERSIONS = [
'11-1', '11-2', '11-3', '11-4', '11-5', '11-6', '11-7', '11-8', '11-9', '11-10', '11-11', '11-12', '11-13', '11-14', '11-15', '11-16', '11-17', '11-18', '11-19', '11-20', '11-21', '11-22', '11-23', '11-24', '12-1', '12-2', '12-3', '12-4', '12-5', '12-6', '12-7', '12-8', '12-9', '12-10', '12-11', '12-12', '12-13', '12-14', '12-15', '12-16', '12-17', '12-18', '12-19', '12-20', '12-21','12-22','12-23', '13-1', '13-1b', '13-3', '13-4', '13-5', '13-6', '13-7', '13-8', '13-9', '13-10', '13-11', '13-12', '13-13', '13-14', '13-15', '13-16', '13-17', '13-18', '13-19','13-20','13-21','13-22','13-23','13-24', '14-1', '14-2', '14-3', '14-4', '14-5', '14-6', '14-7', '14-8', '14-9', '14-10', '14-11', '14-12', '14-13', '14-14', '14-15', '14-16', '14-17', '14-18', '14-19','14-20','14-21','14-22','14-23','14-24','25-s1-1','25-s1-2','2025-s1-3','25-04','25-05','25-06','25-07','25-08','25-09'
]
URL_TEMPLATE = 'https://www.leagueoflegends.com/en-us/news/game-updates/patch-{ver}-notes/'
ASSET_DOMAIN = 'https://cmsassets.rgpub.io'
SAVE_DIR = 'skins'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.212 Safari/537.36',
}
IMAGE_HEADERS = {**HEADERS, 'Referer': 'https://www.leagueoflegends.com'}

# Initialize cloudscraper for anti-bot
scraper = cloudscraper.create_scraper()


def fetch_page(url):
    """Fetch page HTML, raising on error."""
    resp = scraper.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.text


def scrape_skins_from_patch(html, patch_ver):
    """
    Extracts (src, filename) tuples for skins section.
    Targets only skins under the summary paragraph (regardless of <p> class).
    """
    soup = BeautifulSoup(html, 'html.parser')
    # find the summary paragraph by its text content
    summary_p = soup.find('p', string=re.compile(r'The following skins will be released', re.I))
    if not summary_p:
        return []
    # the container is the parent that holds skin-boxes
    container = summary_p.parent
    skins = []
    for box in container.select('div.skin-box'):
        # get image link
        a_img = box.select_one('a.skins.cboxElement') or box.select_one('span.content-border a')
        if not a_img:
            continue
        src = a_img.get('href') or a_img.get('src')
        if not src or ASSET_DOMAIN not in src:
            continue
        # extract title for naming
        title_el = box.select_one('.skin-title a')
        title = title_el.get_text(strip=True) if title_el else os.path.splitext(os.path.basename(src))[0]
        # sanitize filename
        name = re.sub(r'[^0-9a-zA-Z]+', '_', title).strip('_').lower()
        filename = f"{patch_ver.replace('.', '_')}_{name}.jpg"
        skins.append((src, filename))
    return skins


def download_image(src, dest_path):
    """Downloads the image to dest_path if not already present."""
    if os.path.exists(dest_path):
        return False
    resp = scraper.get(src, headers=IMAGE_HEADERS, stream=True, timeout=10)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb') as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)
    return True


def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    for ver in PATCH_VERSIONS:
        url = URL_TEMPLATE.format(ver=ver)
        print(f"Fetching patch {ver}: {url}")
        try:
            html = fetch_page(url)
        except Exception as e:
            print(f"  Skipping {ver}: {e}")
            continue
        skins = scrape_skins_from_patch(html, ver)
        if not skins:
            print(f"  No skins found for patch {ver}")
        for src, name in skins:
            path = os.path.join(SAVE_DIR, name)
            if download_image(src, path):
                print(f"  Saved: {path}")
        time.sleep(1)
    print("Done.")


# -- Tests --
class TestSkinScraper(unittest.TestCase):
    def setUp(self):
        # simulate two summary patterns: with or without class
        self.patch_html = '''
        <div>
            <p>The following skins will be released in this patch:</p>
            <div class="gs-container default-2-col">
                <div class="skin-box">
                    <span class="content-border"><a href="https://cmsassets.rgpub.io/img1.jpg" class="skins cboxElement"></a></span>
                    <h4 class="skin-title"><a>Skin One</a></h4>
                </div>
                <div class="skin-box">
                    <span class="content-border"><a href="https://cmsassets.rgpub.io/img2.jpg"></a></span>
                    <h3 class="skin-title"><a>Skin Two</a></h3>
                </div>
            </div>
        </div>'''

    def test_scrape_skins_from_patch(self):
        skins = scrape_skins_from_patch(self.patch_html, '12.7')
        expected = [
            ('https://cmsassets.rgpub.io/img1.jpg', '12_7_skin_one.jpg'),
            ('https://cmsassets.rgpub.io/img2.jpg', '12_7_skin_two.jpg'),
        ]
        self.assertEqual(skins, expected)

if __name__ == '__main__':
    main()
