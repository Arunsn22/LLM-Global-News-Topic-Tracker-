# LLM-Global-News-Topic-Tracker-
# 📝 Learning Log: Streamlit + Ollama News Summarizer

## Project: Global News Tracker using Streamlit + Ollama (LLaMA 3) + RSS

---

## Topics Learned

### 1. LLM Integration (Ollama)
- Learned how to use `ollama` Python package to connect to a locally running LLaMA 3 model.
- Used the `Client` from `ollama` to send chat prompts and receive responses.

### 2. RSS Feeds
- Discovered how to use RSS feeds from BBC to fetch structured news headlines by category.
- Integrated `feedparser` to read XML-based RSS feeds and extract the top headlines.

### 3. 🖥Streamlit for Frontend
- Created an interactive interface with:
  - Title and description
  - Button to fetch news
  - Expanders for categorized headlines
  - Spinners and stylized output for loading states and summaries

### 4. Summarization Prompting
- Learned prompt construction for summarizing 20 headline strings using LLaMA 3.
- Modified prompt format for better summaries with clear bullet-point format and human-friendly phrasing.

---

## Issues Encountered & Solutions

### `RateLimitError: 429` using OpenAI
- **Issue**: Initial code used OpenAI's GPT model which threw a quota error.
- **Solution**: Switched to **local** LLaMA 3 using `ollama` to eliminate external API dependence.

---

### `ModuleNotFoundError: No module named 'feedparser'`
- **Cause**: Feedparser not installed in the current environment.
- **Fix**: Installed using `pip install feedparser`.

---

### `ModuleNotFoundError: No module named 'ollama'`
- **Cause**: Ollama library missing.
- **Fix**: Installed with `pip install ollama`.

---

### "No headlines found"
- **Cause**: Either RSS feed failed to parse (due to connection or limit) or reached the headline cap.
- **Fix**: Added proper limit check (`max_headlines = 20`) and improved feed parsing fallback.

---

### Script ran too long with topic clustering
- **Cause**: Original version clustered topics and summarized each, leading to long runtimes.
- **Fix**: Removed topic clustering; directly fetched top 20 headlines from multiple categories and summarized all at once.

---

## Enhancements Made

- Introduced a **“📥 Get Today's News”** button to control headline loading.
- Added **loading spinner** while generating summaries.
- Styled the UI with centered headers, expanders, and custom summary box.
- Added sports category and adjusted total headline cap to 20.
- Implemented background summarization after displaying headlines.

---

## Virtual Environment Setup (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install streamlit feedparser ollama
```

---

## Final Outcome

A fully working **Streamlit web app** that:
- Fetches top 20 news headlines across 6 categories
- Displays them with links in an expandable view
- Generates a high-quality summary using LLaMA 3 (via Ollama)
- Provides an interactive, stylish, and local-first experience

---

## Notes

- This setup is fully **local**: no API keys or internet model calls required.
- All summaries are generated via the **LLaMA 3 model** served locally using Ollama (`http://localhost:11434`).
