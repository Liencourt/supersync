from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def apuracao(request):
        return render(request, 'apuracao_contrato/apuracao_contrato.html')
