
patterns = (('é', 'i'), ("ä", "a"), ('ü', "u"), ("ì", "n"), ("ï", "n"),
            ("ö", "t"), ("ë", "n"), ("ç", "s"), ("à", "m"), ("ù", "h"),
            ("ÿ", "l"), ("û", "l"), ("Ä", "A"), ("É", "I"), ("Ü", "I"),
            ("Ì", "N"), ("Ï", "N"), ("Ö", "T"), ("Ò", "D"), ("Ë", "N"),
            ("Ç", "S"), ("À", "M"), ("Ù", "H"), ("ß", "L"), ("Å", "Ri"),
            ("å", "ri"), ("è", "rii"), ("ò", "d"), ("ñ", "sh"), ("È", "Ri"),
            ("Ñ", "Sh"), ("™", "'"), ('˜r˚', 'sri'))


unicodes = {
    'A': ['Ā'],
    "a": ['á', 'ã', 'ā', 'ä'],
    "d": ['ḍ', 'ḓ'],
    "D": ['Ḍ', 'Ḍ'],
    'E': ['É'],
    'e': ['ẽ'],
    'f': ['ƒ'],
    "H": ['Ḥ'],
    "h": ['ḥ'],
    'I': ['Í', 'Ī'],
    "i": ['ī', 'ĩ', 'ì'],
    "J": ['Ĵ'],
    "K": ['Ƙ'],
    'k': ['ƙ'],
    'l': ['ḷ'],
    'M': ['Ṁ'],
    "m": ['ṃ', 'ṁ'],
    "N": ['Ṅ', 'Ñ', 'Ṇ'],
    "n": ['ṇ', 'ṅ', 'ñ'],
    "o": ['ᴏ', 'õ', 'ô'],
    'R': ['Ṛ'],
    'r': ['ṝ', 'ṛ'],
    'S': ['Ṣ', 'Ś'],
    's': ['ṣ', 'ś'],
    'T': ['Ṭ'],
    't': ['ṭ'],
    'U': ['Ū'],
    'u': ['ũ'],
    'w': ['ŵ'],
}


def remove_balaram_font(text):
    for pattern in patterns:
        text = text.replace(pattern[0], pattern[1])
    return text


def replace_unicode(text):
    for key in unicodes:
        for letter in unicodes[key]:
            text = text.replace(letter, key)
    return text
