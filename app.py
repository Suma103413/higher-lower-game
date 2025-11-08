import streamlit as st
import random
from art import vs
from game_data import data

# -----------------------------
# Helper functions
# -----------------------------
def format_data(account):
    """Take account data and return formatted text."""
    account_name = account["name"]
    account_descr = account["description"]
    account_country = account["country"]
    return f"**{account_name}**, a {account_descr}, from {account_country}"

def check_answer(user_guess, a_followers, b_followers):
    """Return True if user guessed correctly."""
    if a_followers > b_followers:
        return user_guess == "A"
    else:
        return user_guess == "B"

# -----------------------------
# Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="Higher or Lower Game", page_icon="🔥", layout="centered")

st.markdown(
    "<h1 style='text-align:center; color:#FF4B4B;'>🔥 Higher or Lower Game 🔥</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align:center;'>Guess who has more followers on Instagram!</p>", unsafe_allow_html=True)
st.divider()

# -----------------------------
# Initialize Session State
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "account_a" not in st.session_state:
    st.session_state.account_a = random.choice(data)
if "account_b" not in st.session_state:
    st.session_state.account_b = random.choice(data)
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# -----------------------------
# Show Game Interface
# -----------------------------
if not st.session_state.game_over:

    # Display score on top
    st.markdown(f"<h4 style='text-align:center;'>Current Score: {st.session_state.score}</h4>", unsafe_allow_html=True)
    st.divider()

    # Layout with centered VS
    col1, col_mid, col2 = st.columns([4, 1, 4])

    with col1:
        st.subheader("A")
        st.markdown(format_data(st.session_state.account_a))

    with col_mid:
        # Centered VS
        st.markdown(f"<div style='text-align:center; font-size:40px; color:#00BFFF;'>{vs}</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("B")
        st.markdown(format_data(st.session_state.account_b))

    # Choose your guess
    st.write("Who has more followers?")
    guess = st.radio(
        "Choose your answer:",
        ["A", "B"],
        horizontal=True,
        index=None,
        key=f"guess_{st.session_state.score}"
    )

    if st.button("Submit Guess 🚀"):
        if guess:
            a_followers = st.session_state.account_a["follower_count"]
            b_followers = st.session_state.account_b["follower_count"]

            is_correct = check_answer(guess, a_followers, b_followers)

            if is_correct:
                st.session_state.score += 1
                st.success(f"✅ Yes! Your guess is correct 🎉")
                st.info(f"Current Score: {st.session_state.score}")

                # Move to next round
                st.session_state.account_a = st.session_state.account_b
                st.session_state.account_b = random.choice(data)
                st.rerun()

            else:
                st.error(f"❌ Oops! That’s wrong 😢 Final Score: {st.session_state.score}")
                st.session_state.game_over = True
                st.rerun()
        else:
            st.warning("Please select an option before submitting!")

# -----------------------------
# Game Over Screen
# -----------------------------
else:
    st.markdown("<h3 style='text-align:center; color:red;'>Game Over 😔</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Your Final Score: <b>{st.session_state.score}</b></p>", unsafe_allow_html=True)
    if st.button("Play Again 🔁"):
        # Reset everything
        st.session_state.score = 0
        st.session_state.account_a = random.choice(data)
        st.session_state.account_b = random.choice(data)
        st.session_state.game_over = False
        st.rerun()
