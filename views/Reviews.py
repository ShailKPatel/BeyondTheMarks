import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import json
import os
from collections import Counter, deque
import re
import numpy as np

# File Paths
REVIEW_PATH = "reviews/recent_reviews.json"
WORD_COUNT_PATH = "reviews/word_count.json"
REVIEW_LIMIT = 6

# Expanded filter words to prevent "lol" variations and vandalism
FILTER_WORDS = {
    "lol", "lolis", "laughing", "out", "loud",  # Cover "laughing out loud" and variations
    "haha", "hehe", "lmao", "rofl"  # Other informal laughter terms
}

# Load reviews
def load_reviews():
    if os.path.exists(REVIEW_PATH):
        with open(REVIEW_PATH, "r", encoding="utf-8") as file:
            return deque(json.load(file), maxlen=REVIEW_LIMIT)
    return deque(maxlen=REVIEW_LIMIT)

# Save reviews
def save_reviews(reviews):
    with open(REVIEW_PATH, "w", encoding="utf-8") as file:
        json.dump(list(reviews), file)

# Load word count
def load_word_count():
    if os.path.exists(WORD_COUNT_PATH):
        with open(WORD_COUNT_PATH, "r", encoding="utf-8") as file:
            return Counter(json.load(file))
    return Counter()

# Save word count
def save_word_count(counter):
    with open(WORD_COUNT_PATH, "w", encoding="utf-8") as file:
        json.dump(dict(counter), file)

# Filter words: stop words, "lol" variations, and vandalism
def should_count_word(word):
    # Use regex to catch "lol" with special characters (e.g., "lol!")
    if re.search(r'l+o+l+[!@#$%^&*]*', word.lower()):
        return False
    # Check against stop words and filter words
    return (word.lower() not in STOPWORDS and 
            word.lower() not in FILTER_WORDS and 
            not any(fw in word.lower() for fw in FILTER_WORDS))

# Check if review contains "lol" or filtered words
def contains_filtered_words(review):
    words = review.split()
    for word in words:
        # Check for "lol" variations with regex
        if re.search(r'l+o+l+[!@#$%^&*]*', word.lower()):
            return True
        # Check for other filter words
        if any(fw in word.lower() for fw in FILTER_WORDS) or word.lower() in FILTER_WORDS:
            return True
    return False

# Initialize data
review_queue = load_reviews()
word_count = load_word_count()

# Streamlit UI
st.title("💬 Beyond the Marks: The Feedback Chronicles")

st.subheader("📜 Recent Reviews")
if review_queue:
    for review in review_queue:
        st.write(f"✍️ {review}")
else:
    st.write("No reviews yet. Be the first to leave your mark! ✨")

st.subheader("📊 Word Cloud")
if word_count:
    # Filter word_count to remove stop words and filtered words
    filtered_word_count = Counter()
    for word, freq in word_count.items():
        if should_count_word(word):
            filtered_word_count[word.lower()] += freq

    if filtered_word_count:
        # Custom color function for a cohesive look (shades of blue)
        def blue_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            return f"hsl(210, 70%, {np.random.randint(40, 80)}%)"

        # Generate word cloud with improved aesthetics
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",  # Lighter background for clarity
            max_words=50,  # Limit to avoid clutter
            min_font_size=12,  # Ensure readability
            scale=3,  # Higher resolution
            stopwords=STOPWORDS.union(FILTER_WORDS),  # Double-check stop words
            color_func=blue_color_func  # Apply custom colors
        ).generate_from_frequencies(filtered_word_count)

        # Display word cloud
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.write("No valid words to display in the word cloud after filtering.")
else:
    st.write("No words to display in the word cloud yet. Submit a review!")

# Submit new review
user_review = st.text_area("Got a complaint or suggestion? Drop it here", "")
if st.button("Submit Review"):
    if user_review:
        # Check if the review contains filtered words
        if not contains_filtered_words(user_review):
            # Only save and process the review if it doesn't contain filtered words
            review_queue.append(user_review)
            save_reviews(review_queue)

            # Process words for word count: remove punctuation, normalize case
            words = re.findall(r'\b\w+\b', user_review.lower())
            for word in words:
                if should_count_word(word):
                    word_count[word] += 1
            save_word_count(word_count)

        # Always show balloons and thanks message, even if review isn't saved
        st.balloons()
        st.success("Review submitted! Thanks for sharing your thoughts!")
        st.rerun()
    else:
        st.warning("Please write something before submitting.")