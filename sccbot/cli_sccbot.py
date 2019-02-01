# coding: utf-8
import click
import register
import data
from settings import Settings

sa_session = data.return_session()
settings = Settings(sa_session, path = "../config/")

@click.group()
def cli():
    """This script showcases different terminal UI helpers in Click."""
    pass


@cli.command()
def list():
    """List Users"""


    user_registerer = register.UserRegisterer(settings)
    users = user_registerer.get_users()
    for u in users:
        print(u)


@cli.command()
def validate():
    """List Users"""

    user_registerer = register.UserRegisterer(settings)
    user_registerer.validate_pending()

if __name__ == "__main__":

    list()
    #validate()