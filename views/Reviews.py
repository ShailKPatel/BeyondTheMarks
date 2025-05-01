import streamlit as st
import plotly.graph_objects as go
import os
import time
from collections import deque, Counter

REVIEW_PATH = "reviews/recent_reviews.txt"
WORD_COUNT_PATH = "reviews/word_count.txt"
REVIEW_LIMIT = 6

# Load reviews into deque with max length
def extract_reviews():
    queue = deque(maxlen=REVIEW_LIMIT)
    try:
        with open(REVIEW_PATH, "r", encoding="utf-8", errors="ignore") as archive:
            for line in archive:
                queue.append(line.strip())
    except FileNotFoundError:
        pass
    return queue

# Save reviews back to file
def preserve_reviews(queue):
    with open(REVIEW_PATH, "w", encoding="utf-8") as archive:
        for entry in queue:
            archive.write(entry.replace("\n", " ") + "\n")

# Load word counts into Counter
def load_word_count():
    counter = Counter()
    if os.path.exists(WORD_COUNT_PATH):
        with open(WORD_COUNT_PATH, "r", errors='ignore') as file:
            for line in file:
                try:
                    word, count = line.strip().split(": ")
                    counter[word] = int(count)
                except ValueError:
                    continue
    return counter

# Save word counts back to file
def save_word_count(counter):
    with open(WORD_COUNT_PATH, "w") as file:
        for word, count in counter.items():
            file.write(f"{word}: {count}\n")

# Initialize data
review_queue = extract_reviews()
word_count_map = load_word_count()

# Streamlit UI
st.title("💬 Beyond the Marks: The Feedback Chronicles")

st.subheader("📜 Recent Reviews (aka My Emotional Rollercoaster)")
if review_queue:
    total_entries = len(review_queue)
    for i in range(0, total_entries, 3):
        columns = st.columns(min(3, total_entries - i))
        for j in range(min(3, total_entries - i)):
            with columns[j]:
                st.write(f"✍️ {list(review_queue)[i + j]}")
else:
    st.write("No reviews yet. Be the first to leave your mark! ✨")

st.subheader("📊 Top 10 Words People Can't Stop Using (aka The 'Sentiment' Breakdown)")
top_words = dict(sorted(word_count_map.items(), key=lambda item: item[1], reverse=True)[:10])
words = list(top_words.keys())
frequencies = list(top_words.values())

fig = go.Figure(data=[go.Bar(x=words, y=frequencies, marker_color='indianred')])
fig.update_layout(
    title="Top 10 Most Used Words",
    xaxis_title="Words",
    yaxis_title="Frequency",
    template="plotly_dark"
)
st.plotly_chart(fig)

user_review = st.text_area("Got Complaint.. Er... Suggestion? Drop them here", "")

if st.button("Submit Review"):
    if user_review:
        review_queue.append(user_review)
        preserve_reviews(review_queue)

        for word in user_review.lower().split():
            word_count_map[word] += 1
        save_word_count(word_count_map)

        st.balloons()
        st.success("Review submitted! No one asked for it, but here we are.")
        time.sleep(3)
        st.rerun()
    else:
        st.warning("Your feedback is as empty as my promises. Try again.")
