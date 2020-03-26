from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    return render(request, 'home.html')


def counts(request):
    full_text = request.GET['fulltext']
    word_list = full_text.split()
    dict_list_of_unique_words = {}
    for word in word_list:
        if word in dict_list_of_unique_words.keys():
            dict_list_of_unique_words[word] += 1
        else:
            dict_list_of_unique_words[word] = 1
    print(dict_list_of_unique_words)
    return render(request, 'count.html', {'fulltext': full_text, 'list_of_words': dict_list_of_unique_words})


def about(request):
    return render(request, 'about.html')