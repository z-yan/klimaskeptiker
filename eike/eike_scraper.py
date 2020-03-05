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

import re
from datetime import date

import feedparser


# This class is used to fetch all posts in a certain range from a WordPress blog
class WpScraper:
    # Initialize with blog URL
    def __init__(self, url):
        self.url = url

    # Get all posts in the range between first_date and last_date
    def get_posts_in_range(self, first_date, last_date):
        # Initialize vars
        i = 1
        posts = []

        # Iterate over blog pages. Loop exits on last page.
        while True:
            print(f'Processing page {i}...')

            # Parse next page
            feed_page = feedparser.parse(f'{self.url}/?feed=rss&paged={i}')

            if len(feed_page['entries']) == 0:
                # Last page -> exit
                print('Reached last page or no entries found.')
                return posts

            # Iterate over posts in page
            for post in feed_page['entries']:
                post_date = date(post['published_parsed'][0], post['published_parsed'][1], post['published_parsed'][2])

                if last_date >= post_date >= first_date:
                    # Date matches -> add new post to list
                    print(f'Adding new post: {post["title"]}')
                    posts.append(post)
                else:
                    # Return all posts to this point.
                    return posts

            # Increment page counter.
            i += 1


if __name__ == '__main__':
    # Create scraper instance for EIKE and set date range
    eike_scraper = WpScraper('https://www.eike-klima-energie.eu/category/klima')
    first_date = date(2015, 11, 23)
    last_date = date(2019, 9, 30)

    # Fetch all posts
    all_eike_posts = eike_scraper.get_posts_in_range(first_date, last_date)

    # Regex to remove HTML tags from content
    html_regex = re.compile('<[^<]+?>')

    # Write posts to file
    with open('eike_posts.txt', 'a') as eike_posts_file:
        # Iterate over all posts.
        for index, post in enumerate(all_eike_posts):
            try:
                print(f'Processing post no. {index + 1}/{len(all_eike_posts)}')
                # Remove HTML tags from post content
                eike_posts_file.write(re.sub(html_regex, '', post['content'][0]['value']))
                # Add post separator
                eike_posts_file.write('\n------\n')
                eike_posts_file.flush()
            except KeyError:
                print(f'Skipping post no. {index + 1} (missing key)')
                continue
