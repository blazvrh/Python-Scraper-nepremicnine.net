output_file_path = "results/new_flats.txt"
timestamp_pickle_file = "results/timestamp.pickle"

locations = [
    "ljubljana-okolica",
    "ljubljana-mesto",
]


class Criteria:
    # Price of the apartment EUR
    min_price = 1
    max_price = 700

    # Size of the apartment m2
    min_size = 50
    max_size = 9999999

    # How many days in the past do we check for new ads
    check_previous_days = 7

    # True -> always check last check_previous_days;
    # False -> Scrap just the difference from previous scrap
    force_previous_days = False


class Email:
    recipients = ['blaz.vrhovec@gmail.com']
    subject = "New apartments"
