# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from photo.models import Photo
from photo.forms import PhotoEditForm

#from gensim.models import word2vec
from gensim.models import word2vec
import gensim
## word2vec


import simplejson
import decimal

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.http import HttpResponse

#import gensim
##0411_render  to response
from django.shortcuts import render_to_response
#from .form import SearchForm#(form.py--> class )
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.helper import FormHelper
#searchForm
from photo.forms import SearchForm



def single_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)

    return render(
        request,
        'photo.html',
        {
            'photo': photo,
        }
    )


def new_photo(request):
    if request.method == "GET":
        edit_form = PhotoEditForm()
    elif request.method == "POST":
        edit_form = PhotoEditForm(request.POST, request.FILES)

        if edit_form.is_valid():
            new_photo = edit_form.save()

            return redirect(new_photo.get_absolute_url())

    return render(
        request,
        'new_photo.html',
        {
            'form': edit_form,
        }
    )


def search(request):
    errors = []
    #hashes=[ ]
    #json_test=simplejson.dumps(hashes,ensure_ascii=False)
    #unicode_test=['안녕 오랜만이야!','123:새로운 하루']
    json_test={}
    unicode_test={}
    context = { 'errors': errors, 'json_test':json_test ,'unicode': unicode_test }

    if 'word1' in request.GET:

        positive      = request.GET['word1']
        print positive

        if not positive:
            errors.append('Enter a search term.')
        elif len(positive) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            """
            newsbooks = NewsData.objects.filter(Title__icontains=q) #title__icontains=q
            return render_to_response('search_results.html',                #render_to_response
                {'newsbooks': newsbooks, 'query': q})

            """

            model = word2vec.Word2Vec.load("stemming2.model")

            positive      = request.GET['word1']#['woman','king']
            #negative      = request.GET['word2']#['man']
            response_data  = model.most_similar(positive=positive ,topn=20)
            hashes        = [{"text": d[0], "size": decimal.Decimal(str(d[1])),"cost":1} for d in response_data]
            model_sim     = model.most_similar(positive=positive ,topn=10)
            json_dump = as_json(hashes)

            unicode_test=['안녕 오랜만이야!','123:새로운 하루']
            print json_dump
            json_test = simplejson.dumps(hashes,ensure_ascii=False)
            as_json(unicode_test)


            #return as_json(unicode_test)#as_json(hashes)
    return render_to_response('search_form2.html', {'errors': errors, 'json_test':json_test,'unicode': unicode_test })
    """
    return render(
                    request,
                    'search_form2.html',
                    context
                  )
    """



def index(request):

  return HttpResponse("Hello, world. You're at the polls index.")

def single_photo(request):
    variable=["안녕 오랜만이야!","123:새로운 하루"]
    json1 = simplejson.dumps(variable,ensure_ascii=False)
    return HttpResponse(json1,content_type='application/json; charset=utf-8')


#word2vec
def as_json(variable):
    json = simplejson.dumps(variable,ensure_ascii=False)
    return HttpResponse(json,content_type='application/json; charset=utf-8')
    #return render_to_response('json_test.html', {'errors': errors})


#한글이 깨질때
"""
HttpResponse(
    json_context,
    content_type=u"application/json; charset=utf-8",
    status=status)
"""

def parse_array_string(get, name):
    param = get.get(name, None)
    if param == None:
        return []
    else:
        return param.split(",")

#########################search form test 0411
def search_form1(request) :
    return render_to_response('search_form.html')

########################search_angular
def search_angular(request):
    errors = []

    hashes=[ ]
    json_test=simplejson.dumps(hashes,ensure_ascii=False)
    unicode_test=['안녕 오랜만이야!','123:새로운 하루']
    positive=[]

    if 'word1' in request.GET:

        positive      = request.GET['word1']
        print positive

        if not positive:
            errors.append('Enter a search term.')
        elif len(positive) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            """
            newsbooks = NewsData.objects.filter(Title__icontains=q) #title__icontains=q
            return render_to_response('search_results.html',                #render_to_response
                {'newsbooks': newsbooks, 'query': q})

            """

            model = word2vec.Word2Vec.load("stemming2.model")

            positive      = request.GET['word1']
            #negative      = request.GET['word2']#['man']
            response_data  = model.most_similar(positive=positive ,topn=10)
            hashes        = [{"text": d[0], "score": decimal.Decimal(str(d[1])),"cost":1} for d in response_data]
            print ("hashes__:",unicode(hashes))
            model_sim     = model.most_similar(positive=positive ,topn=10)
            json_dump = as_json(hashes)

            unicode_test=['안녕','123:새로운 하루']
            print json_dump
            json_test = simplejson.dumps(hashes,ensure_ascii=False)
            as_json(unicode_test)
            #return as_json(unicode_test)#as_json(hashes)
    return render_to_response('search_form_refine1.html', {'errors': errors, 'json_test':json_test.encode('utf-8'),'unicode': unicode_test ,'word1':positive })


############crispy_form test_0422

def crispy(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            context= {'search_form':search_form ,'search_query':search_form.cleaned_data['q']}
            #new_result = search_form.save()
            print("인풋값은,",context['search_query'])

            return render(request, 'visual_layout.html',context)

    else:
        search_form = SearchForm()
        context = {
            'search_form': search_form,
        }
        return render(
                request,
                'crispy_form.html',
                context
        )


