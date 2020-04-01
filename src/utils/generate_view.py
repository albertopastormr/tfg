def create_inform(specific_data_web):

    Html_file = open("pems/pems/templates/use_case/solar.html", "w+")
    Html_file.write('{% extends "base_generic.html" %}')
    Html_file.write('{% block content %}')
    Html_file.write(str(specific_data_web))
    Html_file.write('{% endblock %}')
    Html_file.close()

    