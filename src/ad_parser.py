from bs4 import element

from src.file_handler import append_to_file


class Ad:
    def __init__(self, ad_tag: element.Tag):
        self.parse_error_occurred = False
        self.ad_tag = ad_tag

        self.size_value, self.size_unit = self.get_size()
        self.agency = self.get_agency()
        self.price, self.price_value, self.price_unit = self.get_price()
        self.location = self.get_location()
        self.hyperlink = self.get_hyperlink()
        self.description = self.get_description()

    def get_size(self):
        try:
            main_data = self.ad_tag.find("div", {"class": "main-data"})

            size_tag = main_data.find("span", {"class": "velikost"})

            size = size_tag.contents[0]
            size_split = size.split(" ")

            size_value = float(size_split[0].replace(",", "."))
            size_unit = size_split[-1]
        except Exception as err:
            print(err)
            self.parse_error_occurred = True
            size_value = 0
            size_unit = ""

        return size_value, size_unit

    def get_price(self):
        try:
            main_data = self.ad_tag.find("div", {"class": "main-data"})

            price_tag = main_data.find("span", {"class": "cena"})
            price = price_tag.contents[0]

            price_tag_meta = main_data.find("meta", {"itemprop": "price"})
            if price_tag_meta is None:
                price_tag_meta = main_data.find("meta", {"itemqrop": "price"})

            price_value = float(price_tag_meta["content"])

            price_unit_tag_meta = main_data.find("meta", {"itemprop": "priceCurrency"})
            if price_unit_tag_meta is None:
                price_unit_tag_meta = main_data.find("meta", {"itemqrop": "priceCurrency"})

            price_unit = price_unit_tag_meta["content"]
        except Exception as err:
            print(err)
            self.parse_error_occurred = True
            price = ""
            price_value = 0
            price_unit = ""

        return price, price_value, price_unit

    def get_agency(self):
        try:
            main_data = self.ad_tag.find("div", {"class": "main-data"})

            agency_tag = main_data.find("span", {"class": "agencija"})

            agency = agency_tag.contents[0]
        except Exception as err:
            print(err)
            self.parse_error_occurred = True
            agency = ""

        return agency

    def get_location(self):
        try:
            title_tag = self.ad_tag.find("h2", {"itemprop": "name"})
            if title_tag is None:
                title_tag = self.ad_tag.find("h2", {"itemqrop": "name"})

            location_tag = title_tag.find("span", {"class": "title"})
            location = location_tag.contents[0]
        except Exception as err:
            print(err)
            self.parse_error_occurred = True
            location = ""

        return location

    def get_hyperlink(self):
        try:
            title_tag = self.ad_tag.find("h2", {"itemprop": "name"})
            if title_tag is None:
                title_tag = self.ad_tag.find("h2", {"itemqrop": "name"})

            link_tag = title_tag.find("a")
            link = "https://www.nepremicnine.net" + link_tag["href"]
        except Exception as err:
            print(err)
            self.parse_error_occurred = True
            link = ""

        return link

    def get_description(self):
        try:
            description_tag = self.ad_tag.find("div", {"class": "kratek_container"}).find("div", {"class": "kratek"})
            description = description_tag.contents[0]
        except Exception as err:
            print(err)
            self.parse_error_occurred = True
            description = ""

        return description

    def fits_criteria(self, min_price: float = 0, max_price: float = 99999999, min_size: float = 0,
                      max_size: float = 99999999) -> bool:
        if self.price_value < min_price or self.price_value > max_price:
            return False

        if self.size_value < min_size or self.size_value > max_price:
            return False

        return True

    def get_printable_string(self, extra_new_lines: bool = False) -> str:
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
            return "\n" + print_str + "\n"
        else:
            return print_str

    def print(self):
        print(self.get_printable_string())

    def write_to_file(self, file_path: str):
        append_to_file(file_path, self.get_printable_string(extra_new_lines=True))
