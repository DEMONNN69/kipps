from textblob import TextBlob


def analyze_messages(messages):
    if not messages:
        return {
            'clarity_score': 0.0,
            'relevance_score': 0.0,
            'accuracy_score': 0.0,
            'completeness_score': 0.0,
            'sentiment': 'neutral',
            'empathy_score': 0.0,
            'avg_response_time': 0.0,
            'resolved': False,
            'escalation_needed': False,
            'fallback_count': 0,
            'overall_score': 0.0
        }

    total_text = ' '.join([msg.get('text', '') for msg in messages])
    blob = TextBlob(total_text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    ai_messages = [msg for msg in messages if msg.get('sender') == 'ai']
    user_messages = [msg for msg in messages if msg.get('sender') == 'user']

    clarity_score = min(1.0, len(total_text) / 500.0)
    relevance_score = 0.7 if len(ai_messages) > 0 else 0.3
    accuracy_score = 0.75
    completeness_score = 0.8 if len(ai_messages) >= len(user_messages) else 0.5

    empathy_words = ['sorry', 'understand', 'help', 'feel', 'appreciate', 'thank']
    empathy_count = sum(1 for word in empathy_words if word in total_text.lower())
    empathy_score = min(1.0, empathy_count / 3.0)

    avg_response_time = 2.5

    resolved = len(user_messages) <= len(ai_messages)
    escalation_needed = sentiment == 'negative' and len(user_messages) > 3
    fallback_count = 0

    overall_score = (
        clarity_score * 0.15 +
        relevance_score * 0.15 +
        accuracy_score * 0.15 +
        completeness_score * 0.15 +
        empathy_score * 0.20 +
        (1.0 if resolved else 0.5) * 0.20
    )

    return {
        'clarity_score': round(clarity_score, 2),
        'relevance_score': round(relevance_score, 2),
        'accuracy_score': round(accuracy_score, 2),
        'completeness_score': round(completeness_score, 2),
        'sentiment': sentiment,
        'empathy_score': round(empathy_score, 2),
        'avg_response_time': avg_response_time,
        'resolved': resolved,
        'escalation_needed': escalation_needed,
        'fallback_count': fallback_count,
        'overall_score': round(overall_score, 2)
    }

