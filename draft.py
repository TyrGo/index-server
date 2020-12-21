from os import replace
import re
import pdfplumber
from rangify import rangify

def get_entries(words):
    byte_entries = words.read().splitlines()
    entries = [entry.decode('utf-8') for entry in byte_entries]
    entries = sorted(entries, key=str.casefold)              
    print(f"lines to index {entries}")
    return entries


def list_entries(entries):
    entries_list = []

    for line in entries:
        words = re.split(', |, |: |\+', line)
        for word in words:
            if word not in index_words:
                index_words.append(word)

    return entries_list


def find_words(ms, entries)list):
    found_words = {}

    with pdfplumber.open(ms) as pdf:
        all_pages = len(pdf.pages)

        for num in range(all_pages):
            print(f'processing page {num}')
            pg_num = pdf.pages[num]
            pg_words_case = pg_num.extract_text(x_tolerance=1)
            pg_words_case = re.findall(r'[\w]+', pg_words_case)
            pg_words = [word.lower().lstrip('\n') for word in pg_words_case]
            pg_words = ' '.join(pg_words_case).lower()

            for word in entries_list:
                word = word.replace('9', 'ti').replace(';', 'tio').replace(
                    '^', 'tt').replace('ﬀ', 'ff').replace('ﬁ', 'fi').replace(
                    'ﬃ', 'ffi')
                word_joined = ' '.join(word.split(' ')).lower()

                if word_joined.lower().lstrip() in pg_words:
                    print(f'~~~~~found: {word}')

                    if word not in found_words:
                        found_words[word] = []
                    found_words[word].append(pg_num.page_number)

    return found_words


def make_index(entries, found_words,)
    index = 'Index \n'

    for line in entries:
        new_line = ''
        words = re.split(', |, |: |\+', line)
        print(f"first---${words}")
        subs = words[1:]            # do this only if words len > 0?
        subs = sorted(subs, key=str.casefold)
        words = [words[0]] + subs

        for word in words:
            if word in found_words:
                word = f'{word} {found_words[word]}'
            new_line += f'{word}; '
            print(f"creating index for {word}")

        new_line = new_line[:-2]
        index = f"{index}\n" + new_line

    return index


def generator(ms, words):
    entries = get_entries(words)
    entries_list = list_entries(entries)
    found_words = find_words(ms, entries_list)

    for word in found_words:
        found_words[word] = rangify(found_words[word])

    index = make_index(entries, found_words)

    index_file = open("index.txt", "a")
    index_file.write(index)

    index_file.close()

# from os import replace
# import re
# import pdfplumber
# from rangify import rangify


# def generator(ms, words):
#     byte_entries = words.read().splitlines()
#     byte_entries.reverse()
#     entries = [entry.decode('utf-8') for entry in byte_entries]
#     print(f"words to index {entries}")

#     index_words = []
#     word_pages = {}
#     index = ''

#     for line in entries:
#         words = re.split(', |, |: |\+', line)
#         for word in words:
#             if word not in index_words:
#                 index_words.append(word)

#     # index words now is a list of all words (entries and subentries);

#     with pdfplumber.open(ms) as pdf:
#         all_pages = len(pdf.pages)

#         for num in range(all_pages):
#             print(f'processing page {num}')

#             pg_num = pdf.pages[num]
#             pg_words_case = pg_num.extract_text(x_tolerance=3)
#             pg_words_case = re.findall(r'[\w]+', pg_words_case)
#             pg_words = [word.lower().lstrip('\n') for word in pg_words_case]
#             pg_words = ' '.join(pg_words_case).lower()

#             for word in index_words:
#                 word = word.replace('9', 'ti').replace(
#                     ';', 'tio').replace('^', 'tt').replace('ﬀ', 'ff')
#                 word_joined = ' '.join(word.split(' ')).lower()

#                 if word_joined.lower().lstrip() in pg_words:
#                     print(f'~~~~~found: {word}')

#                     if word not in word_pages:
#                         word_pages[word] = []
#                     word_pages[word].append(pg_num.page_number)

#     # # word_pages is now a dictionary of all the words and their pages

