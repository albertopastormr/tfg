from backend.utils.generate_view import create_inform

def create_inform_general(informs_array):
    return create_inform(
                        path="pems/templates/use_case/solar.html", 
                        specific_data_web = 
                            "<div>" +
                                " ".join(informs_array) +
                            "</div>"
    )

def create_specific_inform():
    return ""