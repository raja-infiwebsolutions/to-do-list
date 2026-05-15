from django.shortcuts import render, redirect
from .forms import UserFormDataForm

# Display the form page
def user_form_view(request):
    if request.method == 'POST':
        form = UserFormDataForm(request.POST)
        if form.is_valid():
            form.save()  # Save valid data into the database
            return redirect('success')  # Redirect after successful submission
    else:
        form = UserFormDataForm()
    return render(request, 'form.html', {'form': form})

# Success view
def success_view(request):
    return render(request, 'success.html')