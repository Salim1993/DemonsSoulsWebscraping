class BeautifulSoupController:

    def get_list_of_strings(self, page_element):
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
        return element.get_text()

    def get_double_values_from_column(self, page_element, replace_number_first, replace_number_second):
        """
        function to get pair value from columns. Some pages use pair of <p> tags to separate values.
        while others separate the values using <br>

        :param page_element: PageElement from beautiful soup. Contains table columns
        :return: Tuple of correct pair value in columns
        """
        list_to_return = ["", ""]
        p_tag = page_element.findChildren("p")
        size_of_children_list = len(p_tag)
        if size_of_children_list == 2:
            list_to_return[0] = p_tag[0].get_text()
            list_to_return[1] = p_tag[1].get_text()
        elif size_of_children_list == 1:
            text = p_tag[0].get_text()
            list_to_return[0] = text[0]
            list_to_return[1] = text[1]
        else:
            text = page_element.contents
            list_to_return[0] = text[0]
            list_to_return[1] = text[3].replace("\xa0", "")
        if replace_number_first and list_to_return[0] == "-":
            list_to_return[0] = 0
        if replace_number_second and list_to_return[1] == "-":
            list_to_return[1] = 0
        return tuple(list_to_return)

    def get_types_string(self, page_element):
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
