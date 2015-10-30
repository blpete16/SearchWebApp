from django.shortcuts import render
from QueryObj import QueryObj

# Create your views here.

def index(request):
    context = {}
    return render(request, 'searchapp/frontpage.html',context)

def gosearch(request):
    rawquery = request.POST['textquery']
    qo = QueryObj(rawquery)
    resultlist = qo.execute()
    context = {'resultlist':resultlist}
    return render(request, 'searchapp/results.html', context)
