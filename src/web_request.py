import requests
from bs4 import BeautifulSoup


def get_ad_list(url: str, params: str = "") -> list:
    """
    Returns a list of ads in html format
    :param url: str
    :param params: str
    :return: list[bs4.element.Tag]
    """
    ads = []

    # check first 200 pages
    for i in range(1, 200):
        url_paged = url + f"{i}/?{params}"
        response = requests.get(url_paged)

        parsed_response = BeautifulSoup(response.text, "html.parser")

        ad_list = parsed_response.find("div", {"class": "seznam"})

        if ad_list is None:
            return ads

        page_ads = ad_list.find_all("div", {"class": "oglas_container"})

        if len(page_ads) == 0:
            break

        ads += page_ads

    return ads
