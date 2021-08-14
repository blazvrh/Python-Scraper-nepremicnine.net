#!venv/Scripts/python
""" Program entry point """
from datetime import datetime, timedelta
from bs4 import element

import config
import src.file_handler as file_handler
from src.web_request import get_ad_list
from src.ad_parser import Ad
from src.send_email import send_email


def scrap() -> None:
    """
    Main scrap function
    :return: None
    """
    file_handler.clear_file(config.output_file_path)

    add_timestamp_to_file()

    scrap_time_window = get_scrap_time_window()  # in days

    file_handler.append_to_file(config.output_file_path, f"Results for last {scrap_time_window} days" + "\n")

    location: str
    for location in config.SearchCriteria.locations:
        append_location_to_file(location)

        url = f"https://www.nepremicnine.net/{config.SearchCriteria.ad_type}/{location}/{config.SearchCriteria.realestate_type}/"
        params = f"last={scrap_time_window}&s=16"  # How many days ago do we check

        ad_list = get_ad_list(url, params)

        ad_tag: element.Tag
        for ad_tag in ad_list:
            ad = Ad(ad_tag)

            if ad_fits_criteria(ad):
                ad.append_to_file(config.output_file_path)

                if config.debug_mode:
                    ad.print()

    file_handler.write_to_pickle(config.timestamp_pickle_file, datetime.now())


def add_timestamp_to_file() -> None:
    """
    Adds timestamp to result file
    :return: None
    """
    now = datetime.now()
    now_str = now.strftime("%d.%m.%Y - %H:%M:%S")
    file_handler.append_to_file(config.output_file_path, now_str + "\n")


def get_scrap_time_window() -> int:
    """
    Checks how many days have passed since last scraping. If data unavailable or
    SearchCriteria.force_previous_days is set to True, SearchCriteria.check_previous_days is returned
    :return: int: days past since last scraping
    """
    if config.SearchCriteria.force_time_window:
        scrap_time_window_days = config.SearchCriteria.time_window_days
    else:
        try:
            last_scrap_timestamp = file_handler.read_pickle(config.timestamp_pickle_file)
        except:
            last_scrap_timestamp = datetime.now() - timedelta(days=config.SearchCriteria.time_window_days)

        date_dif = datetime.now() - last_scrap_timestamp
        scrap_time_window_days = date_dif.days
        if date_dif.seconds > 5 * 60 * 60 or scrap_time_window_days == 0:
            scrap_time_window_days += 1

    return scrap_time_window_days


def append_location_to_file(location: str) -> None:
    """
    Adds a location string to local file (with a few decorations)
    :param location: str
    :return: None
    """
    location_text = "\n" + "-" * 20 + "\n" + location.upper() + "\n" + "-" * 20 + "\n"
    file_handler.append_to_file(config.output_file_path, location_text)


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


if __name__ == "__main__":
    scrap()

    email_subject = config.Email.subject + " - " + datetime.now().strftime("%d.%m.%Y %H:%M")
    email_body = file_handler.get_file_content(config.output_file_path)
    send_email(
        recipients=config.Email.recipients,
        subject=email_subject,
        body=email_body
    )
