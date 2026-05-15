from django.shortcuts import render, redirect
from .forms import UserFormDataForm

# Create your views here.
def user_form_view(request):
    if request.method == 'POST':
        form = UserFormDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserFormDataForm()
    return render(request, 'form.html', {'form': form})