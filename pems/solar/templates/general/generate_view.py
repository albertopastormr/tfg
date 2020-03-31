from util import read_html_file

def create_inform(specific_data_web):

    Html_file = open("pems/solar/templates/solar/prueba_1.html", "w")

    Html_file.write(read_html_file("pems/solar/templates/general/html/head.html"))

    Html_file.write(read_html_file("pems/solar/templates/general/html/header.html"))

    Html_file.write(str(specific_data_web))

    Html_file.write(read_html_file("pems/solar/templates/general/html/end.html"))

    Html_file.close()
    
def create_index():

    Html_file = open("pems/solar/templates/index.html", "w")

    Html_file.write(read_html_file("pems/solar/templates/general/html/head.html"))

    Html_file.write(read_html_file("pems/solar/templates/general/html/header.html"))

    # Context page principal page
    Html_file.write("Index page info.")

    Html_file.write(read_html_file("pems/solar/templates/general/html/end.html"))

    Html_file.close()