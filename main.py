from datetime import datetime, timedelta

from config import locations, Criteria, output_file_path, Email, timestamp_pickle_file
from src.web_request import get_ad_list
from src.ad_parser import Ad
from src.file_handler import clear_file, append_to_file, get_file_content, write_to_pickle, read_pickle
from src.send_email import send_email


def scrap():
    clear_file(output_file_path)

    now = datetime.now()
    now_str = now.strftime("%d.%m.%Y - %H:%M:%S")
    append_to_file(output_file_path, now_str + "\n")

    if Criteria.force_previous_days:
        scrap_day_window = Criteria.check_previous_days
    else:
        try:
            last_scrap_timestamp = read_pickle(timestamp_pickle_file)
        except:
            last_scrap_timestamp = datetime.now() - timedelta(days=Criteria.check_previous_days)

        date_dif = datetime.now() - last_scrap_timestamp
        scrap_day_window = date_dif.days
        if date_dif.seconds > 5 * 60 * 60 or scrap_day_window == 0:
            scrap_day_window += 1

    append_to_file(output_file_path, f"Results for last {scrap_day_window} days" + "\n")

    for location in locations:
        text = "\n" + "-" * 20 + "\n" + location.upper() + "\n" + "-" * 20 + "\n"
        append_to_file(output_file_path, text)

        url = f"https://www.nepremicnine.net/oglasi-oddaja/{location}/stanovanje/"
        params = f"last={scrap_day_window}&s=16"  # How many days ago do we check

        ad_list = get_ad_list(url, params)

        for ad_tag in ad_list:
            ad = Ad(ad_tag)
            fits_criteria = ad.fits_criteria(
                min_size=Criteria.min_size,
                max_size=Criteria.max_size,
                min_price=Criteria.min_price,
                max_price=Criteria.max_price
            )
            if fits_criteria:
                ad.print()
                ad.write_to_file(output_file_path)

    write_to_pickle(timestamp_pickle_file, datetime.now())


if __name__ == "__main__":
    scrap()

    email_subject = Email.subject + " - " + datetime.now().strftime("%d.%m.%Y %H:%M")
    email_body = get_file_content(output_file_path)
    send_email(
        recipients=Email.recipients,
        subject=email_subject,
        body=email_body
    )
