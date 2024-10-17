import re

def parse_newsletter(newsletter_text):
    articles = []
    # Split the newsletter into individual articles based on separator
    raw_articles = newsletter_text.split('------------------------------------------------------------------------------')
    for raw in raw_articles:
        if 'arXiv' in raw:
            try:
                title_match = re.search(r'Title:\s*(.*)', raw)
                link_match = re.search(r'\((https?://arxiv\.org/abs/\d{4}\.\d{5})__.*\)', raw)
                if title_match and link_match:
                    title = title_match.group(1).strip()
                    link = link_match.group(1).strip()
                    articles.append({'title': title, 'link': link})
            except Exception as e:
                # Log or handle parsing errors
                pass
    return articles

def filter_articles(articles, keywords):
    filtered = []
    for article in articles:
        for keyword in keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', article['title'], re.IGNORECASE):
                filtered.append(article)
                break
    return filtered