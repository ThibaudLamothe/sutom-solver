import sys ; sys.path.append("./src")
from src.selenium_sutom import SeleniumSutom

# Définition des chemins
words_path = "data/mots.txt"
chromedriver = "./chromedriver"

# Standard
sutom = SeleniumSutom(driver_path=chromedriver, words_path=words_path)
sutom.run()
sutom.close_driver()
