#!venv/Scripts/python
""" Program entry point """
from src.scrapper import scrap
from src.send_email import Email

if __name__ == "__main__":
    scrap()

    email = Email()
    email.send_email()
