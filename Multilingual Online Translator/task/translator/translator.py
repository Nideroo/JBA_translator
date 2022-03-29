import argparse
import requests

from bs4 import BeautifulSoup

# Description of program
DESCRIPTION = ("This program translates a word to one or multiple target languages."
               "It also writes the result to a .txt file.")
# Languages keyed numerically
LANGUAGES = ["all",
             "arabic",
             "german",
             "english",
             "spanish",
             "french",
             "hebrew",
             "japanese",
             "dutch",
             "polish",
             "portuguese",
             "romanian",
             "russian",
             "turkish"]
# Newline character for use in f-strings
NEWLINE = "\n"


# Get source language, target language, word from command-line arguments
def get_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("source")  # TODO: UPDATE ERROR CHECKING TO USE CHOICES ARGUMENT
    parser.add_argument("target")
    parser.add_argument("word")
    args = parser.parse_args()
    return args


def write_translations_and_examples(wrd, lang_from, lang_to):
    # Build URL using ReversoContext's structure
    url = f"https://context.reverso.net/translation/{lang_from}-{lang_to}/{wrd}"
    # Identify program as a type of browser
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    # Check if we're good to go
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        # Create or open file to also write output to
        with open(f"{wrd}.txt", "a", encoding="utf-8") as opened_file:
            # Select possible translations of word in target language
            word_translations = [word_translation.text.strip()
                                 for word_translation
                                 in soup.select("#translations-content > .translation")]
            if word_translations:
                print_and_write(f"{lang_to.title()} Translations{NEWLINE}", opened_file)
                # Output possible translations
                print_and_write(f"{f'{NEWLINE}'.join(word_translations)}{NEWLINE}", opened_file)
            else:
                print_and_write(f"{lang_to.title()} Translations NOT FOUND{NEWLINE}", opened_file)

            # Select examples containing word, and their translations
            sentences = [sentence.text.strip()
                         for sentence
                         in soup.select("#examples-content > .example > .ltr")]
            if sentences:
                print_and_write(f"{NEWLINE}{lang_to.title()} Examples{NEWLINE}", opened_file)
                # Output pairs of examples and their translations
                for sentence_from, sentence_to in zip(sentences[::2], sentences[1::2]):
                    print_and_write(f"{sentence_from}{NEWLINE}{sentence_to}{NEWLINE}{NEWLINE}", opened_file)
            else:
                print_and_write(f"{NEWLINE}{lang_to.title()} Examples NOT FOUND{NEWLINE}", opened_file)
    elif r.status_code == 404:
        print(f"Sorry, unable to find {wrd}")
    else:
        print("Something wrong with your internet connection")


def print_and_write(string, file):
    print(string, end="")
    file.write(string)


def main():
    args_to_unpack = get_args()
    language_from, language_to, word = args_to_unpack.source, args_to_unpack.target, args_to_unpack.word
    if language_from not in LANGUAGES:
        print(f"Sorry, the program doesn't support {language_from}")
        return 1
    if language_to not in LANGUAGES:
        print(f"Sorry, the program doesn't support {language_to}")
        return 1
    confirmation = f"You chose \"{language_to.title()}\" as a language to translate \"{word}\"."
    print(confirmation)

    # Print translations and examples for target language, or all languages if chosen
    if language_to == "all":
        LANGUAGES.remove(language_from)
        for language in LANGUAGES[1:]:
            write_translations_and_examples(word, language_from, language)
    else:
        write_translations_and_examples(word, language_from, language_to)


if __name__ == "__main__":
    main()
