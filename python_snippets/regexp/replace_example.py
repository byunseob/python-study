import re


def replace(text):
    regexp = re.compile('<.?mark>')
    text = re.sub(regexp, '', text)
    return text


test_text = "<mark>test test1 test2</mark>"
print(replace(test_text))
assert "test test1 test2" == replace(test_text)
