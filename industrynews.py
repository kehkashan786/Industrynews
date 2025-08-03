import feedparser

from flask import Flask, request, jsonify

app = Flask(__name__)

def get_industry_news(industry, max_results=5):
    # Google News RSS Feed URL with query
    query = industry.replace(' ', '+')
    url = f"https://news.google.com/rss/search?q={query}"

    # Parse RSS feed
    feed = feedparser.parse(url)

    # Collect headlines
    headlines = []
    for entry in feed.entries[:max_results]:
        headlines.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })

    # Return the result
    return headlines

@app.route('/industry', methods=['POST'])
def industry_news():
    print("Received request for industry news")
    data = request.get_json(force=True)
    industry_input = data.get('industry')
    if not industry_input:
        return jsonify({'error': 'Industry missing in request'}), 400
    news = get_industry_news(industry_input)
    if news:
        return jsonify({'industry': industry_input, 'news': news})
    else:
        return jsonify({'error': 'No news found or failed to fetch.'}), 404

if __name__ == '__main__':
    print("Starting industry news service...")
    app.run()

