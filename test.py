from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from pathlib import Path
import requests
import os

from weapon import Weapon


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def save_html(url, path):
    fp = requests.get(url, headers={'User-Agent': 'test'})
    with open(path, "w", encoding="utf-8") as fo:
        fo.write(fp.text)


def load_html(path):
    return open(path, 'rb')


def check_if_html_file_exists(path, url):
    path_to_dir = os.path.dirname(__file__)
    absolute_path = os.path.join(path_to_dir, path)
    my_file = Path(absolute_path)
    if not my_file.is_file():
        save_html(url, path)
    return load_html(path)


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. This function just prints them, but you can make it do anything.
    """
    print(e)


def handle_table_line(line):
    columns = line.find_all("td")
    name = columns[0].find("a").get_text()
    phys = columns[1].find_next("p")
    phys_dam = phys.get_text()
    phys_def = phys.find_next("p").get_text()
    mag = columns[2].find_next("p")
    mag_dam = mag.get_text()
    mag_def = mag.find_next("p").get_text()
    fire = columns[3].find_next("p")
    fire_dam = fire.get_text()
    fire_def = fire.find_next("p").get_text()
    aux_type = "-"
    aux_dam = "-"
    aux_col_val = columns[4].get_text()
    if aux_col_val != "-" and aux_col_val != "":
        aux = columns[4].find_next("p")
        aux_dam = aux.get_text()
        aux_type = aux.find_next("p").find("img")["title"]
    types_list = columns[5].find_all("img")
    type_name_list = map(lambda x: x["title"], types_list)
    types_string = ",".join(type_name_list)
    strength = columns[6].find_next("p")
    str_req = strength.get_text()
    str_bonus = strength.find_next("p").get_text()
    dex = columns[7].find_next("p")
    dex_req = dex.get_text()
    dex_bonus = dex.find_next("p").get_text()
    faith = columns[8].find_next("p")
    faith_req = faith.get_text()
    faith_bonus = faith.find_next("p").get_text()
    critical_damage = columns[9].find_next("p").get_text()
    grd_brk = columns[10].get_text()
    weight = columns[11].get_text()
    dur = columns[12].get_text()
    loc_list = columns[13].find_all("li")
    loc_list_parsed = map(lambda x: x.get_text() + x.find("a").get_text(), loc_list)
    loc_string = ",".join(loc_list_parsed)

    dagger = Weapon("Dagger", name, phys_dam, phys_def, mag_dam, mag_def, fire_dam, fire_def, aux_dam, aux_type,
                    types_string, str_req, str_bonus, dex_req, dex_bonus, faith_req, faith_bonus, critical_damage,
                    grd_brk, weight, dur, loc_string)
    print(dagger)


def main():
    html_file = check_if_html_file_exists("dagger.html", "https://demonssouls.wiki.fextralife.com/Daggers")
    soup = BeautifulSoup(html_file, 'html.parser')
    tables = soup.find_all("tr")
    for line in tables[1:]:
        handle_table_line(line)
    html_file.close()


if __name__ == "__main__":
    main()
