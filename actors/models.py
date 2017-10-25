from typing import List


class Site:
    """
    Site Represenation
    """

    def __init__(self, key: str, name: str, domain: str, entry_points: List[str], check_third_party: bool,
                 screen_shot: bool):
        self.key = key
        self.name = name
        self.domain = domain
        self.entry_points = set(entry_points)
        self.check_third_party = check_third_party
        self.screen_shot = screen_shot

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Site: <" + str(self.__dict__) + '>'
