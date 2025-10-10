from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    """
    View principal do dashboard (home page após login).
    """
    return render(request, 'dashboard/home.html', {'user': request.user})
