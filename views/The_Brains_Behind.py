import streamlit as st

# Logo
image = "images/logo.png"
st.logo(image, size='large')

# Page Title
st.title("🧠 The Brains Behind")
st.write("Where genius meets caffeine-fueled debugging! ☕💻")

st.subheader("🐵 **Shail K Patel**")
# Social Links
st.link_button("🔗 Stalk Him on LinkedIn", "https://www.linkedin.com/in/shail-k-patel/")
st.link_button("🐙 Investigate His GitHub", "https://github.com/ShailKPatel")


st.subheader("**🦧 Panchal Dev**")
st.link_button("LinkedIn", "https://www.linkedin.com/in/dev-panchal-connect/", icon="🔗")
st.link_button("GitHub", "https://github.com/DevPanchal2005", icon="🐙")
# Fun Fact
st.write("🚀 **Fun Fact:** This entire project was fueled by **coffee, curiosity, and occasional existential crises**. 😅")
