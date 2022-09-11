import argparse
import sys

sys.path.append("./src")
from src.selenium_sutom import SeleniumSutom


def is_humain():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-hm",
        "--humain",
        help="Une iade humaine peut elle intervenir sur la sélection finale.",
        action='store_true',
    )
    args = parser.parse_args()
    return args.humain


# Définition des chemins
words_path = "data/mots.txt"
chromedriver = "./chromedriver"

# Standard
sutom = SeleniumSutom(
    driver_path=chromedriver, words_path=words_path, humain=is_humain()
)
sutom.run()
sutom.close_driver()
