from textblob import TextBlob
import re


def calculate_clarity_score(text):
    sentences = TextBlob(text).sentences
    if not sentences:
        return 0.0
    
    avg_sentence_length = sum(len(str(s).split()) for s in sentences) / len(sentences)
    
    if avg_sentence_length < 5:
        return 0.3
    elif avg_sentence_length > 25:
        return 0.4
    else:
        return min(1.0, 0.5 + (15 - abs(avg_sentence_length - 15)) / 30)


def calculate_relevance_score(ai_messages, user_messages):
    if not ai_messages or not user_messages:
        return 0.3
    
    user_keywords = set()
    for msg in user_messages:
        blob = TextBlob(msg.get('text', '').lower())
        user_keywords.update([word.lower() for word in blob.words if len(word) > 3])
    
    ai_keywords = set()
    for msg in ai_messages:
        blob = TextBlob(msg.get('text', '').lower())
        ai_keywords.update([word.lower() for word in blob.words if len(word) > 3])
    
    if not user_keywords:
        return 0.5
    
    overlap = len(user_keywords.intersection(ai_keywords))
    relevance = min(1.0, 0.4 + (overlap / len(user_keywords)) * 0.6)
    return relevance


def detect_fallback_count(ai_messages):
    fallback_patterns = [
        r"i don't know",
        r"i'm not sure",
        r"i can't help",
        r"unable to",
        r"cannot assist",
        r"don't understand",
        r"not clear",
    ]
    
    count = 0
    for msg in ai_messages:
        text = msg.get('text', '').lower()
        for pattern in fallback_patterns:
            if re.search(pattern, text):
                count += 1
                break
    return count


def calculate_empathy_score(text, sentiment):
    empathy_indicators = {
        'positive': ['appreciate', 'glad', 'happy', 'pleased', 'thank'],
        'negative': ['sorry', 'apologize', 'understand', 'feel', 'concerned', 'regret'],
        'neutral': ['help', 'assist', 'support', 'here for you']
    }
    
    text_lower = text.lower()
    indicators = empathy_indicators.get(sentiment, empathy_indicators['neutral'])
    
    found_indicators = sum(1 for indicator in indicators if indicator in text_lower)
    empathy_score = min(1.0, 0.3 + (found_indicators / len(indicators)) * 0.7)
    return empathy_score


def calculate_completeness_score(ai_messages, user_messages):
    if not ai_messages:
        return 0.0
    
    question_words = ['what', 'when', 'where', 'who', 'why', 'how', 'which']
    user_questions = 0
    ai_answers = 0
    
    for msg in user_messages:
        text = msg.get('text', '').lower()
        if any(text.startswith(q) or '?' in text for q in question_words):
            user_questions += 1
    
    for msg in ai_messages:
        text = msg.get('text', '').lower()
        if len(text.split()) > 5:
            ai_answers += 1
    
    if user_questions == 0:
        return 0.7 if len(ai_messages) >= len(user_messages) else 0.5
    
    completeness = min(1.0, (ai_answers / user_questions) * 0.8 + 0.2)
    return completeness


def analyze_messages(messages):
    if not messages:
        return {
            'clarity_score': 0.0,
            'relevance_score': 0.0,
            'accuracy_score': 0.0,
            'completeness_score': 0.0,
            'sentiment': 'neutral',
            'empathy_score': 0.0,
            'avg_response_time': 2.5,
            'resolved': False,
            'escalation_needed': False,
            'fallback_count': 0,
            'overall_score': 0.0
        }

    ai_messages = [msg for msg in messages if msg.get('sender') == 'ai']
    user_messages = [msg for msg in messages if msg.get('sender') == 'user']
    
    all_text = ' '.join([msg.get('text', '') for msg in messages])
    user_text = ' '.join([msg.get('text', '') for msg in user_messages])
    
    blob = TextBlob(user_text)
    polarity = blob.sentiment.polarity

    if polarity > 0.15:
        sentiment = 'positive'
    elif polarity < -0.15:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    clarity_score = calculate_clarity_score(all_text)
    relevance_score = calculate_relevance_score(ai_messages, user_messages)
    
    accuracy_score = 0.75
    if fallback_count := detect_fallback_count(ai_messages):
        accuracy_score = max(0.4, 0.75 - (fallback_count * 0.15))
    
    completeness_score = calculate_completeness_score(ai_messages, user_messages)
    empathy_score = calculate_empathy_score(all_text, sentiment)
    
    avg_response_time = 2.5
    resolved = len(ai_messages) >= len(user_messages) and sentiment != 'negative'
    escalation_needed = (sentiment == 'negative' and len(user_messages) > 3) or fallback_count > 2

    overall_score = (
        clarity_score * 0.15 +
        relevance_score * 0.20 +
        accuracy_score * 0.15 +
        completeness_score * 0.15 +
        empathy_score * 0.15 +
        (1.0 if resolved else 0.3) * 0.20
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

