import streamlit as st

# Logo
image = "images/logo.png"
st.logo(image, size='large')

# Page Title
st.title("🛠️ Tech Wizardry")
st.write("Because magic is just science **we don’t understand yet**… but this? This is Python. 🐍🔥")

# 🏗️ Tech Stack Breakdown
st.subheader("📌 **Core Tech Stack** – The Ingredients of This Digital Sorcery")
st.write(
    "**📝 Language:** Python (Because why struggle with anything else?)\n"
    "**🎨 Frontend:** Streamlit (Turning Python scripts into web apps faster than you can say 'debug')\n"
    "**📚 Libraries Used:** The ultimate toolbox for a data scientist:"
)

# List of Libraries Used
st.markdown(
    """
    - 🧮 **Numpy & Pandas** – For making data behave (or at least pretend to).
    - 📊 **Plotly** – Because plain graphs are just… too mainstream.
    - 🎭 **Scipy & Statsmodels** – Where all the statistical black magic happens.
    - 🤖 **Sklearn** – Machine learning, but make it effortless.
    - 🎭 **SHAP** – Bias detection with explainability (a.k.a. “Why is this model so biased?”).
    - 🔍 **Pydocs** – Documenting code like a responsible adult.
    """
)

# 🧙‍♂️ Math Sorcery Section
st.subheader("🧙‍♂️ **Mathematical Wizardry** – Where Numbers Cast Spells")
st.markdown(
    """
    - 📈 **ANOVA for Teacher Rating** – Because some teachers **actually make a difference**.
    - 🎭 **One-Hot Encoding for Bias Detection** – Teaching the model not to judge based on labels.
    - 🕵️ **SHAP for Bias Detection** – Exposing hidden biases like a detective in a noir movie.
    """
)

# 🤯 The "Why This Works" Section
st.subheader("🤯 **Why This Works** – The Not-So-Secret Formula")
st.write(
    "Imagine **feeding raw academic data into a black hole** and getting **insights that actually make sense**. "
    "That’s what this tool does—except it’s backed by **math, machine learning, and enough caffeine to fuel a small rocket.**"
)

# 🚀 Final Fun Note
st.write("⚡ **Fun Fact:** This project has more statistical power than my brain on a Monday morning. 📊☕")

