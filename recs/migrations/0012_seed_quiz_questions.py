from django.db import migrations

from recs.quiz_questions import QUIZ_QUESTIONS


def seed_quiz_questions(apps, schema_editor):
    QuizQuestion = apps.get_model("recs", "QuizQuestion")
    QuizQuestion.objects.bulk_create(
        QuizQuestion(**question) for question in QUIZ_QUESTIONS
    )


def remove_quiz_questions(apps, schema_editor):
    QuizQuestion = apps.get_model("recs", "QuizQuestion")
    QuizQuestion.objects.filter(
        movie_title__in={q["movie_title"] for q in QUIZ_QUESTIONS}
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("recs", "0011_quizattempt_quizquestion"),
    ]

    operations = [
        migrations.RunPython(seed_quiz_questions, remove_quiz_questions),
    ]
