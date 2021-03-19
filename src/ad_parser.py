""" Ad Container """
from bs4 import element

from src.file_handler import append_to_file


class Ad:
    """ Ad container """

    def __init__(self, ad_tag: element.Tag):
        self.ad_tag = ad_tag

        self.parse_error_occurred = False
        self.parse_errors = []

        self.size_value, self.size_unit = self.get_size()
        self.agency = self.get_agency()
        self.price, self.price_value, self.price_unit = self.get_price()
        self.location = self.get_location()
        self.hyperlink = self.get_hyperlink()
        self.description = self.get_description()

    def get_size(self) -> tuple:
        """
        Parse apartment size value and unit
        :return: tuple (value: float, unit: string)
        """
        try:
            main_data = self.ad_tag.find("div", {"class": "main-data"})

            size_tag = main_data.find("span", {"class": "velikost"})
            size = size_tag.contents[0]
            size_split = size.split(" ")

            size_value = float(size_split[0].replace(",", "."))
            size_unit = size_split[-1]
        except Exception as err:
            self.parse_errors.append(err)
            self.parse_error_occurred = True
            size_value = 0
            size_unit = ""

        return size_value, size_unit

    def get_price(self) -> tuple:
        """
        Parse apartment price
        :return: tuple (price: string, value: float, currency: string)
        """
        try:
            main_data = self.ad_tag.find("div", {"class": "main-data"})

            # Price as string
            price_tag = main_data.find("span", {"class": "cena"})
            price = price_tag.contents[0]

            # Price value
            price_tag_meta = main_data.find("meta", {"itemprop": "price"})

            # Sometimes there is a type in attribute name (itemprop -> itemqrop)
            if price_tag_meta is None:
                price_tag_meta = main_data.find("meta", {"itemqrop": "price"})

            price_value = float(price_tag_meta["content"])

            # Price currency
            price_currency_tag_meta = main_data.find("meta", {"itemprop": "priceCurrency"})

            # Sometimes there is a type in attribute name (itemprop -> itemqrop)
            if price_currency_tag_meta is None:
                price_currency_tag_meta = main_data.find("meta", {"itemqrop": "priceCurrency"})

            price_currency = price_currency_tag_meta["content"]
        except Exception as err:
            self.parse_errors.append(err)
            self.parse_error_occurred = True
            price = ""
            price_value = 0
            price_currency = ""

        return price, price_value, price_currency

    def get_agency(self) -> str:
        """
        Parse seller agency
        :return: str
        """
        try:
            main_data = self.ad_tag.find("div", {"class": "main-data"})

            agency_tag = main_data.find("span", {"class": "agencija"})

            agency = agency_tag.contents[0]
        except Exception as err:
            self.parse_errors.append(err)
            self.parse_error_occurred = True
            agency = ""

        return agency

    def get_location(self) -> str:
        """
        Parse apartment location
        :return: str
        """
        try:
            title_tag = self.ad_tag.find("h2", {"itemprop": "name"})

            # Sometimes there is a type in attribute name (itemprop -> itemqrop)
            if title_tag is None:
                title_tag = self.ad_tag.find("h2", {"itemqrop": "name"})

            location_tag = title_tag.find("span", {"class": "title"})
            location = location_tag.contents[0]
        except Exception as err:
            self.parse_errors.append(err)
            self.parse_error_occurred = True
            location = ""

        return location

    def get_hyperlink(self) -> str:
        """
        Parse ad hyperlink
        :return: str
        """
        try:
            title_tag = self.ad_tag.find("h2", {"itemprop": "name"})

            # Sometimes there is a type in attribute name (itemprop -> itemqrop)
            if title_tag is None:
                title_tag = self.ad_tag.find("h2", {"itemqrop": "name"})

            link_tag = title_tag.find("a")
            link = "https://www.nepremicnine.net" + link_tag["href"]
        except Exception as err:
            self.parse_errors.append(err)
            self.parse_error_occurred = True
            link = ""

        return link

    def get_description(self) -> str:
        """
        Parse ad description
        :return: str
        """
        try:
            description_tag = self.ad_tag.find("div", {"class": "kratek_container"}).find("div", {"class": "kratek"})
            description = description_tag.contents[0]
        except Exception as err:
            self.parse_errors.append(err)
            self.parse_error_occurred = True
            description = ""

        return description

    def fits_criteria(self, min_price: float = 0, max_price: float = 99999999, min_size: float = 0,
                      max_size: float = 99999999) -> bool:
        """
        Check if ad fits passed criteria
        :param min_price: float
        :param max_price: float
        :param min_size: float
        :param max_size: float
        :return: bool
        """
        if self.price_value < min_price or self.price_value > max_price:
            return False

        if self.size_value < min_size or self.size_value > max_size:
            return False

        return True

    def get_printable_string(self, extra_new_lines: bool = False) -> str:
        """
        Generate printable string
        :param extra_new_lines: bool: extra new line before and after the string
        :return: str: data about the ad
        """
        print_str = ""
        print_str += self.location + "\n"
        print_str += str(self.size_value) + " " + self.size_unit + "\n"
        print_str += self.price + "\n"
        print_str += str(self.price_value) + " " + self.price_unit + "\n"
        print_str += self.agency + "\n"
        print_str += self.description + "\n"
        print_str += self.hyperlink + "\n"
        print_str += "-" * 100

        if extra_new_lines:
            print_str = "\n" + print_str + "\n"

        return print_str

    def print(self) -> None:
        """
        Print ad to console
        :return: None
        """
        print(self.get_printable_string())

    def append_to_file(self, file_path: str) -> None:
        """
        Write ad to a file - append method
        :param file_path: str: path to file
        :return: None
        """
        append_to_file(file_path, self.get_printable_string(extra_new_lines=True))
