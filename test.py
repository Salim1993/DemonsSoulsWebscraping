from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from pathlib import Path
import requests
import os

from sqlalchemy.exc import IntegrityError

from weapon import Weapon, Base
from database import SessionLocal, engine
from url_data_holder import UrlDataHolder

db = SessionLocal()

Base.metadata.create_all(bind=engine)


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


def handle_table_line(line, weapon_type):
    columns = line.find_all("td")
    name = columns[0].find("a").get_text()
    if check_if_object_exists(name):
        return
    phys = columns[1].find_next("p")
    phys_dam = phys.get_text()
    phys_def = phys.find_next("p").get_text()
    mag = columns[2].find_next("p")
    mag_dam = mag.get_text()
    mag_def = mag.find_next("p").get_text()
    fire = columns[3].find_next("p")
    fire_dam = fire.get_text()
    fire_def = fire.find_next("p").get_text()
    aux = get_aux_values(columns[4])
    aux_dam = aux[0]
    aux_type = aux[1]
    types_string = get_types_string(columns[5])
    strength = get_double_values_from_column(columns[6])
    str_req = strength[0]
    str_bonus = strength[1]
    dex = get_double_values_from_column(columns[7])
    dex_req = dex[0]
    dex_bonus = dex[1]
    faith = get_double_values_from_column(columns[8])
    faith_req = faith[0]
    faith_bonus = faith[1]
    critical_damage = columns[9].find_next("p").get_text()
    grd_brk = columns[10].get_text()
    weight = columns[11].get_text()
    dur = columns[12].get_text()
    loc_string = get_location_string(columns[13])

    weapon = Weapon(name=name, weapon_type=weapon_type, phys_atk=phys_dam, phys_def=phys_def, mag_atk=mag_dam,
                    mag_def=mag_def, fire_atk=fire_dam, fire_def=fire_def, aux_damage=aux_dam, aux_type=aux_type,
                    types_string=types_string, str_req=str_req, str_bonus=str_bonus, dex_req=dex_req,
                    dex_bonus=dex_bonus, faith_req=faith_req, faith_bonus=faith_bonus, critical_damage=critical_damage,
                    guard_break_reduction=grd_brk, weight=weight, durability=dur, location=loc_string)
    print(weapon)
    add_entry(weapon)


def get_aux_values(page_element):
    """
    function to get pair value from columns. Some pages have images to display aux_type,
    while other display type using text

    :param page_element: PageElement from beautiful soup. Contains table columns
    :return: tuple containing damage then type
    """
    have_img = page_element.find("img")
    aux_col_val = page_element.get_text()
    if have_img:
        aux = page_element.find_next("p")
        aux_dam = aux.get_text()
        aux_type = aux.find_next("p").find("img")["title"]
        return aux_dam, aux_type
    elif aux_col_val != "-" and aux_col_val != "":
        aux = page_element.get_text().split(" ")
        aux_dam = aux[1]
        aux_type = aux[0]
        return aux_dam, aux_type
    else:
        return "-", "-"  # default value


def get_location_string(page_element):
    """
    get locations from location column and return in into joined string

    :param page_element: PageElement from beautiful soup. Contains table columns
    :return: String with all the locations joined
    """
    loc_list = page_element.find_all("li")
    loc_list_parsed = map(get_text_from_li_element, loc_list)
    return ",".join(loc_list_parsed)


def get_text_from_li_element(element):
    """
    get text from li, and parses out link info from text

    :param element: li element
    :return: string containing text of list
    """
    link_element = element.find("a")
    if link_element:
        return element.get_text() + link_element.get_text()
    else:
        return element.get_text()


def get_double_values_from_column(page_element):
    """
    function to get pair value from columns. Some pages use pair of <p> tags to separate values.
    while others separate the values using <br>

    :param page_element: PageElement from beautiful soup. Contains table columns
    :return: Tuple of correct pair value in columns
    """
    p_tag = page_element.find("p")
    if p_tag:
        first = p_tag.get_text()
        second = p_tag.find_next("p").get_text()
        return first, second
    else:
        text = page_element.contents
        return text[0], text[3].replace("\xa0", "")


def get_types_string(page_element):
    """
    get types value from type column and return in into joined string

    :param page_element: PageElement from beautiful soup. Contains table columns
    :return: String with all the types joined
    """
    types_list = page_element.find_all("img")
    type_name_list = map(check_if_object_exists, types_list)
    types_string = ""
    if not type_name_list:
        types_string = ",".join(type_name_list)
    return types_string


def check_html_for_title(html):
    if "title" in html:
        return html["title"]
    else:
        return ""


def check_if_object_exists(name):
    return db.query(Weapon).get(name) is not None


def update_object(weapon):
    db.query(Weapon).filter(Weapon.name == weapon.name).update(weapon.create_dict(), synchronize_session=False)


def add_entry(weapon):
    db.add(weapon)
    db.commit()


def download_and_handle_data(url_data_holder):
    """
    take in url for specific weapon data, and download file if non downloaded.
    will then parse through html to add weapon dat from tables

    :param url_data_holder: Contain url, file name, an weapon type
    """
    html_file = check_if_html_file_exists(url_data_holder.file, url_data_holder.url)
    soup = BeautifulSoup(html_file, 'html.parser')
    tables = soup.find_all("tr")
    for line in tables[1:]:
        handle_table_line(line, url_data_holder.weapon_type)
    html_file.close()
    db.close()


def create_url_list():
    dagger_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Daggers", "dagger.html", "dagger")
    straight_sword_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Straight+Swords", "straight_sword.html", "straight sword")
    large_sword_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Large+Swords", "large_sword.html", "large sword")
    very_large_sword_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Very+Large+Swords",
                                         "very_large_sword.html", "very large sword")
    curved_sword_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Curved+Swords", "curved_sword.html", "curved sword")
    katana_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Katanas", "katana.html", "katana")
    thrusting_sword_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Thrusting+Swords", "thrusting_sword.html", "thrusting sword")
    return dagger_url, straight_sword_url, large_sword_url, very_large_sword_url, curved_sword_url, katana_url, thrusting_sword_url


def main():
    data_list = create_url_list()
    for data in data_list:
        download_and_handle_data(data)


if __name__ == "__main__":
    main()
