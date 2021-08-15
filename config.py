""" Config file """

debug_mode = True

# Local files
output_file_path = "results/results.txt"
pickle_file_path = "results/saved_data.pickle"


class SearchLocations:
    """ Available search locations """
    near_ljubljana = "ljubljana-okolica"
    city_ljubljana = "ljubljana-mesto"
    gorenjska = "gorenjska"
    south_primoirska = "juzna-primorska"
    north_primorska = "severna-primorska"
    notranjska = "notranjska"
    savinjska = "savinjska"
    podravska = "podravska"
    koroska = "koroska"
    dolenjska = "dolenjska"
    posavska = "posavska"
    zasavska = "zasavska"
    pomurska = "pomurska"


class AdTypes:
    """ Available ad types """
    i_want_to_rent = "oglasi-oddaja"
    i_am_renting = "oglasi-najem"
    i_am_buying = "oglasi-prodaja"
    i_am_selling = "oglasi-nakup"


class RealestateType:
    """ Realestate type """
    apartment = "stanovanje"
    house = "hisa"
    weekend_facility = "vikend"
    land = "posest"
    office = "poslovni-prostor"
    garage = "garaza"
    holiday_facility = "pocitniski-objekt"


class SearchCriteria:
    """ Search criteria """

    # ad type (rent / buy)
    ad_type = AdTypes.i_want_to_rent

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

    # True -> always check last check_previous_days;
    # False -> Scrap just the difference from previous scrap
    force_time_window = False

    # How many days in the past do we check for new ads
    time_window_days = 7


class Email:
    """ Main data for the email """
    recipients = ['blaz.vrhovec@gmail.com']
    subject = "Scraper nepremicnine.net"
