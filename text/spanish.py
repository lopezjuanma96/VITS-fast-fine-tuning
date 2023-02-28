""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''


# Regular expression matching whitespace:


import re
#In spanish decimals are marked with commas and dots can be used to mark thousands, so 1k = 1.000 and 1/1k = 0,001
_dotted_number_re = re.compile(r'([0-9][0-9\.]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\,[0-9]+)')
_euros_re = re.compile(r'£([0-9\,]*[0-9]+)')
_pesos_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
#_ordinal_re = re.compile(r'[0-9]+(st|nd|rd|th)') ordinals in spanish are much more complex and are not usually abbreviated
_number_re = re.compile(r'[0-9]+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
    ('sra', 'señora'),
    ('srita', 'señorita'),
    ('sr', 'señor'),
    ('dr', 'doctor'),
    ('doc', 'doctor'),
    ('co', 'compañía'),
    ('jr', 'junior')
]]


# List of (ipa, lazy ipa) pairs is not needed in spanish since phonetics are regular (all letters sounds mostly always the same)


def expand_abbreviations(text):
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text


def collapse_whitespace(text):
    return re.sub(r'\s+', ' ', text)


def _remove_dots(m):
    return m.group(1).replace('.', '')


def _expand_decimal_comma(m):
    return m.group(1).replace(',', ' coma ')


def _expand_pesos(m):
    match = m.group(1)
    parts = match.split('.')
    if len(parts) > 2:
        return match + ' pesos'  # Unexpected format
    pesos = int(parts[0]) if parts[0] else 0
    cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if pesos and cents:
        peso_unit = 'peso' if pesos == 1 else 'pesos'
        cent_unit = 'cent' if cents == 1 else 'cents'
        return '%s %s, %s %s' % (pesos, peso_unit, cents, cent_unit)
    elif pesos:
        peso_unit = 'peso' if pesos == 1 else 'pesos'
        return '%s %s' % (pesos, peso_unit)
    elif cents:
        cent_unit = 'cent' if cents == 1 else 'cents'
        return '%s %s' % (cents, cent_unit)
    else:
        return 'cero pesos'
    
def _expand_euros(m):
    match = m.group(1)
    parts = match.split('.')
    if len(parts) > 2:
        return match + ' euros'  # Unexpected format
    euros = int(parts[0]) if parts[0] else 0
    cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if euros and cents:
        euro_unit = 'euro' if euros == 1 else 'euros'
        cent_unit = 'cent' if cents == 1 else 'cents'
        return '%s %s, %s %s' % (euros, euro_unit, cents, cent_unit)
    elif euros:
        euro_unit = 'euro' if euros == 1 else 'euros'
        return '%s %s' % (euros, euro_unit)
    elif cents:
        cent_unit = 'cent' if cents == 1 else 'cents'
        return '%s %s' % (cents, cent_unit)
    else:
        return 'cero euros'


def _expand_number(m):
    num = int(m.group(0))
    if num > 1000 and num < 3000:
        if num == 2000:
            return 'two thousand'
        elif num > 2000 and num < 2010:
            return 'two thousand ' + _inflect.number_to_words(num % 100)
        elif num % 100 == 0:
            return _inflect.number_to_words(num // 100) + ' hundred'
        else:
            return _inflect.number_to_words(num, andword='', zero='oh', group=2).replace(', ', ' ')
    else:
        return _inflect.number_to_words(num, andword='')


def normalize_numbers(text):
    text = re.sub(_dotted_number_re, _remove_dots, text)
    text = re.sub(_euros_re, _expand_euros, text)
    text = re.sub(_pesos_re, _expand_pesos, text)
    text = re.sub(_decimal_number_re, _expand_decimal_comma, text)
    #text = re.sub(_number_re, _expand_number, text)
    return text


def spanish_to_spanish(text):
    text = text.lower()
    text = expand_abbreviations(text)
    text = normalize_numbers(text)
    text = collapse_whitespace(text)
    return text.replace('...', '…')


if __name__ == "__main__":
    print(spanish_to_spanish('Hola gente, mi nombre es Juan Manuel López y soy lo más importante del mundísimo! Todos me deben $10000 por el trabajo 23,15'))