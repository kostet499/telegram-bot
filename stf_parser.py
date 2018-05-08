import urllib.request
import re


def get_html_doc(url):
    """Open the url and return a string"""
    try:
        response = urllib.request.urlopen(url)
    except ConnectionError:
        return None
    html = str(response.read())
    return html


def get_answer_quantity(html):
    """"Extract the quantity of answers"""
    quest_sum = re.search(r'<h2 data-answercount="[0-9]*">', html)
    try:
        quest_sum = quest_sum.group(0)
    except AttributeError:
        return None
    quest_sum = re.sub(r'h2|[^0-9]', '', quest_sum)
    return quest_sum


def get_answer_id_list(html):
    """Get all answer IDs and return a list of them"""
    matcher = re.findall(r'data-answerid="[0-9]*"', html)
    id_list = list()
    for group in matcher:
        id_list.append(int(re.sub(r'[^0-9]', '', group)))
    return id_list
