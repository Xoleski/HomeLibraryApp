import re
import unicodedata

from transliterate import translit

__all__ = [
    "slugify",
]


def slugify(value, allow_unicode=False):
    # Transliterate Cyrillic to Latin
    value = translit(value, 'ru', reversed=True)

    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
