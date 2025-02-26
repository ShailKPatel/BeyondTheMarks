import streamlit as st

# Logo
image = "images/logo.png"
st.logo(image, size='large')

# Page Title
st.title("🧠 The Brains Behind")
st.write("Where genius meets caffeine-fueled debugging! ☕💻")

# Shail K Patel - The mastermind
# The `st.subheader(" **Shail K Patel** – Code Alchemist & Debugging Wizard")` line is creating a
# subheader in the Streamlit web application interface. It displays the text "Shail K Patel - Code
# Alchemist & Debugging Wizard" with a slightly larger font size compared to regular text, making it
# stand out as a section title or heading within the content. The use of double asterisks (`**`)
# around the name emphasizes the text and makes it bold.
st.subheader("🐵 **Shail K Patel** – Code Alchemist & Debugging Wizard")
st.write(
    "Shail doesn't just write code—he **convinces computers to behave**. "
    "Fueled by **late-night debugging marathons** and an unhealthy obsession with **optimizing everything**, "
    "he turned data science into an **art form** (or at least a well-commented mess). "
    "When he's not **teaching pandas how to sort data**, he’s probably debating with Stack Overflow."
)

# Social Links
st.link_button("🔗 Stalk Him on LinkedIn", "https://www.linkedin.com/in/shail-k-patel/")
st.link_button("🐙 Investigate His GitHub", "https://github.com/ShailKPatel")

# Fun Fact
st.write("🚀 **Fun Fact:** This entire project was fueled by **coffee, curiosity, and occasional existential crises**. 😅")
