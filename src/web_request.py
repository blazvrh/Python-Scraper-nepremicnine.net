import requests
from bs4 import BeautifulSoup


def get_ad_list(url: str, params: str = "") -> list:
    ads = []
    for i in range(1, 20):
        url_paged = url + f"{i}/?{params}"
        response = requests.get(url_paged)

        parsed_response = BeautifulSoup(response.text, "html.parser")

        ad_list = parsed_response.find("div", {"class": "seznam"})
        # print(ad_list)
        page_ads = ad_list.find_all("div", {"class": "oglas_container"})

        if len(page_ads) == 0:
            break
        ads += page_ads

    return ads


if __name__ == "__main__":
    print(type(get_ad_list()[0]))
