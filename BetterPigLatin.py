"""
The purpose of this program is to translate English phrases into Pig Latin. 
The program is intended to only 
work with the English language, which rarely (if ever) includes any letters with accents, 
and if they do, it is typically acceptable to not write them. 
The program does account for punctuation, such as quotation marks and periods, 
as well as capitalization. 
"""


def main():
    string = input("What is the phrase you would like to translate into Pig Latin? ")
    print(pig_latin(string))


def pig_latin(string):
    sentence = string.split()  # splits the sentence into a list
    vowels = ["a", "e", "i", "o", "u", "y"]  # vowel list; referred to to declare omit_first_letter
    allowed_symbols = vowels + ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                                'v', 'w', 'x', 'z']
    for i in range(len(allowed_symbols)):
        allowed_symbols += allowed_symbols[i].upper()
    # allowed_symbols is the English alphabet

    exception_v = ['opossum']
    # list of words where the first letter is a vowel, but starts with a consonant
    exception_c = ['honest', 'honestly', 'honesty', 'honor', 'honorary', 'honorific', 'honorly', 'hour', 'hourly',
                   'honorably']
    # list of words where the first consonant is not pronounced
    exception_y = []  # this will have any words that begin with "y"

    pigphrase = []
    # this will have the final sentence in list form

    for i, word in enumerate(sentence):  # pigs every word (word) in sentence
        qu = False  # is the first letter qu?
        omit_first_letter = False  # is the first letter a vowel?

        first_cluster = []  # the consonant cluster being moved to the end
        cluster_length = 0  # the length of the cluster
        list_w_uncased = listify(word)  # converts word into a list

        extra_symbols = generate_extra_symbols(list_w_uncased, allowed_symbols)
        # generates lists to store forbidden symbols

        list_w = listify(stringify(list_w_uncased).lower())
        # essentially makes a new variable that is list_w_uncased w/
        # lowercase letters, free of extra symbols

        # adds the word to list of Y-exceptions if the word begins with a Y
        if list_w[0] == 'y' and word not in ['yggdrasil', 'yttrium']:
            exception_y.append(word)  # makes it so I don't have to add all the y words

        # sets omit bool to true if the word begins with a vowel sound
        if list_w[0] in vowels or word in exception_c:
            omit_first_letter = True

        # fills in the first_cluster and cluster_height variables
        purified_word = stringify(list_w)  # this is used to check if the word is in the exception lists
        if purified_word not in exception_c:

            # exception for exception_v
            if purified_word in exception_v:
                omit_first_letter = False
                while list_w[cluster_length] in vowels:
                    first_cluster += list_w[cluster_length]
                    cluster_length += 1

            count = 0
            while list_w[cluster_length] not in vowels or word in exception_y:
                if list_w[cluster_length] in allowed_symbols:
                    first_cluster += list_w[cluster_length]

                if list_w[cluster_length].lower() == "q" and list_w[cluster_length + 1].lower() == "u":
                    first_cluster += list_w[cluster_length + 1]
                    qu = True
                    # makes an exception for "qu" at the beginning of words

                cluster_length += 1
                if word in exception_y:
                    exception_y.remove(word)  # this makes it so there's no recursion
                    count = 1
            if count == 1:
                exception_y.append(word)  # adds the word back into the list for later ref

        pig = pigify(list_w, cluster_length, first_cluster, qu, extra_symbols[0])

        # this converts every index that was capitalized back to being
        # capitalized
        capital_indices = []
        count = 0
        for j in range(len(list_w_uncased)):
            if list_w_uncased[j].isupper():
                capital_indices.append(j)
                pig[i + len(extra_symbols[0])] = pig[j + len(extra_symbols[0])].upper()

        last_letter_is_upper = False
        if pig[len(pig) - 1].isupper():  # if the last letter is uppercase:
            last_letter_is_upper = True

        count = 0
        if omit_first_letter:
            pig += "y"
            count += 1
            if word in exception_y:
                pig.pop(len(pig) - 1)
                count -= 1
        count += 2
        pig += "a", "y"
        # adds the (y)ay to the end of the word

        if last_letter_is_upper:
            for j in range(count):
                pig[len(pig) - j - 1] = pig[len(pig) - j - 1].upper()

        pig += extra_symbols[1]

        pigphrase.append(stringify(pig))
        # adds pig as a string to pigphrase

    pigphrase = stringify(pigphrase, True)
    # turns list pigphrase into a sentence
    return pigphrase


def listify(string):  # deconstructs a string into individual characters and spits it out in list form
    listy = []
    for _, letter in enumerate(string):
        listy += letter
    return listy


def stringify(alist, wants_spaces=False):  # turns a list into a string
    string = ""
    for _, j in enumerate(alist):
        string += str(j)
        if wants_spaces: # originally had another method that turned into a sentence; this satisfies that
            string += " "
    # adds a string version of each element in a list to var string
    return string


def generate_extra_symbols(alist, allowed_symbols):
    extra_symbols_b = []  # list for any extra beginning symbols
    count = 0
    if alist[count] not in allowed_symbols:
        while alist[count] not in allowed_symbols:
            extra_symbols_b.append(alist[count])
            alist.pop(count)
    # removes any extra beginning symbols and saves them for later

    extra_symbols_e = []  # list for any final symbols
    count = len(alist) - 1
    if alist[count] not in allowed_symbols:
        while alist[count] not in allowed_symbols:
            extra_symbols_e.insert(0, alist[count])
            alist.pop(count)
            count -= 1
    # removes any extra final symbols and saves them for later

    return extra_symbols_b, extra_symbols_e


def pigify(list_w, cluster_length, first_cluster, qu, extra_symbols):
    pig = list_w  # declares a value "pig" that will be added to the phrase later

    # converts the first letters of the word to the last letters
    for i in range(len(list_w) - cluster_length):
        pig[i] = list_w[i + cluster_length]

    # removes the repeat last letters
    for _ in range(cluster_length):
        pig.pop(len(pig) - 1)
    # these two for-loops effectively remove the first consonant cluster

    pig = listify(extra_symbols) + pig
    # adds any extra symbols from the beginning of the word back

    pig += first_cluster
    # this adds said first cluster to the end

    if qu:
        pig.remove("u")

    return pig


if __name__ == '__main__':
    main()
