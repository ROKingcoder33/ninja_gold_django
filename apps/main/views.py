from django.shortcuts import render, redirect
import random
import datetime

# Create your views here.
now = datetime.datetime.now().strftime("%I:%M%p %b-%d-%Y")

def index(request):
    try:
        request.session['goldTotal']
        request.session['activity']
    except KeyError:
        request.session['goldTotal'] = 0
        request.session['activity'] = []
    context = {
        'title': 'Ninja Gold',
        'gold': request.session['goldTotal'],
        'activity': request.session['activity'],
    }
    return render(request, 'main/index.html', context)

def process_money(request):
    if request.method != "POST":
        return redirect('/')

    building = request.POST['building']
    if building == 'farm':
        getGold = random.randrange(10, 20)
    elif building == 'cave':
        getGold = random.randrange(5, 10)
    elif building == 'house':
        getGold = random.randrange(2, 5)
    elif building == 'casino':
        getGold = random.randrange(-50, 50)

    if getGold > 0:
        result = {
            'history': "You earned " + str(getGold) + " in gold (" + str(now) + ")",
            'font_color': 'green'
        }
    else: 
        result = {
            'history': "You lost " + str(getGold) + " in gold (" + str(now) + ")",
            'font_color': 'red'
        }
        
    request.session['goldTotal'] = int(request.session['goldTotal']) + getGold
    if len(request.session['activity']) >= 9:
        request.session['activity'].insert(0, result)
        request.session['activity'].pop(0)
    else:
        request.session['activity'].insert(0, result)
    request.session.modified = True
    return redirect('/')


def reset(request):
    request.session.clear()
    request.session.modified = True
    return redirect('/')
