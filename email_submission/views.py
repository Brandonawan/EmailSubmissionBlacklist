from django.shortcuts import render, redirect
from .models import Email

from silk.profiling.profiler import silk_profile

@silk_profile(name='Submit Email View')
def submit_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("user email:", email)

        # Extract domain from email
        domain = email.split('@')[-1]

        # Check if domain is blacklisted
        if is_domain_blacklisted(domain):
            return render(request, 'blacklisted_email.html')

        try:
            # Try to create a new Email object
            Email.objects.create(email=email)
            return redirect('success')
        except IntegrityError:
            # Handle the case where the email already exists
            return render(request, 'email_already_exists.html')

    return render(request, 'email_form.html')

@silk_profile(name='Success View')
def success(request):
    return render(request, 'success.html')

def is_domain_blacklisted(domain):
    blacklist_file_path = 'email_submission/blacklist.txt' 
    with open(blacklist_file_path, 'r') as f:
        blacklist = f.read().splitlines()
    return domain.lower() in blacklist  # Convert domain to lowercase for case-insensitive comparison
