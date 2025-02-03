from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #return HttpResponse("Rango says hey there partner!<a href=\"http://127.0.0.1:8000/rango/about\">About</a>")

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    # Return a rendered response to send to the client.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    #return HttpResponse("Rango says this is about the page!<a href = \"http://127.0.0.1:8000/rango\">Index</a>")
    return render(request, 'rango/about.html')