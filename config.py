""" Config file """

debug_mode = True

# Local files
output_file_path = "results/new_flats.txt"
timestamp_pickle_file = "results/timestamp.pickle"


class SearchLocations:
    """ Available search locations """
    near_ljubljana = "ljubljana-okolica"
    city_ljubljana = "ljubljana-mesto"


class AdTypes:
    """ Available ad types """
    rent = "oglasi-oddaja"
    buy = "oglasi-prodaja"


class RealestateType:
    """ Realestate type """
    apartment = "stanovanje"
    house = "hisa"


class SearchCriteria:
    """ Search criteria """

    # ad type (rent / buy)
    ad_type = AdTypes.rent

    # realestate type (apartment / house)
    realestate_type = RealestateType.apartment

    # search locations
    locations = [
        SearchLocations.near_ljubljana,
        SearchLocations.city_ljubljana
    ]

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
    """ Main data for the email """
    recipients = ['blaz.vrhovec@gmail.com']
    subject = "Scraper nepremicnine.net"
