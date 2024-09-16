import streamlit as st
from streamlit_option_menu import option_menu
import home, admin


class MultiApp:
    def _init_(self):
        self.apps = []
    def add_app(Self, title, function):
        Self.apps.append({
            "title": title,
            "function": function
       })
        
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='Navegación',
                options=['Home', 'Administrar cursos'],
                icons=['house-fill', 'person-circle'],
                menu_icon= "chat-text-fill",
                default_index=1,
                styles={
                    "container": {"padding": "5!important","backgroung-color:": 'black',},
                    "icon":{"font-size": "23px"},
                    "nav-link": { "font-size": "20px", "text-align": "left", "margin":"0px"},
                    "nav-link_Selected": {"background-color": "#02ab21"},
                }
            )

        if app== 'Home':
           home.app() 
        if app== 'Administrar cursos':
           admin.app() 

    run()


