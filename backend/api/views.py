import datetime
import json
import os
import random
import string
import re
import math
import operator
from api.ranked_retrieval import handle_indexes, calculate_query_tf_idf, calculate_doc_scores
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from persiantools.jdatetime import JalaliDate
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from api.basic_text_processes import remove_punctuation, get_learning_datas, text_processing

import api.make_main_index
from .models import News, Match, Team, Video, ConfirmationCode, FavoriteTeams


# Create your views here.
def get_news(request):
    news = News.objects.all().order_by('-news_date')
    news_arr = []
    for n in news:
        news_arr.append({'id': n.id, 'title': n.title})
    return JsonResponse({'news': news_arr})


def get_hottest_news(request):
    news = News.objects.filter(is_hot=True)
    news_arr = []
    for n in news:
        news_arr.append({'id': n.id, 'title': n.title, 'image': n.image.url})
    return JsonResponse({'news': news_arr})


def get_news_detail(request, news_id):
    news = News.objects.get(id=news_id)
    players_label = []
    teams_label = []
    for player in news.players_label.all():
        players_label.append({'id': player.id, 'name': player.name})
    for team in news.team_label.all():
        teams_label.append({'id': team.id, 'name': team.name})
    return JsonResponse(
        {'title': news.title, 'image': news.image.url, 'text': news.text, 'players_label': players_label,
         'teams_label': teams_label})


def get_news_filter_player(request, player_id):
    news = News.objects.filter(players_label__id=player_id)
    news_arr = []
    for n in news:
        news_arr.append({'id': n.id, 'title': n.title, 'image': n.image.url})
    videos = Video.objects.filter(players_label__id=player_id)
    videos_arr = []
    for video in videos:
        videos_arr.append({'id': video.id, 'title': video.title, 'image': video.image.url})
    return JsonResponse({'news': news_arr, 'videos': videos_arr})


def get_news_filter_team(request, team_id):
    news = News.objects.filter(team_label__id=team_id)
    news_arr = []
    for n in news:
        news_arr.append({'id': n.id, 'title': n.title, 'image': n.image.url})
    videos = Video.objects.filter(team_label__id=team_id)
    videos_arr = []
    for video in videos:
        videos_arr.append({'id': video.id, 'title': video.title, 'image': video.image.url})
    return JsonResponse({'news': news_arr, 'videos': videos_arr})


def get_live_score(request):
    today = datetime.datetime.today()
    matches = Match.objects.all()
    matches_arr = []
    for n in matches:
        match_date = datetime.datetime(n.match_date.year, n.match_date.month, n.match_date.day, n.match_date.hour,
                                       n.match_date.minute)
        today_or_not = False
        if match_date + datetime.timedelta(hours=3, minutes=30) < datetime.datetime(
                today.year, today.month, today.day, 0, 0) - datetime.timedelta(days=1):
            continue
        if match_date + datetime.timedelta(hours=3, minutes=30) >= datetime.datetime(
                today.year, today.month, today.day, 0, 0):
            today_or_not = True
        matches_arr.append({'match_date': str(JalaliDate(n.match_date + datetime.timedelta(hours=3, minutes=30))),
                            'time': (n.match_date + datetime.timedelta(hours=3, minutes=30)).time(),
                            'host': n.host.name, 'guest': n.guest.name, 'host_score': n.host_score,
                            'guest_score': n.guest_score, 'today': today_or_not, 'finished': n.finished,
                            'League': n.host.league.name})
    return JsonResponse({'matches': matches_arr})


def get_matches(request):
    matches = Match.objects.all()
    matches_arr = []
    for n in matches:
        matches_arr.append({'match_date': str(JalaliDate(n.match_date)),
                            'time': (n.match_date + datetime.timedelta(hours=3, minutes=30)).time(),
                            'host': n.host.name, 'guest': n.guest.name, 'host_score': n.host_score,
                            'guest_score': n.guest_score, 'finished': n.finished, 'League': n.host.league.name,
                            'week': n.week})
    return JsonResponse({'matches': matches_arr})


def get_max_fixture_leagues(request):
    max_premier_league = Match.objects.filter(host__league__name='لیگ برتر انگلیس').aggregate(Max('week'))['week__max']
    max_laliga = Match.objects.filter(host__league__name='لالیگا').aggregate(Max('week'))['week__max']
    max_bundesliga = Match.objects.filter(host__league__name='بوندسلیگا').aggregate(Max('week'))['week__max']
    max_seria_a = Match.objects.filter(host__league__name='سری آ').aggregate(Max('week'))['week__max']
    return JsonResponse({'premierLeague': max_premier_league, 'laliga': max_laliga, 'bundesliga': max_bundesliga,
                         'serieA': max_seria_a})


