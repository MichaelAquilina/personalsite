from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from polls.models import Question, Choice

# Create your views here.
def index(request):
    return render(
        request,
        'polls/index.html',
        {'latest_question_list': Question.objects.order_by('-pub_date')[:5]}
    )


def details(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    else:
        return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': 'You didnt select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