#     for word in word_pages:
#         word_pages[word] = rangify(word_pages[word])

#     # word_pages now has neat page ranges

#     for line in entries:
#         new_line = ''
#         words = re.split(', |, |: |\+', line)

#         for word in words:
#             if word in word_pages:
#                 word = f'{word} {word_pages[word]}'
#             new_line += f'{word}; '
#             print(f"creating index for {word}")

#         index = f"{new_line} \n" + index

#     # now we have a nice index!

#     index_file = open("index.txt", "a")
#     index_file.write(index)

#     index_file.close()




# TODOS:
# range neatly as 102-7


# import pdfplumber
# from rangify import rangify


# def generator(ms, words):
#     # fileObj = open(words, "r")
#     byte_entries = words.read().splitlines()
#     byte_entries.reverse()
#     entries = [entry.decode('utf-8') for entry in byte_entries]
#     print(f"words to index {entries}")
#     # fileObj.close()

#     index = {}

#     with pdfplumber.open(ms) as pdf:
#         all_pages = len(pdf.pages)

#         for num in range(all_pages):
#             pg_num = pdf.pages[num]
#             pg_words_case = pg_num.extract_text(x_tolerance=3).split(' ')
#             pg_words = [word.lower().lstrip('\n') for word in pg_words_case]
#             print(f"processing {pg_num}")

#             for word in entries:
#                 if word.lower().lstrip() in pg_words:
#                     print(f"~~~~~found word {word}")

#                     if word not in index:
#                         index[word] = []
#                     index[word].append(pg_num.page_number)

#     indext = open("index.txt", "a")

#     for entry in index:
#         pages = rangify(index[entry])
#         indext.write(f'{entry}: {pages}\n')
#         print(f"creating index for {entry} at {pages}")

#     indext.close()
    
#     return indext

# # TODOS:
# # Handle 'Smith, John', 'Smith, J.P.'
# # Order index with subentries
# # range neatly as 102-7

# from os import replace
# import re
# import pdfplumber
# from rangify import rangify


# def generator(ms, words):
#     byte_entries = words.read().splitlines()
#     entries = [entry.decode('utf-8') for entry in byte_entries]
#     entries = sorted(entries, key=str.casefold)              
#     print(f"lines to index {entries}")

#     index_words = []
#     word_pages = {}
#     index = 'Index \n'

#     for line in entries:
#         words = re.split(', |, |: |\+', line)
#         for word in words:
#             if word not in index_words:
#                 index_words.append(word)

#     # index words now is a list of all words (entries and subentries);

#     with pdfplumber.open(ms) as pdf:
#         all_pages = len(pdf.pages)

#         for num in range(all_pages):
#             print(f'processing page {num}')

#             pg_num = pdf.pages[num]
#             pg_words_case = pg_num.extract_text(x_tolerance=1)
#             pg_words_case = re.findall(r'[\w]+', pg_words_case)
#             pg_words = [word.lower().lstrip('\n') for word in pg_words_case]
#             pg_words = ' '.join(pg_words_case).lower()
#             # print(f"woooords ${pg_words}")

#             for word in index_words:
#                 word = word.replace('9', 'ti').replace(';', 'tio').replace(
#                     '^', 'tt').replace('ﬀ', 'ff').replace('ﬁ', 'fi').replace(
#                     'ﬃ', 'ffi')
#                 word_joined = ' '.join(word.split(' ')).lower()

#                 if word_joined.lower().lstrip() in pg_words:
#                     print(f'~~~~~found: {word}')

#                     if word not in word_pages:
#                         word_pages[word] = []
#                     word_pages[word].append(pg_num.page_number)

#     # # word_pages is now a dictionary of all the words and their pages

#     for word in word_pages:
#         word_pages[word] = rangify(word_pages[word])

#     # word_pages now has neat page ranges

#     for line in entries:
#         new_line = ''
#         words = re.split(', |, |: |\+', line)
#         print(f"first---${words}")
#         subs = words[1:]            # do this only if words len > 0?
#         subs = sorted(subs, key=str.casefold)
#         words = [words[0]] + subs

