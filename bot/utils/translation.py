import logging

translations = {
    "ru": {

    }
}


def _(text, lang="uz"):
    if lang == "uz":
        return text
    global translations
    try:
        return translations[lang][text]
    except Exception as err:
        logging.error(err)
