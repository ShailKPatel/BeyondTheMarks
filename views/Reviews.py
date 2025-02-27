import streamlit as st
import plotly.graph_objects as go
import os

class QueueWithReverse:
    """Queue with a fixed limit, older reviews are removed when new ones come in."""
    THRESHOLD = 6  # Maximum queue size

    def __init__(self):
        """Initialize the queue with a fixed limit."""
        self.limit = self.THRESHOLD
        self.storage = []

    def enqueue(self, entry):
        """Add a new entry to the queue. If full, remove the oldest entry."""
        if self.is_full():
            self.dequeue()
        self.storage.append(entry)

    def dequeue(self):
        """Remove and return the oldest entry in the queue."""
        if not self.is_empty():
            return self.storage.pop(0)
        return None

    def size(self):
        """Return the current number of entries in the queue."""
        return len(self.storage)

    def is_full(self):
        """Check if the queue has reached its limit."""
        return self.size() >= self.limit

    def is_empty(self):
        """Check if the queue is empty."""
        return self.size() == 0

    def retrieve(self):
        """Retrieve the list of current queue entries."""
        return self.storage

def extract_reviews():
    """Retrieve archived review entries and load them into the queue."""
    repository = QueueWithReverse()
    try:
        with open("reviews/recent_reviews.txt", "r", encoding="utf-8", errors='ignore') as archive:
            for note in archive:
                repository.enqueue(note.strip())
    except FileNotFoundError:
        pass  # If file does not exist, start with an empty queue
    return repository

def preserve_reviews(repository):
    """Save the current queue entries back to the archive file."""
    with open("reviews/recent_reviews.txt", "w", encoding="utf-8") as archive:
        for entry in repository.retrieve():
            archive.write(entry.replace("\n", " ") + "\n")

# Custom HashMap for word frequency
class CustomHashMap:
    def __init__(self, filename="reviews/word_count.txt"):
        self.hash_map = {}
        self.filename = filename
        self.load_word_count()

    def add(self, word):
        """Add word to the hash map and update its frequency."""
        self.hash_map[word] = self.hash_map.get(word, 0) + 1
        self.save_word_count()

    def get_items(self):
        """Get the top 10 most frequent words."""
        return dict(sorted(self.hash_map.items(), key=lambda item: item[1], reverse=True)[:10])

    def load_word_count(self):
        """Load the word count data from the file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', errors='ignore') as file:
                lines = file.readlines()
                for line in lines:
                    word, count = line.strip().split(": ")
                    self.hash_map[word] = int(count)

    def save_word_count(self):
        """Save the word frequency data to the file."""
        with open(self.filename, 'w') as file:
            for word, count in self.hash_map.items():
                file.write(f"{word}: {count}\n")


# Initialize data structures
review_queue = extract_reviews()  # Load existing reviews into the queue
word_count_map = CustomHashMap()  # Custom HashMap for word frequency

# Streamlit UI
st.title("💬 Beyond the Marks: The Feedback Chronicles")

# Display stored reviews (last 6 reviews)
st.subheader("📜 Recent Reviews (aka My Emotional Rollercoaster)")
reviews = review_queue.retrieve()
if reviews:
    total_entries = len(reviews)
    for i in range(0, total_entries, 3):
        columns = st.columns(min(3, total_entries - i))
        for j in range(min(3, total_entries - i)):
            with columns[j]:
                st.write(f"✍️ {reviews[i + j]}")
else:
    st.write("No reviews yet. Be the first to leave your mark! ✨")

# Display top 10 most frequent words
st.subheader("📊 Top 10 Words People Can't Stop Using (aka The 'Sentiment' Breakdown)")
# Get the top 10 words and their frequencies
word_counts = word_count_map.get_items()

# Prepare data for the bar graph
words = list(word_counts.keys())
frequencies = list(word_counts.values())

# Create a Plotly bar graph
fig = go.Figure(data=[go.Bar(x=words, y=frequencies, marker_color='indianred')])

# Update the layout for better display
fig.update_layout(
    title="Top 10 Most Used Words)",
    xaxis_title="Words",
    yaxis_title="Frequency",
    template="plotly_dark"
)

# Show the graph
st.plotly_chart(fig)
# Input for user reviews
user_review = st.text_area("Got Complaint.. Er... Suggestion? Drop them here", "")

if st.button("Submit Review"):
    if user_review:
        review_queue.enqueue(user_review)  # Add review to queue
        preserve_reviews(review_queue)  # Save the updated reviews

        # Process words in review
        words = user_review.lower().split()
        for word in words:
            word_count_map.add(word)  # Update word frequency

        st.balloons()
        st.success("Review submitted! No one asked for it, but here we are.")
        st.rerun()

    else:
        st.warning("Your feedback is as empty as my promises. Try again.")
