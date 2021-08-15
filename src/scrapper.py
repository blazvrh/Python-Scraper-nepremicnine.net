""" Scrapper logic """
from datetime import datetime, timedelta
from bs4 import element

import config
import src.file_handler as file_handler
from src.web_request import get_ad_list
from src.ad_parser import Ad

import sys

sys.setrecursionlimit(10000)


class SavedData:
    """
    Data from previous Scraps
    """

    def __init__(self):
        self.saved_data = self.get_saved_data()

        self.scraped_time_window = self.get_scrap_time_window()
        self.saved_ads = self.saved_data["ads"]

    @staticmethod
    def get_saved_data() -> dict:
        """
        Retrieves saved data from pickle file. Creates dictionary if pickle doesnt exist.
        :return: dict: {"ads": dict {hyperlink(str): scrap_timestamp(float)}, "datetime": scrap_timestamp(float)}
        """
        try:
            saved_data = file_handler.read_pickle(config.pickle_file_path)
        except:
            saved_data = {
                "datetime": datetime.now() - timedelta(days=config.SearchCriteria.time_window_days),
                "ads": {}
            }
        return saved_data

    def get_scrap_time_window(self) -> int:
        """
        Checks how many days have passed since last scraping. If data unavailable or
        SearchCriteria.force_previous_days is set to True, SearchCriteria.check_previous_days is returned
        :return: int: days past since last scraping
        """
        if config.SearchCriteria.force_time_window:
            scrap_time_window_days = config.SearchCriteria.time_window_days
        else:
            last_scrap_timestamp = datetime.fromtimestamp(self.saved_data["datetime"])

            date_dif = datetime.now() - last_scrap_timestamp
            scrap_time_window_days = date_dif.days
            if date_dif.seconds > 5 * 60 * 60 or scrap_time_window_days == 0:
                scrap_time_window_days += 1

        return scrap_time_window_days

    def save_current_data(self, scrap_datetime: datetime, new_ads) -> None:
        """
        Saves data to pickle file
        :param scrap_datetime: datetime of current scrap
        :param new_ads: dict: {hyperlink(str): scrap_timestamp(float)}- newly scraped ads
        :return:
        """
        ads_to_save = {hyperlink: ad.scrap_timestamp for (hyperlink, ad) in new_ads.items()}

        for hyperlink, scrap_timestamp in self.saved_ads.items():
            if datetime.fromtimestamp(scrap_timestamp) > scrap_datetime - timedelta(days=7):
                ads_to_save[hyperlink] = scrap_timestamp

        data_to_save = {
            "datetime": scrap_datetime.timestamp(),
            "ads": ads_to_save
        }

        file_handler.write_to_pickle(config.pickle_file_path, data_to_save)

    def is_new_ad(self, ad) -> bool:
        """
        checks if ad is new or already scraped
        :param ad: Ad
        :return: boolean
        """
        return not (ad.hyperlink in self.saved_ads)


def scrap() -> None:
    """
    Main scrap function
    :return: None
    """
    file_handler.clear_file(config.output_file_path)

    add_timestamp_to_file()

    saved_data = SavedData()
    scrap_time_window = saved_data.scraped_time_window  # in days

    file_handler.append_to_file(config.output_file_path, f"Results for last {scrap_time_window} days" + "\n")

    scrap_datetime = datetime.now()
    new_ads: dict
    new_ads = {}

    location: str
    for location in config.SearchCriteria.locations:
        append_location_to_file(location)

        url = f"https://www.nepremicnine.net/{config.SearchCriteria.ad_type}/{location}/{config.SearchCriteria.realestate_type}/"
        params = f"last={scrap_time_window}&s=16"  # How many days ago do we check

        ad_list = get_ad_list(url, params)

        ad_tag: element.Tag
        for ad_tag in ad_list:
            ad = Ad(ad_tag, scrap_datetime.timestamp())

            if ad_fits_criteria(ad) and saved_data.is_new_ad(ad):
                new_ads[ad.hyperlink] = ad
                ad.append_to_file(config.output_file_path)

                if config.debug_mode:
                    ad.print()

    saved_data.save_current_data(scrap_datetime, new_ads)


def append_location_to_file(location: str) -> None:
    """
    Adds a location string to local file (with a few decorations)
    :param location: str
    :return: None
    """
    location_text = "\n" + "-" * 20 + "\n" + location.upper() + "\n" + "-" * 20 + "\n"
    file_handler.append_to_file(config.output_file_path, location_text)


def add_timestamp_to_file() -> None:
    """
    Adds timestamp to result file
    :return: None
    """
    now = datetime.now()
    now_str = now.strftime("%d.%m.%Y - %H:%M:%S")
    file_handler.append_to_file(config.output_file_path, now_str + "\n")


def ad_fits_criteria(ad: Ad) -> bool:
    """
    Checks if ad fits Search criteria
    :param ad: Ad: single Ad object
    :return: bool
    """
    return ad.fits_criteria(
        min_size=config.SearchCriteria.min_size,
        max_size=config.SearchCriteria.max_size,
        min_price=config.SearchCriteria.min_price,
        max_price=config.SearchCriteria.max_price
    )
