import unicodedata


def strip_accents(text):
    # try:
        text = unicodedata.normalize('NFD', text)\
                .encode('ascii', 'ignore')\
                .decode("utf-8")

        return str(text)
"""
    except Exception as e: # unicode is a default on python 3
        print(f"strip_accents ça fait prout : {e}")
        return e
"""
