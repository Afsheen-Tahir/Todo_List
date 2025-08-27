
from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
path('',TemplateView.as_view(template_name='Outer/index.html') ,name="Main"),
   path('Done',views.Done,name="Done"),
   path('Home',views.Home,name="Home"),
   path('register/',views.registration,name="register"),
   path('Login/',views.Login,name="Login"),
   path('Logout/',views.Logout,name="Logout"),
   path('Detail',views.Detail,name="Detail"),
 path("contact/", views.contact, name="contact"),
   path('Delete/<int:id>',views.Delete,name="Delete"),
   path('Update/<int:id>',views.Update,name="update"),
   path('Add',views.Add,name="Add"),
]
