from django.shortcuts import render
from QueryObj import QueryObj

# Create your views here.

def index(request):
    context = {}
    return render(request, 'searchapptwo/frontpage.html',context)

def gosearch(request):
    rawquery = request.POST['textquery']
    qo = QueryObj(rawquery)
    resultlist = qo.execute()
    RC=len(resultlist)
    ErrorMsg=""
    if (RC==0):
	ErrorMsg="You may need to shorten your query or use synonyms."
    context = {'resultlist':resultlist,'resultcount':RC, 'ErrorMsg':ErrorMsg}
    return render(request, 'searchapptwo/results.html', context)