def get_standings(request):
    teams = Team.objects.all()
    teams_arr = []
    for t in teams:
        teams_arr.append({'name': t.name, 'league': t.league.name, 'score': t.score})
    return JsonResponse({'teams': teams_arr})


def get_videos(request):
    videos = Video.objects.all()
    videos_arr = []
    for v in videos:
        videos_arr.append({'id': v.id, 'title': v.title, 'image': v.image.url})
    return JsonResponse({'videos': videos_arr})


def get_video(request, video_id):
    video = Video.objects.get(id=video_id)
    players_label = []
    teams_label = []
    for player in video.players_label.all():
        players_label.append({'id': player.id, 'name': player.name})
    for team in video.team_label.all():
        teams_label.append({'id': team.id, 'name': team.name})
    return JsonResponse(
        {'title': video.title, 'content': video.content.url, 'players_label': players_label,
         'teams_label': teams_label})


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(length))
    return result


@api_view(['POST'])
def get_confirmation_code(request):
    body = json.loads(request.body)
    email = body['email']
    conf_code_qs = ConfirmationCode.objects.filter(email=email)
    if len(conf_code_qs) != 0:
        conf_code_qs.delete()
    confirmation_code = get_random_string(6)
    conf_code_record = ConfirmationCode()
    conf_code_record.code = confirmation_code
    conf_code_record.email = email
    send_mail(
        'Arman Varzesh: Confirmation Code',
        'Your confirmation code is : ' + confirmation_code,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    conf_code_record.save()
    return HttpResponse(status=200)


@api_view(['POST'])
def check_confirmation_code(request):
    body = json.loads(request.body)
    sent_conf_code = body['confirmationcode']
    email = body['email']
    confcode_queryset = ConfirmationCode.objects.filter(email=email)
    if len(confcode_queryset) == 0:
        return HttpResponseBadRequest()
    saved_conf_code = confcode_queryset[0]
    if saved_conf_code.code == sent_conf_code:
        saved_conf_code.verified = True
        saved_conf_code.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


@api_view(['POST'])
def set_password(request):
    body = json.loads(request.body)
    email = body['email']
    password = body['password']
    confcode_queryset = ConfirmationCode.objects.filter(email=email)
    if len(confcode_queryset) == 0:
        return HttpResponseBadRequest()
    if not confcode_queryset[0].verified:
        return HttpResponseBadRequest()
    try:
        User.objects.create_user(username=email, email=email, password=password)  # ****************
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=403)


@api_view(['POST'])
def login_view(request):
    body = json.loads(request.body)
    email = body['email']
    password = body['password']
    user = authenticate(request, username=email, password=password)
    if user is not None:
        token_query_set = Token.objects.filter(user=user)
        if len(token_query_set) != 0:
            token_query_set.delete()
        token = Token.objects.create(user=user)
        return JsonResponse({'token': token.key})
    else:
        return HttpResponse(status=403)


