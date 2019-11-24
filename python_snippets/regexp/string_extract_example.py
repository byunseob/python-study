import re


def extract(text):
    regexp = '<mark>(.+?)</mark>'
    m = re.search(regexp, text)
    if m:
        return m.group(1)
    else:
        return ''


test_text = "<mark>test test1 test2</mark>"
print(extract(test_text))
assert "test test1 test2" == extract(test_text)


def extract_by_htmlparser(html: str):
    from html.parser import HTMLParser

    class CustomHtmlParser(HTMLParser):
        content = ''
        name = ''

        def error(self, message):
            pass

        def handle_starttag(self, tag, attrs):
            if tag == 'meta':
                for attr in attrs:
                    if attr[0] == 'content':
                        self.content = attr[1]
                    if attr[0] == 'name':
                        self.name = attr[1]

    parser = CustomHtmlParser()
    parser.feed(html)
    return parser


test_text = '<meta name="Robots" content="noindex, nofollow" />'
print(extract_by_htmlparser(test_text).name)
assert "Robots" == extract_by_htmlparser(test_text).name
