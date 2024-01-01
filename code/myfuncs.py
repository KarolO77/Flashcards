import deepl
from settings import ts_api_key
from math import ceil


def display_text(surface, text, pos, font):
    text_surface = font.render(text, True, "#303030")
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)


def adjust_text(word, scale=28):
    if scale * len(word) > 440:
        if "/" in word:
            dcw = word.split("/")
        else:
            dcw = word.split()
        fir_half = " ".join(dcw[: ceil(len(dcw) / 2)])
        sec_half = " ".join(dcw[ceil(len(dcw) / 2) :])
        word = [adjust_text(fir_half, scale), adjust_text(sec_half, scale)]
    else:
        word = [word]

    return word


def extract_phrase(phrase):
    result = []
    for word in phrase:
        if isinstance(word, list):
            result.extend(extract_phrase(word))
        else:
            result.append(word)
    return result


def translate_text(text):
    translator = deepl.Translator(ts_api_key)
    return str(translator.translate_text(text, source_lang="PL", target_lang="EN-GB"))


def check_brackets(text):
    if not (text[-1] == ")" and text[0] == "("):
        return "(" + text + ")"
    else:
        return text
