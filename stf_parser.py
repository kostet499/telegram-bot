import urllib.request
import re


def get_html_doc(url):
    response = urllib.request.urlopen(url)
    html = str(response.read())
    return html


def get_answer_quantity(html):
    quest_sum = re.search(r'<h2 data-answercount="[0-9]*">', html)
    try:
        quest_sum = quest_sum.group(0)
    except AttributeError:
        print('No answercount tag found')
    quest_sum = re.sub(r'h2|[^0-9]', '', quest_sum)
    return quest_sum


print(get_answer_quantity
      (get_html_doc('https://ru.stackoverflow.com/questions/825215/')))
