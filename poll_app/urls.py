from django.urls import path
from poll_app import views

urlpatterns = [
    path('', views.login_user , name='login'),
    path('logout', views.logout_user, name='logout'),
    path('signup/', views.signup , name='signup'),
    path('home/', views.home, name='home'),
    path('livevote/', views.live_vote, name='live_vote'),
    path('create_poll/', views.create_poll, name='create_poll'),
    path('save_poll/', views.save_poll, name='save_poll'),
    path('delete_poll/<int:id>', views.delete_poll, name='delete_poll'),
    path('activate_poll/<int:id>', views.activate_poll, name='activate_poll'),
    path('poll_action/<int:id>', views.poll_action, name='poll_action'),
    path('polling/<int:id>', views.polling , name='polling'),
    path('like_poll/<int:id>', views.like_poll , name='like_poll'),
    path('vote_count/<int:id>', views.vote_count, name='vote_count'),
    path('poll_detail/<int:id>', views.poll_detail, name='poll_detail'),
    path('live_poll_detail/<int:id>', views.live_poll_detail, name='live_poll_detail'),
    path('search/',views.search, name='search')
    
]
