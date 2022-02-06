from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def profile_view(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True
        
    context = {'form': form, 'confirm':confirm, 'profile':profile}
    return render(request, 'profiles/main.html',context )