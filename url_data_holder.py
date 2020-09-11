class UrlDataHolder:
    """
    Meant to group url of data, file where to save, and weapon type together
    to more easily organize
    """
    def __init__(self, url, file, weapon_type):
        self.url = url
        self.file = file
        self.weapon_type = weapon_type
