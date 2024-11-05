import streamlit as st

st.header("Settings")
st.write(f"You are logged in as {st.session_state.role}.")
st.title("⚙️ Settings")
st.write("Adjust your preferences here.")

# Initialize dark mode state if not set
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False  # Default to light mode

# CSS for customized theme
def get_css(dark_mode):
    if dark_mode:
        return f"""
        <style>
            body {{
                background-color: #000000;  /* Fondo negro */
                color: #FFFFFF;  /* Texto en blanco */
            }}
            .stButton>button {{
                background-color: #1A73E8;  /* Botones en azul oscuro */
                color: #FFFFFF;
                border: 1px solid #A142F4;  /* Borde morado */
            }}
            .stTextInput>div>input {{
                background-color: #1A73E8;  /* Fondo de inputs en azul oscuro */
                color: #FFFFFF;
            }}
            .block-container {{
                background-color: #000000;
            }}
        </style>
        """
    else:
        return f"""
        <style>
            body {{
                background-color: #FFFFFF;  /* Fondo claro */
                color: #1A73E8;  /* Texto en azul oscuro */
            }}
            .stButton>button {{
                background-color: #A142F4;  /* Botones en púrpura */
                color: #FFFFFF;
                border: 1px solid #1A73E8;  /* Borde azul oscuro */
            }}
            .stTextInput>div>input {{
                background-color: #FFFFFF;
                color: #1A73E8;
            }}
            .block-container {{
                background-color: #FFFFFF;
            }}
        </style>
        """

# Sidebar toggle for theme
st.sidebar.title("Theme Settings")
toggle = st.sidebar.checkbox("Enable Dark Mode", value=st.session_state.dark_mode)

# Update session state and apply CSS
st.session_state.dark_mode = toggle
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Example input and button to test theme
user_input = st.text_input("Enter some text:")
st.write(f"You entered: {user_input}")
st.button("Click me")