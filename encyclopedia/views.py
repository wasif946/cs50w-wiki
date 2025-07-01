from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from . import util
from .forms import EntryForm
import random
import markdown2
import os

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return HttpResponseNotFound("Entry not found")
    
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get('q', '')
    if not query:
        return redirect('index')
    
    entries = util.list_entries()
    # Check for exact match
    if query.lower() in [entry.lower() for entry in entries]:
        return redirect('entry', title=query)
    
    # Find partial matches
    matches = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "matches": matches,
        "query": query
    })

def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "Entry already exists"
                })
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        form = EntryForm()
    return render(request, "encyclopedia/create.html", {
        "form": form
    })

def edit(request, title):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return HttpResponseNotFound("Entry not found")
        form = EntryForm(initial={"title": title, "content": content})
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

def random_page(request):
    entries = util.list_entries()
    if not entries:
        return redirect('index')
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)