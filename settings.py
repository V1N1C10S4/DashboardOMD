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
        return """
        <style>
            body { background-color: #004D40; color: #F9A825; }
            .stButton>button { background-color: #1F1F1F; color: #F9A825; border: 1px solid #F9A825; }
            .stTextInput>div>input { background-color: #262626; color: #F9A825; }
            .block-container { background-color: #004D40; }
        </style>
        """
    else:
        return """
        <style>
            body { background-color: #F0F2F6; color: #004D40; }
            .stButton>button { background-color: #F9A825; color: #004D40; border: 1px solid #004D40; }
            .stTextInput>div>input { background-color: #FFFFFF; color: #004D40; }
            .block-container { background-color: #F0F2F6; }
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