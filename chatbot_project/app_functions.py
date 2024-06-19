import streamlit as st
import base64
import io
import os

def image_to_base64(image) -> str:
    """
    Convert an image to a base64-encoded string.

    Args:
        image: A PIL Image object

    Returns:
        A base64-encoded string representation of the image
    """
    with io.BytesIO() as buffer:
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")

def display_logo_and_title(logo_image):
    logo_base64 = image_to_base64(logo_image)
    html_template = """
        <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
            <img src="data:image/jpeg;base64,{logo_base64}" width="250" alt="logo">
            <p>{title}</p>
        </div>
    """
    title = "Edit - Disruptive Digital Education"
    st.markdown(html_template.format(logo_base64=logo_base64, title=title), unsafe_allow_html=True)

def display_intro(logo_image):
    display_logo_and_title(logo_image=logo_image)
    display_gif("robot_animation.gif")

    st.subheader("Olá, eu sou o EditAssist, o assistente virtual da Edit.")
    st.write("Escreva a tua pergunta abaixo para saber mais sobre os nossos cursos:")

def display_gif(gif_path: str) -> None:
    """
    Display a GIF image from a file path.

    Args:
        gif_path: The path to the GIF file.

    Returns:
        None
    """
    if not os.path.exists(gif_path):
        st.error(f"Error: GIF file '{gif_path}' not found.")
        return

    try:
        with open(gif_path, "rb") as gif_file:
            gif_data = base64.b64encode(gif_file.read()).decode()
        
        html = f"""
            <div style="display: flex; justify-content: center;">
                <img src="data:image/gif;base64,{gif_data}" width="200" alt="robot animation">
            </div>
            """
        
        st.markdown(html, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error displaying GIF: {e}")

def display_chat_history():
    for i in range(0, len(st.session_state.history), 2):
        user_message, user_time = st.session_state.history[i]
        bot_message, bot_time = st.session_state.history[i + 1]
        
        user_html = f"""
            <div class='message user-message'>
                <div class='message-content'>{user_message}</div>
                <div class='message-time'>{user_time}</div>
            </div>
        """
        
        bot_html = f"""
            <div class='message bot-message'>
                <div class='message-content'>{bot_message}</div>
                <div class='message-time'>{bot_time}</div>
            </div>
        """
        
        st.markdown(user_html, unsafe_allow_html=True)
        st.markdown(bot_html, unsafe_allow_html=True)
