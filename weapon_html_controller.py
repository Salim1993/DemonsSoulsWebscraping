from weapon import Weapon


class WeaponHtmlController:
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
        phys = self.columns[1].find_next("p")
        phys_dam = phys.get_text()
        phys_def = phys.find_next("p").get_text()
        mag = self.columns[2].find_next("p")
        mag_dam = mag.get_text()
        mag_def = mag.find_next("p").get_text()
        fire = self.columns[3].find_next("p")
        fire_dam = fire.get_text()
        fire_def = fire.find_next("p").get_text()
        aux = self.__get_aux_values(self.columns[4])
        aux_dam = aux[0]
        aux_type = aux[1]
        types_string = self.__get_types_string(self.columns[5])
        strength = self.__get_double_values_from_column(self.columns[6])
        str_req = strength[0]
        str_bonus = strength[1]
        dex = self.__get_double_values_from_column(self.columns[7])
        dex_req = dex[0]
        dex_bonus = dex[1]
        faith = self.__get_double_values_from_column(self.columns[8])
        faith_req = faith[0]
        faith_bonus = faith[1]
        critical_damage = self.columns[9].find_next("p").get_text()
        grd_brk = self.columns[10].get_text()
        weight = self.columns[11].get_text()
        dur = self.columns[12].get_text()
        loc_string = self.__get_location_string(self.columns[13])

        return Weapon(name=name, weapon_type=self.weapon_type, phys_atk=phys_dam, phys_def=phys_def, mag_atk=mag_dam,
                      mag_def=mag_def, fire_atk=fire_dam, fire_def=fire_def, aux_damage=aux_dam, aux_type=aux_type,
                      types_string=types_string, str_req=str_req, str_bonus=str_bonus, dex_req=dex_req,
                      dex_bonus=dex_bonus, faith_req=faith_req, faith_bonus=faith_bonus,
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
        elif aux_col_val != "-" and aux_col_val != "":
            aux = page_element.get_text().split(" ")
            aux_dam = aux[1]
            aux_type = aux[0]
            return aux_dam, aux_type
        else:
            return "-", "-"  # default value

    def __get_location_string(self, page_element):
        """
        get locations from location column and return in into joined string

        :param page_element: PageElement from beautiful soup. Contains table columns
        :return: String with all the locations joined
        """
        loc_list = page_element.find_all("li")
        loc_list_parsed = map(self.__get_text_from_li_element, loc_list)
        return ",".join(loc_list_parsed)

    def __get_text_from_li_element(self, element):
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

    def __get_double_values_from_column(self, page_element):
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

    def __get_types_string(self, page_element):
        """
        get types value from type column and return in into joined string

        :param page_element: PageElement from beautiful soup. Contains table columns
        :return: String with all the types joined
        """
        types_list = page_element.find_all("img")
        type_name_list = map(self.__check_html_for_title, types_list)
        types_string = ""
        if not type_name_list:
            types_string = ",".join(type_name_list)
        return types_string

    def __check_html_for_title(self, html):
        if "title" in html:
            return html["title"]
        else:
            return ""
