# Traditional libs
import time
import requests
import pyperclip
from logzero import logger as lg

# Local files
import tk as tk
import solve_suttom as ss
import word_detection as wd

from selenium_basic import SeleniumBasic

# Selenium
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By


class SeleniumSutom(SeleniumBasic):
    def __init__(self, words_path, humain=False, larousse=False, **kwargs):
        super(SeleniumSutom, self).__init__(**kwargs)
        self.url = "https://sutom.nocle.fr/#"
        self.words_path = words_path
        self.humain = humain
        self.larousse = larousse

    def background_click(self):
        action = ActionBuilder(self.driver)
        action.pointer_action.pointer_down(MouseButton.LEFT)
        action.pointer_action.pointer_up(MouseButton.LEFT)
        action.perform()

    def is_finished(self):
        html = str(self.driver.page_source)
        html = html.replace("</", "<")
        table = html.split("<table>")
        return len(table) < 4

    def extract_table(self):
        html = str(self.driver.page_source)
        html = html.replace("</", "<")
        table = html.split("<table>")[3]
        table = table.replace("<tbody>", "")
        table = table.split("<tr>")
        table = [i for i in table if len(i) > 0]
        return table

    @staticmethod
    def parse_table(table):
        pt = []
        for mot in table:
            if "resultat" in mot:
                mot = mot.split("<td>")
                mot = [i for i in mot if len(i) > 0]
                # print(mot)
                letters = [i[-1] for i in mot]
                rep = [i.split('"')[1].split()[0] for i in mot]
                pt.append((letters, rep))
        return pt

    @staticmethod
    def add_word_to_action(action, word):
        for letter in word:
            action = action.send_keys(letter)
        return action

    def clear_word(self, nb_letters=10):
        action = ActionChains(self.driver)
        for i in range(nb_letters):
            action.send_keys(Keys.BACKSPACE)
        action.perform()

    def try_word(self, word):
        self.clear_word()
        action = ActionChains(self.driver)
        action = self.add_word_to_action(action, word)
        action.send_keys(Keys.ENTER)
        action.perform()

    def extract_hints(self, table):
        indice_initial = table[0].replace("<td>", "")
        self.first_letter = indice_initial[0]
        self.word_size = len(indice_initial)
        lg.info(f"{indice_initial} => {self.first_letter}, {self.word_size}")

    def extract_solution(self):
        time.sleep(2)
        timings = self.driver.execute_script("return window.performance.getEntries();")
        txt = [i["name"] for i in timings if i["name"].endswith(".txt")]
        url = txt[0]
        rep = requests.get(url)
        solution = str(rep.content).replace("b'", "")[:-1]
        self.solution = solution
        # print(">>> Solution found: ", solution)

    @staticmethod
    def parse_rules(pt):
        not_in = []
        lettre_in_not_at = {}
        lettre_at = {}
        lettre_nb = {}
        for comb in pt:
            for nb, (lettre, statut) in enumerate(zip(comb[0], comb[1])):
                # print(nb, lettre, statut)
                lettre = lettre.lower()
                if statut == "non-trouve":
                    not_in.append(lettre)
                if statut == "bien-place":
                    lettre_at[lettre] = nb
                if statut == "mal-place":
                    if lettre in lettre_in_not_at.keys():
                        nbs = lettre_in_not_at[lettre] + [nb]
                        lettre_in_not_at[lettre] = nbs
                    else:
                        lettre_in_not_at[lettre] = [nb]

        # Pour les lettres en doubles
        not_in = list(set(not_in))
        not_in = [i for i in not_in if i not in lettre_at.keys()]
        not_in = [i for i in not_in if i not in lettre_in_not_at.keys()]
        return {
            "not_in": not_in,
            "lettre_in_not_at": lettre_in_not_at,
            "lettre_at": lettre_at,
            "lettre_nb": lettre_nb,
        }

    def extract_results(self):
        time.sleep(1)
        part = self.driver.find_element(by=By.LINK_TEXT, value="Partager")
        part.click()
        self.result = pyperclip.paste()

    def open_stats(self):
        stats_bt = self.driver.find_element(
            by=By.ID, value="configuration-stats-bouton"
        )
        stats_bt.click()

    def solve_sutom(self, words_list, word, clean_word):
        termine = False
        nb = 1
        lists_ = []
        while not termine:
            print("*" * 50)
            print("*", "ESSAI N°", nb, ":", clean_word)
            print("*" * 50)

            # Envoi du mot
            self.try_word(word)
            time.sleep(1)
            self.background_click()
            time.sleep(3)

            termine = self.is_finished()
            if termine:
                print("GAGNE")
                break

            # Analyse du résultat
            table = self.extract_table()
            pt = self.parse_table(table)
            rules = self.parse_rules(pt)

            # Affichage des nouvelles règles
            print("Nouvelles règles:")
            _ = [print("-", k, ":", v) for k, v in rules.items()]

            # Selection du nouveau mot
            words_list = ss.filter_macro(words_list, rules)
            print(len(words_list), "matching words.")
            lists_.append(words_list)

            nb_limit = 40
            if self.larousse and len(words_list) < nb_limit and len(words_list) > 1:
                self.larousse = False
                print(
                    "Remaining only",
                    len(words_list),
                    f"=> Less than {nb_limit} =>Larousse check",
                )
                bad, good = wd.filter_larousse(words_list)
                print("- bad :", len(bad))
                print("- good:", len(good))
                words_list = good

            rep = None
            nb_limit = 20
            if self.humain and len(words_list) <= nb_limit and len(words_list) > 1:
                rep = tk.inter(words_list)
                print(rep)

            if rep is None or rep == "__automatix__":
                clean_word, new_word = wd.get_new_word(words_list)
            else:
                clean_word, new_word = rep, wd.conv_letters(rep)
            print(clean_word)

            word = new_word

            if nb == 6:
                termine = True
                print("Perdu")
            nb += 1

    def run(self):
    
        if not self.check_driver():
            lg.error("Pas de driver. Pas de SUTOM.")
            return True

        url = self.url
        self.connect_to_url(url)
        self.background_click()

        table = self.extract_table()
        self.extract_hints(table)
        

        # Chargement des mots correspondants
        words_list = ss.filter_corpus(
            self.words_path, self.first_letter.lower(), self.word_size
        )

        # Sélection du mot initial
        clean_word, initial_word = wd.get_initial_word(words_list)
        print(clean_word)

        word = initial_word

        self.solve_sutom(words_list, word, clean_word)
        self.extract_results()
        print(self.result)

    def run_hack(self):

        url = self.url
        self.connect_to_url(url)
        self.background_click()        
        self.extract_solution()
        self.try_word(wd.conv_letters(self.solution))



if __name__ == "__main__":

    words_path = "../data/mots.txt"
    chromedriver = "../chromedriver"
    
    sutom = SeleniumSutom(driver_path=chromedriver, words_path=words_path)
    sutom.run()
    sutom.close_driver()
