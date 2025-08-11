from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.fed = []
        self.ignored_tags = {"title", "style", "script"}
        self.skip = False
        self.skip_tag = None

    def handle_starttag(self, tag, attrs):
        if tag in self.ignored_tags:
            self.skip = True
            self.skip_tag = tag

    def handle_endtag(self, tag):
        if self.skip and tag == self.skip_tag:
            self.skip = False
            self.skip_tag = None

    def handle_data(self, data):
        if not self.skip:
            self.fed.append(data)

    def get_data(self):
        return "".join(self.fed)


def strip_tags(value):
    """
    Remove HTML tags and certain unwanted content from the given HTML string,
    returning clean, plain text with normalized whitespace.

    This function uses a custom HTML parser that strips out all HTML tags,
    and also ignores the content inside <title>, <style>, and <script> tags,
    which often contain CSS, JavaScript, or metadata not useful for log messages.

    Whitespace, including newlines, is collapsed to single spaces for readability.

    Intended use:
    Clean and simplify HTML error responses from Checkbox (e.g., 503 Service Temporarily Unavailable pages)
    to produce more readable and concise log messages.

    Args:
        value (str): The raw HTML string to clean.

    Returns:
        str: Plain text extracted from the HTML input, without tags or ignored content,
             with normalized whitespace.
    """
    s = MLStripper()
    s.feed(value)
    return " ".join(s.get_data().split())
