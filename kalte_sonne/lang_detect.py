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

from langdetect import DetectorFactory
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0
pattern = re.compile(r"[“„]((.|\n)*?)[“”]")

if __name__ == '__main__':
    # Read scraped data
    with open('scraped_kalte_sonne.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # Initialize iterator
    res_iter = re.finditer(pattern, text)
    # Copy text
    new_text = text
    # Remove all English quotes
    for match in res_iter:
        try:
            if detect(match.group(0)) == 'en':
                new_text = new_text.replace(match.group(0), '')
        except LangDetectException:
            continue
    # Write cleaned data
    with open('cleaned_kalte_sonne.txt', 'w') as new_file:
        new_file.write(new_text)
