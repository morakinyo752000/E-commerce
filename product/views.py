from django.contrib import messages
from django.shortcuts import  render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from product.models import CommentForm, Comment
#
# def index(request):
#     return HttpResponse('My Product Page')



def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    # return HttpResponse(url)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id= current_user.id
            data.save()
            messages.success(request, "Your Review has been sent. Thank You for your interest")

            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


