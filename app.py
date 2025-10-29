import streamlit as st
import feedparser
from ollama import Client

# Ollama client (ensure ollama is running)
client = Client(host='http://localhost:11434')

# RSS feeds
RSS_FEEDS = {
    "🌍 World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "💼 Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "🧪 Science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "💻 Technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "🩺 Health": "http://feeds.bbci.co.uk/news/health/rss.xml",
    "🏟 Sports": "http://feeds.bbci.co.uk/sport/rss.xml"
}

# Page config
st.set_page_config(page_title="📰 Global News Tracker", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #FFFFFF;'>🗞️ Global News </h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Click the button below to fetch today's top news headlines and get a summarized overview.</p>",
    unsafe_allow_html=True
)

# UI Button
if st.button("📥 Get Today's News", use_container_width=True):
    headlines = []
    total_collected = 0
    max_headlines = 20

    with st.container():
        st.subheader("📰 Headlines by Category")

        for category, url in RSS_FEEDS.items():
            if total_collected >= max_headlines:
                break

            feed = feedparser.parse(url)
            entries = feed.entries[:5]

            if entries:
                with st.expander(f"{category}"):
                    for entry in entries:
                        if total_collected < max_headlines:
                            st.markdown(
                                f"<li><a href='{entry.link}' target='_blank'>{entry.title}</a></li>",
                                unsafe_allow_html=True
                            )
                            headlines.append(entry.title)
                            total_collected += 1
                        else:
                            break

    if headlines:
        st.markdown("---")
        st.subheader("🧠 Generating Summary...")

        with st.spinner("Please wait while we summarize the headlines..."):
            try:
                news_text = "\n".join(headlines)
                prompt = f"Summarize the following news headlines:\n\n{news_text}"

                response = client.chat(
                    model="llama3",
                    messages=[{"role": "user", "content": prompt}]
                )
                summary = response['message']['content']

                st.success("✅ Summary Ready")
                st.markdown("### 📋 Summary of Top Headlines")
                st.markdown(f"<div style='background-color: #333; padding: 15px; border-radius: 10px;'>{summary}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error generating summary: {e}")
    else:
        st.warning("⚠️ No headlines found. Please check your network or RSS feeds.")

#else:
    #st.info("👆 Click the button above to fetch the latest news.")
