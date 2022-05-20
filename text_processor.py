import os
import re
from textwrap import TextWrapper

from util.word_lists import (
    complex_phrases,
    ly_words_not_adverbs,
    passive_voice_pre_words,
    qualifying_words,
    qualifier_linkers,
    sentence_starters,
)
from util.line_format import LineFormat
from util.readability import Readability


STAT = {
    'total_sentences': 0,
    'hard_sentences': 0,
    'very_hard_sentences': 0,
    'adverbs': 0,
    'qualifiers': 0,
    'passive_voice': 0,
    'bad_start': 0,
    'complex': 0,
    'total_letters': 0,
    'total_characters': 0,
    'total_words': 0,
    'total_paragraphs': 0
}


def get_letters_in_sentence(sentence: str) -> list:
    """
    Return a list of letters to get the total number of them per sentence.
    """
    letters_pattern = re.compile(r'[A-Za-z]', re.M)
    return letters_pattern.findall(sentence)


def get_words_in_sentence(sentence: str) -> list:
    """
    Return a list of words to get the total number of them per sentence.
    """
    words_pattern = re.compile(r'[\w\'/-]+', re.M)
    return words_pattern.findall(sentence)


def get_readability(words_in_sentence: int, reading_level: int) -> Readability:
    """
    Calculate the sentence's readability based on the number of words in sentence and reading level.
    """
    if words_in_sentence < 14:
        return Readability.NORMAL
    elif 10 <= reading_level <= 14:
        return Readability.HARD
    elif reading_level > 14:
        return Readability.VERY_HARD
    else:
        return Readability.NORMAL


def get_reading_level(letters_in_sentence: int, words_in_sentence: int) -> int:
    """
    Calculate the reading level of the sentence.
    """
    return round(
        4.71 * (letters_in_sentence / words_in_sentence)
        + 0.5 * words_in_sentence
        - 21.43
    )


def highlight(sentence: str, text_to_highlight: str, readability: Readability, line_format: str) -> str:
    """
    Apply formatting to the sentence's combination of words (or the whole sentence) based on its readability level.
    """
    if readability is not Readability.NORMAL:
        sentence = sentence.replace(
            text_to_highlight,
            f'{LineFormat.map(LineFormat.ENDC, to="symbol")}'
            f'{LineFormat.map(line_format, to="symbol")}{text_to_highlight}'
            f'{LineFormat.map(LineFormat.ENDC, to="symbol")}'
            f'{LineFormat.map(LineFormat.YELLOW if readability is Readability.HARD else LineFormat.RED, to="symbol")}'
        )
    else:
        sentence = sentence.replace(
            text_to_highlight,
            f'{LineFormat.map(line_format, to="symbol")}'
            f'{text_to_highlight}'
            f'{LineFormat.map(LineFormat.ENDC, to="symbol")}'
        )
    return sentence


def process_sentence(sentence: str) -> str:
    """
    Calculate statistics for the incoming sentence, apply coloring based on readability
    """
    letters_in_sentence = get_letters_in_sentence(sentence)
    number_of_letters = len(letters_in_sentence)
    words_in_sentence = get_words_in_sentence(sentence)
    number_of_words = len(words_in_sentence)

    STAT['total_letters'] += number_of_letters
    STAT['total_words'] += number_of_words
    STAT['total_characters'] += len(sentence)

    reading_level = get_reading_level(number_of_letters, number_of_words)
    readability = get_readability(number_of_words, reading_level)

    # READABILITY COLORING
    if readability is Readability.HARD:
        STAT['hard_sentences'] += 1
        sentence = (
            f'{LineFormat.map(LineFormat.YELLOW, to="symbol")}'
            f'{sentence}'
            f'{LineFormat.map(LineFormat.ENDC, to="symbol")}'
        )
    elif readability is Readability.VERY_HARD:
        STAT['very_hard_sentences'] += 1
        sentence = (
            f'{LineFormat.map(LineFormat.RED, to="symbol")}'
            f'{sentence}'
            f'{LineFormat.map(LineFormat.ENDC, to="symbol")}'
        )

    for i, word in enumerate(words_in_sentence):
        # ADVERBS COLORING
        if word.lower().endswith('ly') and word.lower() not in ly_words_not_adverbs:
            STAT['adverbs'] += 1
            sentence = highlight(sentence, word, readability, LineFormat.CYAN)

        # QUALIFYING WORDS COLORING
        elif word.lower() in qualifying_words:
            phrase_to_highlight = ''
            # if the word is in the list of qualifying words, we need to check it
            if qualifying_words[word.lower()]:
                # if the previous word is a linker (was, were, don't, will)
                if i > 0 and words_in_sentence[i - 1].lower() in qualifier_linkers:
                    # if there was a pronoun before
                    if i > 1 and words_in_sentence[i - 2].lower() in qualifying_words[word.lower()]:
                        phrase_to_highlight = f'{words_in_sentence[i - 2]} {words_in_sentence[i - 1]} {word}'
                # if the previous word is a pronoun
                elif i > 0 and words_in_sentence[i - 1].lower() in qualifying_words[word.lower()]:
                    phrase_to_highlight = f'{words_in_sentence[i - 1]} {word}'
            else:
                phrase_to_highlight = f'{word}'

            if phrase_to_highlight:
                STAT['qualifiers'] += 1
                sentence = highlight(sentence, phrase_to_highlight, readability, LineFormat.CYAN)

        # PASSIVE VOICE COLORING
        if word.lower().endswith('ed') and words_in_sentence[i - 1].lower() in passive_voice_pre_words:
            STAT['passive_voice'] += 1
            phrase_to_highlight = f'{words_in_sentence[i - 1]} {word}'
            sentence = highlight(sentence, phrase_to_highlight, readability, LineFormat.GREEN)

    # COMPLEX WORDS
    for complex_phrase in complex_phrases:
        if complex_phrase in sentence:
            STAT['complex'] += 1
            sentence = highlight(sentence, complex_phrase, readability, LineFormat.PURPLE)

    # SENTENCE STARTERS
    for sentence_starter in sentence_starters:
        if sentence.startswith(sentence_starter):
            STAT['bad_start'] += 1
            sentence = highlight(sentence, sentence_starter, readability, LineFormat.GREEN)

    return sentence


