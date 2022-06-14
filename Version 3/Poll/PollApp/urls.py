from django.urls import include, path
from PollApp.views import all_Polls, home,create_poll,poll_result,add_option,delete_option,poll_created, signin, signout, signup, vote_option, voted
from PollApp.views import vote_ask_id,vote
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name="home"),

    # POLL BLOG
    path('allPolls/',all_Polls,name="all_Polls"),



    # POLL CREATION 
    path('create_poll/',create_poll,name="create_poll"),
    path('add_options',add_option,name="add_option"),
    path('<int:id>',delete_option,name="delete_option"),
    path('created/',poll_created,name="poll_created"),

    # POLL VOTING
    path('vote_ask_id/',vote_ask_id,name="vote_ask_id"),
    path('vote/',vote,name="vote"),
    path('voted/',voted,name="voted"),
    path('vote/<int:id>',vote_option,name="vote_option"),

    # POLL RESULT
    path('result/',poll_result,name="results"),

    path("signup/",signup,name="signup"),
    path("signin/",signin,name="signin"),
    path("signout/",signout,name="signout"),

    path("accounts/",include('allauth.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
