class LineFormat:
    """
    Colors for different parts of text that need to be highlighted.
    """
    # TODO(redd4ford): use blue as text added lately from console
    BLUE = '\033[94m'
    # adverbs/qualifiers
    CYAN = '\033[36m'
    # passive voice
    GREEN = '\033[32m'
    # complex phrases
    PURPLE = '\033[35m'
    # readability = hard
    YELLOW = '\033[93m'
    # readability = very hard
    RED = '\033[91m'
    # end coloring symbol
    ENDC = '\033[0m'

    FORMAT_TO_SYMBOL_MAPPER = {
        BLUE: "Ⓑ",
        CYAN: "Ⓒ",
        GREEN: "Ⓖ",
        PURPLE: "Ⓟ",
        YELLOW: "Ⓨ",
        RED: "Ⓡ",
        ENDC: "Ⓧ"
    }

    SYMBOL_TO_FORMAT_MAPPER = {
        "Ⓑ": BLUE,
        "Ⓒ": CYAN,
        "Ⓖ": GREEN,
        "Ⓟ": PURPLE,
        "Ⓨ": YELLOW,
        "Ⓡ": RED,
        "Ⓧ": ENDC
    }

    @staticmethod
    def map(key: str, to: str) -> str:
        """
        Convert LineFormat color code to symbol or vice versa.
        """
        if to == 'symbol':
            return LineFormat.FORMAT_TO_SYMBOL_MAPPER[key]
        elif to == 'format':
            return LineFormat.SYMBOL_TO_FORMAT_MAPPER[key]
        else:
            raise NotImplementedError

    @staticmethod
    def convert_paragraph_formats_to_symbols(paragraph: str) -> str:
        """
        Map all color codes to corresponding symbols.
        """
        for line_format in LineFormat.FORMAT_TO_SYMBOL_MAPPER:
            paragraph = paragraph.replace(line_format, LineFormat.map(line_format, to='symbol'))
        return paragraph

    @staticmethod
    def convert_paragraph_symbols_to_formats(paragraph: str) -> str:
        """
        Map all color symbols to corresponding codes.
        """
        for symbol in LineFormat.SYMBOL_TO_FORMAT_MAPPER:
            paragraph = paragraph.replace(symbol, LineFormat.map(symbol, to='format'))
        return paragraph
