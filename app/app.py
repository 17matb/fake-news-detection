import streamlit as st

# --- CONFIG PAGE ---
st.set_page_config(
    page_title="Fake News Checker",
    page_icon="📰",
    layout="centered",
)

# --- INIT SESSION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STYLE CSS POUR GARDER LE CHAT INPUT EN BAS ---
st.markdown(
    """
    <style>
    /* Fixe la zone d'input en bas */
    .stChatInputContainer {
        position: fixed;
        bottom: 1rem;
        left: 0;
        right: 0;
        z-index: 100;
        background-color: white;
        padding: 1rem 2rem 0.5rem 2rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    /* Laisse de la place en bas pour ne pas masquer le contenu */
    .block-container {
        padding-bottom: 8rem;
    }

    /* Permet le scroll si beaucoup de messages */
    .stApp {
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TITRE ---
st.title("Fake News Checker")
st.divider()
st.markdown(
    """
    Entrez une news ou un article pour vérifier la véracité de l'information.
    """
)

# --- AFFICHAGE DES MESSAGES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAMP DE SAISIE (en bas, fixé par le CSS) ---
user_input = st.chat_input("Écrivez ici votre news...")

if user_input:
    # Message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Réponse assistant (simulée ici)
    with st.chat_message("assistant"):
        with st.spinner("Vérification de la véracité de la news..."):
            try:
                fake_or_not = "Cette news semble fiable."  # à remplacer par ton modèle
                st.markdown(fake_or_not)
                st.session_state.messages.append(
                    {"role": "assistant", "content": fake_or_not}
                )
            except Exception as e:
                error_msg = f"Erreur pendant l'analyse : {e}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
