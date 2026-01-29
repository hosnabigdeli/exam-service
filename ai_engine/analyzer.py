def analyze_exam(score, total, topic_stats):
    level = "Beginner"
    if score / total > 0.7:
        level = "Intermediate"
    if score / total > 0.85:
        level = "Advanced"

    weaknesses = [t for t, v in topic_stats.items() if v < 50]

    return {
        "level": level,
        "weaknesses": weaknesses,
        "recommended_courses": [
            {"title": f"{w} Fundamentals", "platform": "Udemy"} for w in weaknesses
        ],
        "recommended_mentors": [
            {"name": f"{w} Mentor", "field": w} for w in weaknesses
        ],
        "feedback": f"سطح شما {level} است و نیاز به تقویت {', '.join(weaknesses)} دارید"
    }
