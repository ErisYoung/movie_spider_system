def get_line_name(strings: str):
    return strings[0].upper()


def write_html_to_base(text):
    file_name = "temp.html"
    with open(file_name, 'w', encoding="utf8") as f:
        f.write(text)
