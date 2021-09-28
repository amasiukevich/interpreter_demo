from typing import List


def check_unique_names(list_of_names: List[str]):
    return len(set(list_of_names)) == len(list_of_names)