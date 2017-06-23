import time

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView

from widgets.forms import RegistrationForm
from widgets.models import BackgroundImages, Widget, UsersWidgets


def home(request):
    return render(request, 'home.html')


@login_required
def personalized(request):
    user = request.user

    backgrounds = BackgroundImages.objects.all()
    featured_widgets = Widget.objects.filter(is_featured=True)
    selected_users_widgets = UsersWidgets.objects.filter(user=user)
    user_background = request.user.background.image.url if request.user.background else ''

    top_widgets_ids = list(UsersWidgets.objects.values('widget_id').annotate(count=Count('id')) \
        .order_by('-count').values_list('widget_id', flat=True))
    un_sorted_widgets_objects = Widget.objects.filter(id__in=top_widgets_ids).order_by()

    un_sorted_widgets_objects = dict([(obj.id, obj) for obj in un_sorted_widgets_objects])
    top_widgets = [un_sorted_widgets_objects[id] for id in top_widgets_ids]

    # """
    # SELECT widget_id, count(1) as count from user_widget GROUP BY widget_id ORDER BY count DESC
    # """

    context = {'top_widgets': top_widgets, 'featured_widgets': featured_widgets,'backgrounds': backgrounds,
               'user': user, 'user_background': user_background, 'selected_users_widgets': selected_users_widgets}
    return render(request, 'personalized.html', context)


@login_required
def update_background(request):
    request.user.background_id = request.POST.get('background_id')
    request.user.save()

    return HttpResponse(status=201)


@login_required
def users_widgets(request):
    action = request.POST.get('action')
    widget = request.POST.get('widget_id')
    user = request.user

    if action == 'add':
        widget = request.POST.get('widget_id')
        user_widget = UsersWidgets(widget_id=widget, user=user)
        user_widget.save()
    elif action == 'remove':
        user_widget = UsersWidgets.objects.filter(id=widget)
        user_widget.delete()

    return HttpResponse(status=201)


@login_required
def update_count(request):
    widget = request.POST.get('widget_id')
    user_widget = UsersWidgets.objects.filter(user=request.user, widget_id=widget).first()
    if user_widget:
        user_widget.click_count += 1
        user_widget.save()

    return HttpResponse(status=201)


class RegistrationUserView(FormView):
    form_class = RegistrationForm

    def form_valid(self, form):
        form.instance.username = time.time()
        form.save()

        widget = Widget.objects.first()
        if widget:
            user_widget = UsersWidgets()
            user_widget.user = form.instance
            user_widget.widget = widget
            user_widget.save()

        login(self.request, form.instance)

        return redirect('/personalized')
