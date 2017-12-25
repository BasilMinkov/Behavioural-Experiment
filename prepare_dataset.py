"""This code is used to prepare data to run an experiment with expyriment package"""

import os


def split_after_point(phrase):
    n = phrase.count(".")
    if n > 1:
        index = phrase.find(".")
        return phrase[:index + 1], phrase[index + 2:-1]
    else:
        index = phrase.find(":")
        return phrase[:index + 1], phrase[index + 2:-1]


def prepare_instruction():
    with open(os.path.join(os.getcwd(), "static", "instruction.txt"), "r", encoding='utf-8') as text:
        return text.read()


def prepare_phrases():
    phrases = {}
    counter = -1  # phrase identifier

    with open(os.path.join(os.getcwd(), "static", "stimuli", "text", "phrases.txt"), "r", encoding='utf-8') as text:

        #  Iterate through file lines
        lines = text.readlines()
        for i in range(len(lines) - 1):
            phrase = lines[i]

            #  Check whether line is suitable for being phrases.
            if phrase.find("•") != -1:
                counter += 1
                for sign in ["•", "\n", "\t", "«", "»"]:
                    phrase = phrase.replace(sign, "")

                # Make two phrases. First – to be presented at once. Second – to be presented by words.
                phrase1, phrase2 = split_after_point(phrase)

                # Check whether there is a question after a phrase, testing probationer attention.
                question = lines[i + 1]
                if question.find("Да / Нет") != -1:
                    for sign in ["(", ")", "\n", "\t"]:
                        question = question.replace(sign, "")
                    phrases.update({counter: [phrase1, phrase2, question]})
                else:
                    phrases.update({counter: [phrase1, phrase2, None]})

    return phrases
