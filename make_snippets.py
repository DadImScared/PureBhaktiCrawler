
import re

from remove_words import remove_stop_words


def find_indexes(search, query):
    search_lst = search.lower().split(" ")
    query = remove_stop_words(query.lower().split(" "))
    indexes = []
    for i, e in enumerate(search_lst):
        for word in query:
            if word in e:
                indexes.append(i)
    return indexes


def can_make_snippet(content, query):
    if re.search(query, content):
        return True
    clean_query = remove_stop_words(query.split())
    for word in clean_query:
        if re.findall(word, content):
            return True
    return False


def make_index(content_list, query):
    regex = re.compile(query, re.I)
    index_list = []
    for i, x in enumerate(content_list):
        if re.search(regex, x):
            index_list.append(i)
    return index_list


def sort_indexes(indexes, word_between):
    solo_snippets = []
    groups = []
    group = set()
    for i, num in enumerate(indexes):

        if indexes[-1] is indexes[i]:
            if num not in group:
                solo_snippets.append(num)
            if group:
                groups.append(sorted([item for item in group]))
            break
        if indexes[i+1] - indexes[i] > (word_between*2):
            if group:
                groups.append(sorted([item for item in group]))
            if num not in group:
                solo_snippets.append(num)
            group.clear()

        else:
            group.add(num)
            group.add(indexes[i+1])
    return solo_snippets, groups


def collect_indexes(first_word, last_word, content_lst):
    # list of first word indexes
    f_indexes = set()
    # list of last word indexes
    l_indexes = set()

    for index, word in enumerate(content_lst):
        if first_word.lower() in word.lower() :
            f_indexes.add(index)
        if last_word.lower() in word.lower() :
            l_indexes.add(index)
    return f_indexes, l_indexes


def collect_all_indexes(query, content_lst):
    search_words = remove_stop_words(query.split(" "))
    indexes = set()

    for index, element in enumerate(content_lst):
        for word in search_words:
            if word.lower() in element.lower():
                indexes.add(index)
        # if element.lower() in search_words:
        #     indexes.add(index)
    return sorted([i for i in indexes])


def find_phrase(first_word, last_word, query_len, content_lst):
    f_indexes, l_indexes = collect_indexes(first_word, last_word, content_lst)
    indexes = set()

    for l_index in l_indexes:
        for f_index in f_indexes:
            if (l_index - f_index) == (query_len-1):
                indexes.add(l_index)
    return sorted([i for i in indexes])


def make_snippets(content, query, word_sep=50, display_content=None):
    search_content = content.split(" ")
    content_lst = display_content.split(" ") if display_content else content.split()
    indexes = []
    if len(query.split(" ")) > 1:
        if re.findall(query, content):
            search_words = query.split(" ")
            indexes = find_phrase(search_words[0], search_words[-1], len(search_words), search_content)
        else:
            indexes = collect_all_indexes(query, search_content)

    else:
        indexes = find_indexes(content, query)
    if not indexes:

        return
    solo_snippets, group_snippets = sort_indexes(indexes, word_sep)
    complete_snippets = []
    group_content = []
    search_snippets = []

    for index in solo_snippets:
        if index-word_sep > 0:
            if index < len(content_lst)-word_sep:
                complete_snippets.append(" ".join(content_lst[index - word_sep:index+word_sep]))
                search_snippets.append(" ".join(search_content[index - word_sep:index+word_sep]))
            else:
                complete_snippets.append(" ".join(content_lst[index - word_sep:]))
                search_snippets.append(" ".join(search_content[index - word_sep:]))
        else:
            if index < len(content_lst)-word_sep:
                complete_snippets.append(" ".join(content_lst[:index+word_sep]))
                search_snippets.append(" ".join(search_content[:index+word_sep]))
            else:
                complete_snippets.append(" ".join(content_lst[:index+(len(content_lst)-index)]))
                search_snippets.append(" ".join(search_content[:index+(len(content_lst)-index)]))
            # complete_snippets.append(" ".join(apart[index-50:]))
    for group in group_snippets:
        if group[0]-word_sep > 0:
            if group[-1] < len(content_lst)-word_sep:
                complete_snippets.append(" ".join(content_lst[group[0]-word_sep:group[-1]+word_sep]))
                search_snippets.append(" ".join(search_content[group[0]-word_sep:group[-1]+word_sep]))
            else:
                complete_snippets.append(" ".join(content_lst[group[0]-word_sep:]))
                search_snippets.append(" ".join(search_content[group[0]-word_sep:]))
        else:
            if group[-1] < len(content_lst)-word_sep:
                complete_snippets.append(" ".join(content_lst[:group[-1]+word_sep]))
                search_snippets.append(" ".join(search_content[:group[-1]+word_sep]))
            else:
                complete_snippets.append(" ".join(content_lst[:group[-1]+(len(content_lst)-group[-1])]))
                search_snippets.append(" ".join(search_content[:group[-1]+(len(content_lst)-group[-1])]))

    return complete_snippets, search_snippets
# snippets = make_snippets(apart, 'radha')
# print(len(snippets))
# [print(x) for x in snippets]
