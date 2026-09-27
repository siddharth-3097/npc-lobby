import random

from .models import Karma, QuizAttempt, QuizQuestion

QUESTIONS_PER_ATTEMPT = 10


def pick_quiz_questions(count=QUESTIONS_PER_ATTEMPT):
    """`count` random questions, at most one per movie/show, so a single
    playthrough never repeats a title.
    """
    movie_titles = list(
        QuizQuestion.objects.filter(active=True).values_list("movie_title", flat=True).distinct()
    )
    random.shuffle(movie_titles)
    chosen_titles = movie_titles[:count]

    questions = []
    for title in chosen_titles:
        pool = list(QuizQuestion.objects.filter(active=True, movie_title=title))
        questions.append(random.choice(pool))

    random.shuffle(questions)
    return questions


def serialize_question(question):
    return {
        "id": question.id,
        "movie_title": question.movie_title,
        "style": question.style,
        "prompt": question.prompt,
        "options": {"a": question.option_a, "b": question.option_b, "c": question.option_c},
        "correct_option": question.correct_option,
    }


def leaderboard_rows(limit=50):
    return list(QuizAttempt.objects.all()[:limit])


def record_attempt(name, email, score, total):
    """First-ever submission per email locks in the score and awards a
    one-time +3 karma. Replays don't change the score or earn more karma,
    since by the time someone's played through, they've already seen every
    correct answer.
    """
    email = email.strip().lower()
    attempt, created = QuizAttempt.objects.get_or_create(
        email=email,
        defaults={"name": name, "score": score, "total_questions": total},
    )
    if created:
        Karma.add(email, 3)
    return attempt, created
