
from stop_words import get_stop_words

# gets list of stop words. Example [a, about, above , after]
stop_words = get_stop_words('en')
cap_words = [word[0].upper() + word[1:] for word in stop_words]
full_words = stop_words + cap_words


def remove_stop_words(text_lst):
    # empty list to add words that aren't stop words
    new_text_lst = []

    # iterate over text list with all words
    for word in text_lst:
        # filter happens here. If the word is not in the list of stop words
        # append to new text list without stop words
        if word not in full_words:
            new_text_lst.append(word)

    return new_text_lst
