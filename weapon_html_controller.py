from meelee_weapon import MeeleeWeapon
from beautiful_soup_controller import BeautifulSoupController


class WeaponHtmlController(BeautifulSoupController):
    """
    WeaponHtmlController takes PageElement class from BeautifulSoup containing table info of weapon values
    we need. It will parse data and create weapon object
    """

    def __init__(self, page_element, weapon_type):
        self.columns = page_element.find_all("td")
        self.weapon_type = weapon_type

    def get_name(self):
        return self.columns[0].find("a").get_text()

    def create_weapon(self):
        name = self.columns[0].find("a").get_text()
        # FUCK the Reaper Scythe
        if name == "Reaper Scythe":
            return self.__return_empty_weapon(name)
        phys = self.get_double_values_from_column(self.columns[1], True, True)
        phys_dam = phys[0]
        phys_def = phys[1]
        mag = self.get_double_values_from_column(self.columns[2], True, True)
        mag_dam = mag[0]
        mag_def = mag[1]
        fire = self.get_double_values_from_column(self.columns[3], True, True)
        fire_dam = fire[0]
        fire_def = fire[1]
        aux = self.__get_aux_values(self.columns[4])
        aux_dam = aux[0]
        aux_type = aux[1]
        types_string = self.get_types_string(self.columns[5])
        strength = self.get_double_values_from_column(self.columns[6], True, False)
        str_req = strength[0]
        str_bonus = strength[1]
        dex = self.get_double_values_from_column(self.columns[7], True, False)
        dex_req = dex[0]
        dex_bonus = dex[1]
        faith = self.get_double_values_from_column(self.columns[8], True, False)
        faith_req = faith[0]
        faith_bonus = faith[1]
        critical_damage = self.get_double_values_from_column(self.columns[9], True, False)[0]
        grd_brk = self.columns[10].get_text().strip()
        weight = self.columns[11].get_text().strip()
        dur = self.columns[12].get_text().strip()
        loc_string = self.get_list_of_strings(self.columns[13])

        return MeeleeWeapon(name=name, weapon_type=self.weapon_type, phys_atk=phys_dam, phys_def=phys_def,
                            mag_atk=mag_dam, mag_def=mag_def, fire_atk=fire_dam, fire_def=fire_def, aux_damage=aux_dam,
                            aux_type=aux_type, types_string=types_string, str_req=str_req, str_bonus=str_bonus,
                            dex_req=dex_req, dex_bonus=dex_bonus, faith_req=faith_req, faith_bonus=faith_bonus,
                            critical_damage=critical_damage,
                            guard_break_reduction=grd_brk, weight=weight, durability=dur, location=loc_string)

    def __get_aux_values(self, page_element):
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
        elif aux_col_val != "-" and aux_col_val != "" and aux_col_val != ' -':
            aux = page_element.get_text().split(" ")
            aux_dam = aux[1]
            aux_type = aux[0]
            return aux_dam, aux_type
        else:
            return "-", "-"  # default value

    def __return_empty_weapon(self, name):
        return MeeleeWeapon(name=name, weapon_type=self.weapon_type, phys_atk=0, phys_def=0,
                            mag_atk=0, mag_def=0, fire_atk=0, fire_def=0, aux_damage=0, aux_type="", types_string="",
                            str_req=0, str_bonus="", dex_req=0, dex_bonus="", faith_req=0, faith_bonus="",
                            critical_damage=0, guard_break_reduction=0, weight=0, durability=0, location="")
