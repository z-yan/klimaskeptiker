#  MIT License
#
#  Copyright (c) 2020 Betani Slavova, Zdravko Yanakiev
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # Open post links file
    with open('all_post_links.txt', 'r') as post_links_file:
        post_links = post_links_file.readlines()

    print('Opened links file.')

    # Open scraped posts file
    with open('scraped_kalte_sonne.txt', 'a') as scraped_ks:
        print('Opened scraped posts file.')

        # Iterate over all post links
        for index, post_link in enumerate(post_links):
            print(f'Processing link {post_link} ({index}/{len(post_links)})')
            # Fetch post HTML page
            r = requests.get(post_link)
            # Parse HTML
            soup = BeautifulSoup(r.text, 'html.parser')

            try:
                # Get post content by CSS selector
                content = soup.select('div.entry-content[itemprop="text"]')[0].text
                print('Writing content to file.')
                scraped_ks.write(content)
                # Write post separator
                scraped_ks.write('\n------\n')
                scraped_ks.flush()
            except:
                # Continue if scraping fails
                print('Failed scraping content from link.')
                continue