def get_sentences(paragraph: str) -> list:
    """
    Split the paragraph into sentences to process them.
    """
    sentence_pattern = re.compile(r'([A-Z][^\\.!?]*[\\.!?])', re.M)
    sentences = sentence_pattern.findall(paragraph)
    return sentences if sentences else [paragraph]


def process_paragraph(paragraph: str) -> str:
    """
    Process single paragraph from the text.
    """
    processed_paragraph = ''
    sentences = get_sentences(paragraph)

    STAT['total_sentences'] += len(sentences)

    for sentence in sentences:
        processed_sentence = process_sentence(sentence)
        processed_paragraph += ' ' + processed_sentence

    return processed_paragraph


def process_text(text: list) -> tuple:
    """
    The whole text processing flow, paragraph by paragraph.
    Returns the processed text with formatting, and calculated text statistics.
    """
    STAT['total_paragraphs'] = len(list(filter(lambda p: p != '', text)))

    processed_text = []
    for paragraph in text:
        processed_paragraph = process_paragraph(paragraph) if paragraph != '' else ''
        processed_text.append(processed_paragraph)

    return processed_text, STAT


def print_text(text: list) -> None:
    """
    Print the whole processed text.
    """
    for paragraph in text:
        paragraph = LineFormat.convert_paragraph_symbols_to_formats(
            TextWrapper(
                width=os.get_terminal_size().columns + 1, break_long_words=False
            )
            .fill(text=paragraph)
        )
        print(paragraph)


def print_stat() -> None:
    """
    Prints text statistics in the following order:
        - Total paragraphs found;
        - Total sentences found;
        - Total words found;
        - Total characters and letters found;
        - Number of sentences that are hard to read;
        - Number of sentences that are very hard to read;
        - Number of sentences with a bad start;
        - Number of passive voice usages;
        - Number of adverbs and qualifier words found;
        - Number of phrases that have simpler alternatives.
    """
    print(
        f'\n\n====================================\n\n'
        f'Paragraphs: {STAT["total_paragraphs"]}\n'
        f'Sentences: {STAT["total_sentences"]}\n'
        f'Words: {STAT["total_words"]}\n'
        f'Characters: {STAT["total_characters"]} ({STAT["total_letters"]} letters)\n'
        f'\n'
        f'{STAT["hard_sentences"]} out of {STAT["total_sentences"]} sentences are '
        f'{LineFormat.YELLOW}hard to read{LineFormat.ENDC}.\n'
        f'{STAT["very_hard_sentences"]} out of {STAT["total_sentences"]} sentences are '
        f'{LineFormat.RED}very hard to read{LineFormat.ENDC}.\n'
        f'Found:\n'
        f'{LineFormat.GREEN}- {STAT["bad_start"]} cliché sentence openers{LineFormat.ENDC}. ' +
        f'{"Rebuild the sentence to avoid them." if STAT["bad_start"] > 0 else ""}\n'
        f'{LineFormat.GREEN}- {STAT["passive_voice"]} uses of passive voice{LineFormat.ENDC}. '
        f'{"Use active voice instead." if STAT["passive_voice"] > 0 else ""}\n'
        f'{LineFormat.CYAN}- {STAT["adverbs"]} adverbs & '
        f'{STAT["qualifiers"]} qualifiers{LineFormat.ENDC}. '
        f'{("Try to use " + str(STAT["total_paragraphs"] // 3) + " or less.") if STAT["qualifiers"] > 0 else ""}'
        f'\n'
        f'{LineFormat.PURPLE}- {STAT["complex"]} phrases have simpler alternatives{LineFormat.ENDC}. '
        f'{"Enter the phrases to find replacement recommendations:" if STAT["complex"] > 0 else ""}\n\n'
    )
