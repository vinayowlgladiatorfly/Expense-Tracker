from django.shortcuts import render, redirect
from .models import Profile, Expense
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Fetch the profile of the current user
    profile = Profile.objects.filter(user=request.user).first()
    expenses = Expense.objects.filter(user=request.user)

    if request.method == 'POST':
        text = request.POST.get('text')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')

        # Ensure the amount is converted to a float
        try:
            amount = float(amount)
        except ValueError:
            amount = 0

        # Create a new expense and associate it with the current user
        expense = Expense(user=request.user, amount = amount, name=text, expense_type=expense_type)
        expense.save()

        # Update profile balance and expenses
        if expense_type == "Positive":
            profile.balance += float(amount)
        else:
            profile.expenses += float(amount)
            profile.balance -= float(amount)

        profile.save()
        return redirect('/')

    context = {'profile': profile, 'expenses': expenses}
    return render(request, 'index.html', context)



