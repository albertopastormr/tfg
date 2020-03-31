import codecs

def read_html_file(path_file):
    f = codecs.open(path_file, 'r')
    return f.read()