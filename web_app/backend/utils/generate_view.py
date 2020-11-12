def create_inform(path, specific_data_web):

    Html_file = open(path, "w+")
    Html_file.write('{% extends "base_generic.html" %}')
    Html_file.write('{% block content %}')
    Html_file.write(str(specific_data_web))
    Html_file.write('{% endblock %}')
    Html_file.close()



    