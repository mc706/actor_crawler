from typing import List


class Site:
    """
    Site Represenation
    """
    def __init__(self, name: str, domain: str, entry_points: List[str], check_third_party: bool):
        self.name = name
        self.domain = domain
        self.entry_points = entry_points
        self.check_third_party = check_third_party