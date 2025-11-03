import streamlit as st
import feedparser
from ollama import Client

# ✅ Initialize Ollama client (ensure ollama is running)
client = Client(host='http://localhost:11434')

# ✅ RSS Feeds by category
RSS_FEEDS = {
    "🌍 World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "💼 Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "🧪 Science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "💻 Technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "🩺 Health": "http://feeds.bbci.co.uk/news/health/rss.xml",
    "🏟 Sports": "http://feeds.bbci.co.uk/sport/rss.xml"
}

# ✅ Page setup
st.set_page_config(page_title="📰 Global News Tracker", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #FFFFFF;'>🗞️ Global News Tracker</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Fetch today’s top news by category and generate a brief summary instantly.</p>",
    unsafe_allow_html=True
)

# ✅ Maintain app state
if "headlines" not in st.session_state:
    st.session_state.headlines = {}
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

# ✅ Clear session state
def clear_news():
    st.session_state.headlines = {}
    st.session_state.show_summary = False

# ✅ Button row
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Get Today's News", use_container_width=True):
        clear_news()
        st.session_state.show_summary = False
        st.session_state.headlines = {}

        with st.container():
            st.subheader("📰 Headlines by Category")
            for category, url in RSS_FEEDS.items():
                feed = feedparser.parse(url)
                entries = feed.entries[:5]
                if entries:
                    st.session_state.headlines[category] = [
                        (entry.title, entry.link) for entry in entries
                    ]
                    with st.expander(f"{category}"):
                        for entry in entries:
                            st.markdown(
                                f"<li><a href='{entry.link}' target='_blank'>{entry.title}</a></li>",
                                unsafe_allow_html=True
                            )
        if not st.session_state.headlines:
            st.warning("⚠️ No headlines found. Please check your network or RSS feeds.")

with col2:
    if st.button("🧹 Clear News", use_container_width=True):
        clear_news()
        st.success("News cleared successfully!")

# ✅ Summarize only if headlines exist
if st.session_state.headlines:
    st.markdown("---")
    st.subheader("🧠 Generate Summary")

    if st.button("🧩 Summarize Headlines", use_container_width=True):
        st.session_state.show_summary = True

    # ✅ Hide news when summarizing
    if st.session_state.show_summary:
        with st.spinner("Generating short summary (1-2 headlines per category)..."):
            try:
                # Take 1–2 headlines per category for speed
                selected_headlines = []
                for cat, items in st.session_state.headlines.items():
                    selected_headlines.extend([t for t, _ in items[:2]])

                news_text = "\n".join(selected_headlines)
                prompt = f"Summarize these recent news headlines briefly (3-5 concise points):\n\n{news_text}"

                response = client.chat(
                    model="llama3",
                    messages=[{"role": "user", "content": prompt}]
                )
                summary = response["message"]["content"]

                st.success("✅ Summary Ready")
                st.markdown("### 📋 Condensed Summary of Top Headlines")
                st.markdown(
                    f"<div style='background-color: #333; padding: 15px; border-radius: 10px; color: white;'>{summary}</div>",
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"❌ Error generating summary: {e}")
