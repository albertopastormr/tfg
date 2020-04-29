from backend.general_report import generate_analysis_general, generate_kpi_general
from backend.utils.generate_view import create_inform

def create_inform_general():
    return create_inform(
                        path="pems/templates/use_case/solar.html", 
                        specific_data_web = 
                            "<div>" + 
                                str(generate_analysis_general()) + 
                                str(generate_kpi_general()) + 
                            "</div>"
    )

def create_specific_inform():
    return ""