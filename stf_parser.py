import urllib.request
import urllib.error
import re


def get_html_doc(url):
    """Open the url and return a string"""
    try:
        response = urllib.request.urlopen(url)
    except ConnectionError:
        return None
    except urllib.error.HTTPError:
        return None
    html = str(response.read())
    return html


def get_answer_quantity(html, is_link):
    """"Extract the quantity of answers"""
    if is_link:
        html = get_html_doc(html)
        if html is None:
            return None
    quest_sum = re.search(r'<h2 data-answercount="([0-9]*)">', html)
    try:
        return int(quest_sum.group(1))
    except AttributeError:
        return None


def get_answer_id_list(html):
    """Get all answer IDs and return a list of them"""
    matcher = re.findall(r'data-answerid="[0-9]*"', html)
    id_list = list()
    for group in matcher:
        id_list.append(int(re.sub(r'[^0-9]', '', group)))
    return id_list
