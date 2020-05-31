from django.urls import path
from . import views

urlpatterns = [
    # main
    path('', views.VariantsView.as_view()),

    # total
    path('<int:pk>_type_tasks/', views.TypeOfTasksView.as_view()),
    path('search/', views.OneTaskByIdView.as_view(), name='search'),

    # user
    path('id<int:pk>/', views.UserPageView.as_view(), name='user_page'),
    path('id<int:pk>/change', views.ChangeUserPage, name='change_user_page'),

    # Variant view
    path('<int:pk>_variant_step_1/', views.SolvingOneVariant, name='variant_page_1'),
    path('<int:pk>_variant_step_3/', views.TotalSolvigVariant, name='variant_result'),

    # auth
    path('registration/', views.registrPage, name='registration'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]