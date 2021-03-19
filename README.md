# Scraper - nepremicnine.net
- Python scraper for apartments and houses.
    - https://www.nepremicnine.net/


## Requirements
1. Clone repo
1. `pip install -r requirements.txt`
1. Add `config_mail_auth.py` to root folder
    - This file holds credentials for email authentication
    ```python
    gmail_user = 'user@gmail.com'
    gmail_password = 'password'
    ```
1. Set your Gmail account to support less secure applications
    - https://myaccount.google.com/security
    - Turn on `Less secure app access`
    - This is a requirement if you want to access your Gmail account from Python
1. Configure settings in [config.py](config.py) to your linking
1. Run main.py
1. You can edit [Scraper.bat](tools/Scraper.bat) for automated script runs with venv

## Results
- Results will be saved to `results.txt` in [results](results) folder
    - Text is not pretty yet - feel free to upgrade it
    - Single result example:
    ```
    NOVE FUŽINE
    54.0 m2
    600,00 €/mesec
    600.0 EUR
    Zasebna ponudba
    54 m2, 2-sobno, zgrajeno l. 1986, adaptirano l. 2010, 12/12 nad., Oddam sodobno opremljeno 2-sobno stanovanje na Novih F...
    https://www.nepremicnine.net/oglasi-oddaja/nove-fuzine-stanovanje_6395101/
    ```
- Additionally `timestamp.piclkle` is generated in same folder each time you run the scraper
    - Next run will check last timestamp and scrap only in time window from that date
    - You can turn this off in [config.py](config.py) and always scrap in a constant time window
        - `force_time_window = True`
        - `time_window_days = 7`
        