def forgotpassword(request):
    body = json.loads(request.body)
    email = body['email']
    user_qs = User.objects.filter(email=email)
    if len(user_qs) == 0:
        return HttpResponseBadRequest()
    new_password = get_random_string(8)
    user_qs[0].set_password(new_password)
    send_mail(
        'Arman Varzesh: password',
        'Your password is : ' + new_password,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    user_qs[0].save()
    return HttpResponse(status=200)


def get_teams(request):
    teams = Team.objects.all()
    teams_arr = []
    for t in teams:
        teams_arr.append({'id': t.id, 'name': t.name})
    return JsonResponse({'teams': teams_arr})


def search_boolean(request):
    body = json.loads(request.body)
    query = remove_punctuation(body['query'])
    learning_words = get_learning_datas()
    refined_query = []
    docs_for_each_word_in_query = {}
    for word in query:
        word = text_processing(word, learning_words)
        if (not word is None) and (not word in refined_query):
            refined_query.append(word)
    with open(os.path.join(settings.BASE_DIR, "api/indexes/main_index.txt"), encoding='utf-8') as fp:
        for i, line in enumerate(fp):
            if i == 0:
                continue
            for word in refined_query:
                if word == line.split(' ')[0]:
                    docs_for_each_word_in_query[word] = []
                    first_bracket_pos = line.find('[')
                    docs = re.findall(r'\d+', line[first_bracket_pos + 1:-2:1])[0::2]
                    for doc in docs:
                        docs_for_each_word_in_query[word].append(int(doc))
                    break
    with open(os.path.join(settings.BASE_DIR, "api/indexes/aux_index.txt"), encoding='utf-8') as fp:
        for i, line in enumerate(fp):
            if i == 0:
                continue
            for word in refined_query:
                if word == line.split(' ')[0]:
                    if not word in docs_for_each_word_in_query:
                        docs_for_each_word_in_query[word] = []
                    first_bracket_pos = line.find('[')
                    docs = re.findall(r'\d', line[first_bracket_pos + 1:-2:1])[0::2]
                    for doc in docs:
                        docs_for_each_word_in_query[word].append(int(doc))
                    break
    if len(docs_for_each_word_in_query) != len(refined_query):
        return HttpResponse(status=404)
    common_docs = []
    for word, docs in docs_for_each_word_in_query.items():
        if not common_docs:
            common_docs = docs
        else:
            common_docs = set(common_docs).intersection(docs)
    common_docs = list(common_docs)
    if common_docs == []:
        return HttpResponse(status=404)
    else:
        news = News.objects.filter(pk__in=common_docs)
        news_arr = []
        for n in news:
            news_arr.append({'id': n.id, 'title': n.title, 'image': n.image.url})
        return JsonResponse({'news': news_arr})


def ranked_retrieval(request):
    scores = {}
    body = json.loads(request.body)
    query = remove_punctuation(body['query'])
    learning_words = get_learning_datas()
    refined_query = {}
    df_for_each_term_in_query = {}
    num_of_docs = 0
    docs_length = {}
    tf_document_term = {}
    for word in query:
        word = text_processing(word, learning_words)
        if not word is None:
            if word in refined_query:
                refined_query[word] += 1
            else:
                refined_query[word] = 1
    num_of_docs, scores, docs_length, df_for_each_term_in_query, tf_document_term = handle_indexes(
        os.path.join(settings.BASE_DIR, "api/indexes/main_index.txt"), num_of_docs, scores, docs_length,
        refined_query, df_for_each_term_in_query,
        tf_document_term)
    num_of_docs, scores, docs_length, df_for_each_term_in_query, tf_document_term = handle_indexes(
        os.path.join(settings.BASE_DIR, "api/indexes/aux_index.txt"), num_of_docs, scores, docs_length,
        refined_query, df_for_each_term_in_query,
        tf_document_term)
    for doc in docs_length:
        docs_length[doc] = math.sqrt(docs_length[doc])
    refined_query = calculate_query_tf_idf(refined_query, df_for_each_term_in_query, num_of_docs)

    scores = calculate_doc_scores(tf_document_term, scores, refined_query, docs_length)
    top_ten_docs = get_top_ten(scores)
    news = []
    for doc_id in top_ten_docs:
        news.append(News.objects.get(id=doc_id))
    news_arr = []
    for n in news:
        news_arr.append({'id': n.id, 'title': n.title, 'image': n.image.url})
    return JsonResponse({'news': news_arr})


def sort_descending(d):
    sorted_d = dict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_d


def get_top_ten(d):
    d = sort_descending(d)
    top_ten = []
    for i, doc_id in enumerate(d):
        if i == 10:
            break
        top_ten.append(doc_id)
    return top_ten


@api_view(('POST',))
@permission_classes((permissions.IsAuthenticated,))
def select_favorite_team(request):
    body = json.loads(request.body)
    favorite_team_id = body['favoriteTeam']
    user = request.user
    if FavoriteTeams.objects.filter(user=user).exists():
        FavoriteTeams.objects.filter(user=user).delete()
    try:
        team = Team.objects.get(id=favorite_team_id)
    except Team.DoesNotExist:
        return HttpResponseBadRequest()
    favorite_team = FavoriteTeams(user=user, team=team)
    favorite_team.save()
    return HttpResponse(status=200)


@api_view(('POST',))
@permission_classes((permissions.IsAuthenticated,))
def logout(request):
    user = request.user
    Token.objects.get(user=user).delete()
    return HttpResponse(status=200)


@api_view(('GET',))
@permission_classes((permissions.IsAuthenticated,))
def get_favorite_team_news(request):
    user = request.user
    try:
        favorite_team = FavoriteTeams.objects.get(user=user)
    except FavoriteTeams.DoesNotExist:
        return HttpResponseNotFound()
    team = favorite_team.team
    news = team.news_set.filter(news_date__gte=datetime.datetime.now() - datetime.timedelta(days=2))
    news_arr = []
    for n in news:
        news_arr.append({'id': n.id, 'title': n.title, 'image': n.image.url})
    return JsonResponse({'news': news_arr, 'favoriteTeam': favorite_team.team.name})