#         for word in words:
#             if word in word_pages:
#                 word = f'{word} {word_pages[word]}'
#             new_line += f'{word}; '
#             print(f"creating index for {word}")

#         new_line = new_line[:-2]
#         index = f"{index}\n" + new_line

#     # now we have a nice index!

#     index_file = open("index.txt", "a")
#     index_file.write(index)

#     index_file.close()

# # from os import replace
# # import re
# # import pdfplumber
# # from rangify import rangify


# # def generator(ms, words):
# #     byte_entries = words.read().splitlines()
# #     byte_entries.reverse()
# #     entries = [entry.decode('utf-8') for entry in byte_entries]
# #     print(f"words to index {entries}")

# #     index_words = []
# #     word_pages = {}
# #     index = ''

# #     for line in entries:
# #         words = re.split(', |, |: |\+', line)
# #         for word in words:
# #             if word not in index_words:
# #                 index_words.append(word)

# #     # index words now is a list of all words (entries and subentries);

# #     with pdfplumber.open(ms) as pdf:
# #         all_pages = len(pdf.pages)

# #         for num in range(all_pages):
# #             print(f'processing page {num}')

# #             pg_num = pdf.pages[num]
# #             pg_words_case = pg_num.extract_text(x_tolerance=3)
# #             pg_words_case = re.findall(r'[\w]+', pg_words_case)
# #             pg_words = [word.lower().lstrip('\n') for word in pg_words_case]
# #             pg_words = ' '.join(pg_words_case).lower()

# #             for word in index_words:
# #                 word = word.replace('9', 'ti').replace(
# #                     ';', 'tio').replace('^', 'tt').replace('ﬀ', 'ff')
# #                 word_joined = ' '.join(word.split(' ')).lower()

# #                 if word_joined.lower().lstrip() in pg_words:
# #                     print(f'~~~~~found: {word}')

# #                     if word not in word_pages:
# #                         word_pages[word] = []
# #                     word_pages[word].append(pg_num.page_number)

# #     # # word_pages is now a dictionary of all the words and their pages

# #     for word in word_pages:
# #         word_pages[word] = rangify(word_pages[word])

# #     # word_pages now has neat page ranges

# #     for line in entries:
# #         new_line = ''
# #         words = re.split(', |, |: |\+', line)

# #         for word in words:
# #             if word in word_pages:
# #                 word = f'{word} {word_pages[word]}'
# #             new_line += f'{word}; '
# #             print(f"creating index for {word}")

# #         index = f"{new_line} \n" + index

# #     # now we have a nice index!

# #     index_file = open("index.txt", "a")
# #     index_file.write(index)

# #     index_file.close()




# # TODOS:
# # range neatly as 102-7


# # import pdfplumber
# # from rangify import rangify


# # def generator(ms, words):
# #     # fileObj = open(words, "r")
# #     byte_entries = words.read().splitlines()
# #     byte_entries.reverse()
# #     entries = [entry.decode('utf-8') for entry in byte_entries]
# #     print(f"words to index {entries}")
# #     # fileObj.close()

# #     index = {}

# #     with pdfplumber.open(ms) as pdf:
# #         all_pages = len(pdf.pages)

# #         for num in range(all_pages):
# #             pg_num = pdf.pages[num]
# #             pg_words_case = pg_num.extract_text(x_tolerance=3).split(' ')
# #             pg_words = [word.lower().lstrip('\n') for word in pg_words_case]
# #             print(f"processing {pg_num}")

# #             for word in entries:
# #                 if word.lower().lstrip() in pg_words:
# #                     print(f"~~~~~found word {word}")

# #                     if word not in index:
# #                         index[word] = []
# #                     index[word].append(pg_num.page_number)

# #     indext = open("index.txt", "a")

# #     for entry in index:
# #         pages = rangify(index[entry])
# #         indext.write(f'{entry}: {pages}\n')
# #         print(f"creating index for {entry} at {pages}")

# #     indext.close()
    
# #     return indext

# # # TODOS:
# # # Handle 'Smith, John', 'Smith, J.P.'
# # # Order index with subentries
# # # range neatly as 102-7
