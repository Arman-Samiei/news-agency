from django.urls import path
from api import signals
from api.rss_feed import set_rss_links_news
from . import views
from api import rss_feed


from .views import get_news, get_hottest_news, get_news_detail, get_news_filter_player, get_news_filter_team, \
    get_live_score, get_matches, get_max_fixture_leagues, get_standings, get_videos, get_video, login_view, \
    get_confirmation_code, check_confirmation_code, set_password, forgotpassword, get_teams, search_boolean, \
    select_favorite_team, logout, get_favorite_team_news, ranked_retrieval



urlpatterns = [
    path('news', get_news),
    path('hottestnews', get_hottest_news),
    path('newsdetail/<int:news_id>', get_news_detail),
    path('newsfilterplayer/<int:player_id>', get_news_filter_player),
    path('newsfilterteam/<int:team_id>', get_news_filter_team),
    path('livescore/', get_live_score),
    path('leagueMatches', get_matches),
    path('max_fixture_leagues', get_max_fixture_leagues),
    path('standings', get_standings),
    path('videos', get_videos),
    path('videos/video/<int:video_id>', get_video),
    path('users/confirmationcode', get_confirmation_code),
    path('users/checkconfirmationcode', check_confirmation_code),
    path('users/setpassword', set_password),
    path('users/login', login_view),
    path('users/forgotpassword', forgotpassword),
    path('users/favoriteteam', select_favorite_team),
    path('users/favoriteteamnews', get_favorite_team_news),
    path('users/logout', logout),
    path('teams', get_teams),
    path('booleansearch', search_boolean),
    path('rankedretrieval', ranked_retrieval),

]

