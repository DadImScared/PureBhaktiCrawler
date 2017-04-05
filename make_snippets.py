
import re


def make_index(content_list, query):
    regex = re.compile(query, re.I)
    index_list = []
    for i, x in enumerate(content_list):
        if re.search(regex, x):
            index_list.append(i)
    return index_list


def sort_indexes(indexes):
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
        if indexes[i+1] - indexes[i] > 100:
            if group:
                groups.append(sorted([item for item in group]))
            if num not in group:
                solo_snippets.append(num)
            group.clear()

        else:
            group.add(num)
            group.add(indexes[i+1])
    return solo_snippets, groups


def make_snippets(content, query):
    content_lst = content.split(" ")
    indexes = make_index(content_lst, query)
    solo_snippets, group_snippets = sort_indexes(indexes)
    complete_snippets = []
    group_content = []
    for index in solo_snippets:
        if index-50 > 0:
            if index < len(content_lst)-50:
                complete_snippets.append(" ".join(content_lst[index - 50:index+50]))
            else:
                complete_snippets.append(" ".join(content_lst[index - 50:]))
        else:
            if index < len(content_lst)-50:
                complete_snippets.append(" ".join(content_lst[:index+50]))
            else:
                complete_snippets.append(" ".join(content_lst[:index+(len(content_lst)-index)]))
            # complete_snippets.append(" ".join(apart[index-50:]))
    for group in group_snippets:
        if group[0]-50 > 0:
            if group[-1] < len(content_lst)-50:
                complete_snippets.append(" ".join(content_lst[group[0]-50:group[-1]+50]))
            else:
                complete_snippets.append(" ".join(content_lst[group[0]-50:]))
        else:
            if group[-1] < len(content_lst)-50:
                complete_snippets.append(" ".join(content_lst[:group[-1]+50]))
            else:
                complete_snippets.append(" ".join(content_lst[:group[-1]+(len(content_lst)-group[-1])]))

    return complete_snippets
# snippets = make_snippets(apart, 'radha')
# print(len(snippets))
# [print(x) for x in snippets]
