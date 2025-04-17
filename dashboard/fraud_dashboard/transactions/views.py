from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from .models import SuspiciousTransaction  # Import the model
from django.shortcuts import render  # Import render function
from django.db.models import Q
from django.utils.dateparse import parse_date

def dashboard(request):
    transactions = SuspiciousTransaction.objects.all().order_by('-date')

    # Filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    rule = request.GET.get('rule')
    reviewed = request.GET.get('reviewed')
    search = request.GET.get('search')
    if search:
        transactions = transactions.filter(
            Q(account_number__icontains=search) |
            Q(transaction_id__icontains=search) |
            Q(rule_triggered__icontains=search)
        )
    if start_date:
        transactions = transactions.filter(date__date__gte=parse_date(start_date))
    if end_date:
        transactions = transactions.filter(date__date__lte=parse_date(end_date))
    if min_amount:
        transactions = transactions.filter(amount__gte=min_amount)
    if max_amount:
        transactions = transactions.filter(amount__lte=max_amount)
    if rule:
        transactions = transactions.filter(rule_triggered__icontains=rule)
    if reviewed in ['true', 'false']:
        transactions = transactions.filter(is_reviewed=(reviewed == 'true'))

    context = {
        'transactions': transactions,
        'filters': request.GET
    }
    return render(request, 'transactions/dashboard.html', context)

def dashboard(request):
    from django.conf import settings
    print("Template DIRS:", settings.TEMPLATES[0]['DIRS'])  # debug line
    
    try:
        template = get_template('transactions/dashboard.html')
    except TemplateDoesNotExist:
        print("TEMPLATE NOT FOUND")
    transactions = SuspiciousTransaction.objects.all()
    return render(request, 'transactions/dashboard.html', {'transactions': transactions})
