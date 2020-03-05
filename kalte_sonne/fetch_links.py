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

from datetime import date

import feedparser


# Fetch all Kalte Sonne post links in a certain time range.
# Their RSS feed does not provide full post content, so as a preliminary step to scraping we have to fetch all links.
def fetch_links(start_time, end_time):
    # Open links file
    with open('all_post_links.txt', 'a') as links_file:
        i = 1

        # Iterate over Kalte Sonne pages
        while True:
            print(f'Processing page {i}...')
            feed_page = feedparser.parse(f'https://kaltesonne.de/?feed=rss&paged={i}')

            if len(feed_page['entries']) == 0:
                print('Reached last page.')
                break

            # Iterate over posts in page
            for post in feed_page['entries']:
                post_date = date(post['published_parsed'][0], post['published_parsed'][1], post['published_parsed'][2])

                if end_time > post_date > start_time:
                    # Post date matches, add link to file
                    print(f'Adding new link: {post["link"]}')
                    links_file.write(f'{post["link"]}\n')
                    links_file.flush()
                else:
                    # No more posts in range (including current) -> return
                    return
            i += 1


if __name__ == '__main__':
    # Set time range
    start_time = date(2015, 11, 23)
    end_time = date(2019, 9, 30)
    # Fetch Kalte Sonne links
    fetch_links(start_time, end_time)
