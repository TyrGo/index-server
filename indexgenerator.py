from os import replace
import re
import pdfplumber


def make_index(ms, words):
    entries = get_entries(words)
    entries_list = list_entries(entries)
    found_words = find_words(ms, entries_list)
    print(f"found_words: {found_words}")
    ranged_words = range_words(found_words)
    index = write_index(entries, ranged_words)
    write_file(index)


def get_entries(words):
    byte_entries = words.read().splitlines()
    lines = [entry.decode('utf-8') for entry in byte_entries]
    # better: get more e.g. ' ' with regex
    not_empties = [line for line in lines if line != '']
    entries = sorted(not_empties, key=str.casefold)
    print(f"lines to index: {entries}")
    return entries


def list_entries(entries):
    entries_list = []

    for line in entries:
        words = re.split(', |, |: |\+', line)
        for word in words:
            if word not in entries_list:
                entries_list.append(word)

    # maybe do some other formatting around here?, also remove hypthen ?
    entries_list = remove_ligatures(entries_list)
    return entries_list


def remove_ligatures(entries_list):  # careful: maybee unecessary but line above and a line below both need tidy words slightly differently
    return [tidy_word(word) for word in entries_list]


def tidy_word(word):  # careful this is used twice in quite different functions, fixing it for one might ruin it for another
    return word.replace('9', 'ti').replace(';', 'tio').replace(
        '^', 'tt').replace('ﬀ', 'ff').replace('ﬁ', 'fi').replace(
            'ﬃ', 'ffi').replace('-', ' ')  # do this neater, last elsewhere?, and add cases, last clause not needed with find_all done right??


def find_words(ms, entries_list):
    found_words = {}

    with pdfplumber.open(ms) as pdf:
        all_pages = len(pdf.pages)

        for num in range(all_pages):
            print(f'processing page {num}')
            pg_num = pdf.pages[num]
            content = pg_num.extract_text(x_tolerance=1)
            pg_words = neat_array(content)

            for word in entries_list:
                entry_words = neat_array(word)
                if entry_present(entry_words, pg_words):
                    print(f'~~~~~found: {word}')

                    if word not in found_words:
                        found_words[word] = []
                    found_words[word].append(pg_num.page_number)

    return found_words


def neat_array(content):
    words = re.findall(r'[\w]+', content)
    words_lowered = [word.lower().lstrip() for word in words]
    return words_lowered


def entry_present(entry_words, pg_words):
    # if not pg_words:  # not sure these lines needed??
    #     return False
    # if not entry_words:
    #     return True
    first, rest = entry_words[0], entry_words[1:]
    pos = 0
    try:
        while True:
            pos = pg_words.index(first, pos) + 1
            if not rest or pg_words[pos:pos+len(rest)] == rest:
                return True
    except ValueError:
        return False


def range_words(found_words):
    for word in found_words:
        found_words[word] = rangify(found_words[word])

    return found_words


def rangify(arr):
    if arr == []:
        return ''

    final_list = []
    ranger = []
    i = 0

    while i < len(arr):
        if ranger != [] and arr[i] != arr[i - 1] + 1:
            if len(ranger) > 1:
                range = f'{ranger[0]}-{ranger[-1]}'
                final_list.append(shorten_range(range))
            else:
                final_list.append(ranger[0])
            ranger = []
        ranger.append(str(arr[i]))
        i += 1

    if len(ranger) == 1:
        final_list.append(str(arr[-1]))
    else:
        range = f'{ranger[0]}-{ranger[-1]}'
        final_list.append(shorten_range(range))

    return ', '.join(final_list)


def shorten_range(range):
    [lefty, righty] = range.split('-')

    if len(lefty) < len(righty):
        return range

    i = 0

    while i < len(righty) and lefty[i] == righty[i]:
        i += 1

    return f"{lefty}-{righty[i:]}"


def write_index(entries, found_words):
    index = 'Index'
    letter = ''

    for line in entries:
        new_line = ''
        words = re.split(', |, |: |\+', line)
        subs = words[1:]            # do this only if words len > 0?
        subs = sorted(subs, key=str.casefold)
        words = [words[0]] + subs

        for word in words:
            # checkthis is all needed?,do this out of loop somehow for betterO?
            check_word = tidy_word(word)
            if check_word in found_words:
                word = f'{word} {found_words[check_word]}'
            new_line += f'{word}; '
            print(f"creating index for {word}")

        new_line = new_line[:-2]
        if new_line[0].lower() != letter:
            index = f"{index}\n"
            letter = new_line[0].lower()
        index = f"{index}\n" + new_line

    return index


def write_file(index):
    index_file = open("index.txt", "a")
    index_file.write(index)
    index_file.close()


# def rangify(arr):
#     if arr == []:
#         return ''

#     final_list = []
#     ranger = []
#     i = 0

#     while i < len(arr):
#         if ranger != [] and arr[i] != arr[i - 1] + 1:
#             if len(ranger) > 1:
#                 final_list.append(f'{ranger[0]}-{ranger[-1]}')
#             else:
#                 final_list.append(ranger[0])
#             ranger = []
#         ranger.append(str(arr[i]))
#         i += 1

#     if len(ranger) == 1:
#         final_list.append(str(arr[-1]))
#     else:
#         final_list.append(f'{ranger[0]}-{ranger[-1]}')

#     return ', '.join(final_list)
