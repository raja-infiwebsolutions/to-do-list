from django.shortcuts import render, redirect
from .forms import UserForm

# Create your views here.
def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = UserForm()
    return render(request, 'form.html', {'form': form})