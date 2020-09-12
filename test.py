from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from pathlib import Path
import requests
import os

from meelee_weapon import MeeleeWeapon, Base
from database import SessionLocal, engine
from url_data_holder import UrlDataHolder
from weapon_html_controller import WeaponHtmlController

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

    TODO: at some point this should go into its own class
    """
    print(e)


def handle_table_line(line, weapon_type):
    weapon_controller = WeaponHtmlController(line, weapon_type)
    if check_if_object_exists(weapon_controller.get_name()):
        return
    meelee_weapons = weapon_controller.create_weapon()
    print(meelee_weapons)
    add_entry(meelee_weapons)


def check_if_object_exists(name):
    return db.query(MeeleeWeapon).get(name) is not None


def update_object(meelee_weapons):
    db.query(MeeleeWeapon).filter(MeeleeWeapon.name == meelee_weapons.name).update(meelee_weapons.create_dict(), synchronize_session=False)


def add_entry(meelee_weapons):
    db.add(meelee_weapons)
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
    very_large_sword_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Very+Large+Swords", "very_large_sword.html", "very large sword")
    curved_sword_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Curved+Swords", "curved_sword.html", "curved sword")
    katana_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Katanas", "katana.html", "katana")
    thrusting_sword_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Thrusting+Swords", "thrusting_sword.html", "thrusting sword")
    axes_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Axes", "axe.html", "axe")
    large_axes_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Large+Axes", "large_axe.html", "large axe")
    hammer_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Hammers", "hammer.html", "hammer")
    large_hammer_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Large+Hammers", "large_hammer.html", "large hammer")
    fist_weapon_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Fist+Weapons", "fist_weapon.html", "fist weapon")
    spear_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Spears", "spear.html", "spear")
    polearm_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Polearms", "polearm.html", "polearm")
    # bows_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Bows", "bow.html", "bow")
    # crossbows_url = UrlDataHolder("https://demonssouls.wiki.fextralife.com/Crossbows", "crossbow.html", "crossbow")
    return (dagger_url, straight_sword_url, large_sword_url, very_large_sword_url, curved_sword_url, katana_url, thrusting_sword_url,
            axes_url, large_axes_url, hammer_url, large_hammer_url, fist_weapon_url, spear_url, polearm_url)  # , bows_url, crossbows_url)


def main():
    data_list = create_url_list()
    for data in data_list:
        download_and_handle_data(data)


if __name__ == "__main__":
    main()
