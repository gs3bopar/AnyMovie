from django.shortcuts import render
from anymovie.models import Title, Principals, Review, Favourite, History
from anymovie.methods import *
from django.core.mail import send_mail as sm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template import loader
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .forms import SignUpForm, ReviewForm
from django.db import connection
from django.http import JsonResponse
from django import forms
from datetime import datetime
from django.contrib.auth import (
    get_user_model
)
from django.core.paginator import Paginator
from django.http import QueryDict

# Create your views here.
from django.http import HttpResponse

UserModel = get_user_model()

@login_required
def home(request):
    favourites = Favourite.objects.raw(
        'select t_id, u_id, name, release_year, rating \
        from favourite natural join title \
        where u_id = %s;', [request.user.id])
    history = History.objects.raw(
        'select t_id, u_id, time, name, release_year, rating \
        from history natural join title \
        where u_id = %s \
        order by time desc \
        limit 10;', [request.user.id])
    return render(request, 'homepage.html', {
        'rating': range(1, 10),
        'favourites': favourites,
        'history': history})

@login_required
def results(request):
    name = request.GET['name_field']
    year = request.GET['year_field']
    genre = request.GET['genre_field']
    rating = request.GET['movie_rating']
    fullResult = Title.objects.raw(gen_query_search(name, year, genre, rating))

    dict = {'name_field': name, 'year_field': year, 'genre_field': genre, 'movie_rating': rating }
    query_dict = QueryDict('', mutable=True)
    query_dict.update(dict)
    query = query_dict.urlencode()

    page = request.GET.get('page', 1)
    paginator = Paginator(fullResult, 25)
    results = paginator.page(page)
    
    favourites = Favourite.objects.raw(
        'select t_id, u_id, name, release_year, rating \
        from favourite natural join title \
        where u_id = %s;', [request.user.id])

    favourites_t_ids = []
    
    for favourite in favourites:
        favourites_t_ids.append(favourite.t_id)

    return render(request, 'results.html', {'results': results, 'query': query, 'favourites_t_ids': favourites_t_ids})

@login_required
def movie(request, t_id):
    movies = Title.objects.raw('select * from title where t_id = %s;', [t_id])
    directors = Principals.objects.raw(
        'select t_id, category, name, characters \
        from principals natural join person \
        where t_id = %s and lower(category) = %s;', [t_id, 'director'])
    principals = Principals.objects.raw(
        'select t_id, category, name, characters \
        from principals natural join person \
        where t_id = %s and lower(category) <> %s \
        order by category;', [t_id, 'director'])
    reviews = Review.objects.raw(
        'select u_id, username, rating, comment, time \
        from review as r natural join custom_user \
        where r.t_id = %s \
        order by time desc \
        limit 10;', [t_id])
    # Add review if submit button was pressed
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            rating = review_form.cleaned_data.get('rating') or 'NULL'
            comment = review_form.cleaned_data.get('comment') or ''
            my_review = Review.objects.raw(
                'select u_id, username, rating, comment, time \
                from review as r natural join custom_user \
                where r.t_id = %s \
                and r.u_id = %s;', [t_id, request.user.id])

            with connection.cursor() as cursor:
                # Figure out what action to perform on the review table
                if rating != 'NULL' or comment != '':
                    # User already made a review, so his old review will be updated
                    if my_review:
                        if rating == 'NULL':
                            cursor.execute('update review \
                                            set rating = NULL, comment = %s, time = now() \
                                            where t_id = %s and u_id = %s;', [comment, t_id, request.user.id])
                        else:
                            cursor.execute('update review \
                                            set rating = %s, comment = %s, time = now() \
                                            where t_id = %s and u_id = %s;', [rating, comment, t_id, request.user.id])
                    # User is making a review for the movie for the first time
                    else:
                        if rating == 'NULL':
                            cursor.execute('insert into review \
                                            values(%s, %s, now(), NULL, %s);',
                                            [request.user.id, t_id, comment])
                        else:
                            cursor.execute('insert into review \
                                            values(%s, %s, now(), %s, %s);',
                                            [request.user.id, t_id, rating, comment])
                # If both rating and comment are empty, delete the user's review
                else:
                    # Since the user only has one review per title, we can filter for the
                    # review just based on the user id and title id alone
                    cursor.execute('delete from review \
                                    where u_id = %s and t_id = %s;',
                                    [request.user.id, t_id])
    else:
        review_form = ReviewForm()
    
    favourites = Favourite.objects.raw(
        'select t_id, u_id \
        from favourite \
        where u_id = %s and t_id = %s;', [request.user.id, t_id])

    if (len(favourites) > 0):
        favourite = True
    else:
        favourite = False

    matching_history = History.objects.raw(
        'select t_id, u_id \
        from history \
        where u_id = %s and t_id = %s;', [request.user.id, t_id])

    if (len(matching_history) > 0):
        with connection.cursor() as cursor:
            cursor.execute('update history \
                            set time = now() \
                            where t_id = %s and u_id = %s;', [t_id, request.user.id])
    else:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO history (u_id, t_id, time) \
                                VALUES (%s, %s, now());', [request.user.id, t_id])

    return render(request, 'movie.html',
        {'movies': movies,
        'directors': directors,
        'principals': principals,
        'reviews': reviews,
        'review_form': review_form,
        't_id': t_id,
        'favourite': favourite})


def get_users(email):
    # Makes the required query to fetch all the data for that required user
    active_users = UserModel._default_manager.filter(**{
        '%s__iexact' % UserModel.get_email_field_name(): email,
        'is_active': True,
    })
    return (u for u in active_users if u.has_usable_password())

def send_mail(request):
    email = request.POST.__getitem__('email')
    for user in get_users(email):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'
        current_site = get_current_site(request)
        domain = current_site.domain
        sm(
            subject = 'Password Reset',
            message = 'Please follow the instructions below.',
            html_message = loader.render_to_string("password_reset_email.html",
            {
                'username': user.username,
                'protocol': protocol,
                'domain': domain,
                'uidb64': uidb64,
                'token': token
            }),
            from_email = 'noreply@example.com',
            recipient_list = [email],
            fail_silently=False,
        )
        return render(request, 'password_reset_done.html')
        # return HttpResponse(f"Email sent to user with address as {email}.")
    return render(request, 'email_not_exist.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data.get('email') or ''
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Now when we create user we dump data to custom_user table
            # before doing form.save() check if email matches with any other previous emails
            with connection.cursor() as cursor:
                cursor.execute('SELECT count(*) FROM custom_user WHERE email = \'' + email_address + '\';')
                previous_emails = cursor.fetchone()
            if previous_emails[0] < 1:
                form.save()
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                # now insert into custom user table
                current_user = request.user
                uid = current_user.id
                # dump data to custom user
                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO custom_user (u_id, email, password, username) VALUES(\'' + str(uid) + '\', \'' + email_address + '\', \'' + raw_password + '\', \'' + username + '\');')
                return redirect('home')
            else:
                return render(request, 'email_already_exist.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def favourite_save(request):
    t_id = request.POST.get('t_id', None)
    value = request.POST.get('value', None)
    u_id = request.user.id

    if (value == 'Favourite'):
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO favourite (u_id, t_id) \
                            VALUES (%s, %s);', [u_id, t_id])
        data = {
        }
        return JsonResponse(data)
    elif (value == 'Unfavourite'):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM favourite \
                            WHERE u_id = %s and t_id = %s;', [u_id, t_id])
        data = {
        }
        return JsonResponse(data)
    else:
        return JsonResponse(data)
