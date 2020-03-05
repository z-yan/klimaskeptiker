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

import csv
import random

from wordcloud import WordCloud


# Returns a color function picking a random color from a list
def rand_color_func_generator(colors):
    return lambda *args, **kw: colors[random.randint(0, len(colors) - 1)]


# Different color functions for the two corpora
eike_color_func = rand_color_func_generator(['#392a90', '#68abe5', '#eff601'])
ks_color_func = rand_color_func_generator(['#0f5da7', '#000000', '#f5db00'])


# Parses a CSV file to the format accepted by WordCloud.
def csv_to_score_dict(path):
    result = dict()

    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            score, word = row
            result[word] = int(score)

    return result


# Generate a word cloud from a CSV file with a specified color function.
def gen_wordcloud(in_path, out_path, color_func):
    # Parse CSV data
    score_dict = csv_to_score_dict(in_path)
    # Initialize WordCloud object
    wc = WordCloud(width=2000, height=1000, font_path='./fonts/Roboto-Regular.ttf', mode='RGBA', background_color=None)
    # Generate word cloud from keyness/frequencies
    wc.generate_from_frequencies(score_dict)
    # Apply color function
    wc.recolor(color_func=color_func)
    # Write word cloud to output file
    wc.to_file(out_path)


if __name__ == '__main__':
    # Generate word clouds for both corpora
    gen_wordcloud('./data/Single_Keywords_EIKE_Keyness.csv', 'eike.png', eike_color_func)
    gen_wordcloud('./data/singles_with_keyness_ks.csv', 'ks.png', ks_color_func)
