import pdfplumber
from rangify import rangify


def generator(ms, words):
    # fileObj = open(words, "r")
    byte_entries = words.read().splitlines()
    byte_entries.reverse()
    entries = [entry.decode('utf-8') for entry in byte_entries]
    print(f"words to index {entries}")
    # fileObj.close()

    index = {}

    with pdfplumber.open(ms) as pdf:
        all_pages = len(pdf.pages)

        for num in range(all_pages):
            pg_num = pdf.pages[num]
            pg_words_case = pg_num.extract_text(x_tolerance=3).split(' ')
            pg_words = [word.lower().lstrip('\n') for word in pg_words_case]
            print(f"processing {pg_num}")

            for word in entries:
                if word.lower().lstrip() in pg_words:
                    print(f"~~~~~found word {word}")

                    if word not in index:
                        index[word] = []
                    index[word].append(pg_num.page_number)

    indext = open("index.txt", "a")

    for entry in index:
        pages = rangify(index[entry])
        indext.write(f'{entry}: {pages}\n')
        print(f"creating index for {entry} at {pages}")

    indext.close()
    
    return indext


# TODOS:
# Handle 'Mona Lisa'
# Order index with subentries
# range neatly as 102-7
