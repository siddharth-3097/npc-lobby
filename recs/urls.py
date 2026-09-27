from django.urls import path

from . import views

app_name = "recs"

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.list_view, name="list"),
    path("api/submit/", views.submit_recommendation, name="submit"),
    path("api/send-list/", views.send_list, name="send_list"),
    path("api/thank-you/", views.thank_you, name="thank_you"),
    path("api/invite/", views.invite_friend, name="invite"),
    path("api/karma/", views.check_karma, name="check_karma"),
    path("api/cron/weekly-tier-progress/", views.cron_weekly_tier_progress, name="cron_weekly_tier_progress"),
    path("quiz/", views.quiz_view, name="quiz"),
    path("quiz/api/questions/", views.quiz_questions_api, name="quiz_questions_api"),
    path("quiz/api/submit/", views.quiz_submit, name="quiz_submit"),
    path("quiz/test/", views.quiz_test_view, name="quiz_test"),
]
