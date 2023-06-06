# TODO

from cs50 import get_string


def main():
    Text = get_string("Text: ")
    # letters
    l = count_letters(Text)
    # words
    w = count_words(Text)
    # sentences
    s = count_sentences(Text)
    # putting it all together
    L = (l * 100) / (w + 1)
    S = (s * 100) / (w + 1)
    Grade = round(0.0588 * L - 0.296 * S - 15.8)

    # if the grade number is less than 1
    if Grade < 1:
        print("Before Grade 1")
    # if the grade number is 16 of higher
    elif Grade >= 16:
        print("Grade 16+")
    # if the grade number is between 1 and 16, round the grade number to the nearest int
    else:
        print(f"Grade {Grade}")


# count letters
def count_letters(Text):
    letters = 0
    for i in range(len(Text)):
        if (Text[i].isalpha()):
            letters += 1
    return letters


# count words
def count_words(Text):
    word = Text.count(" ")
    return word


# count sentences
def count_sentences(Text):

    aa = Text.count('.')
    cc = Text.count('!')
    bb = Text.count('?')

    sentences = int(aa + cc + bb)
    return sentences


main()