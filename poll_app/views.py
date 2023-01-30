from django.shortcuts import render
from .forms import LoginForm,SignupForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import socket


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            messages.error(request,'Invalid credential!')
            
    return render(request,'login.html', {'form': LoginForm})


            
def logout_user(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(len(password))
            if len(password) >= 8:
                try:
                    checkuser = User.objects.get(username = username)
                    messages.add_message(request,messages.INFO,'User already exist!')
                    return redirect('signup')
                except:
                    user = User(username=username, email=email, password = password)
                    user.save()
                    login(request,user)
                    return redirect('home')
            messages.add_message(request,messages.INFO,'Password should be at least 8 characters!')
            return redirect('signup')

                
            
            
    return render(request, 'signup.html', {'form': SignupForm})




def home(request):
    if request.user.is_authenticated:

        user = User.objects.get(username = request.user.username)
        polls = Question.objects.filter(user=user)
        total_poll = polls.count()
        ongoing_poll = Question.objects.filter(user=user,status=True)
        ongoing_poll = ongoing_poll.count()
        total_votes = 0
        answer = []
        
        for poll in polls:
            ans = Answer.objects.filter(title=poll)
            for a in ans:
                answer.append(a)
                total_votes = total_votes + a.votes
        
        return render(request, 'home.html',{'user':user, 'polls':polls,'ongoing_poll':ongoing_poll,'total_poll':total_poll, 'total_votes':total_votes,'ans':answer})

    return redirect('login')


def live_vote(request):
    if request.user.is_authenticated:
         if request.method == 'GET':
            user = User.objects.get(username = request.user.username)
            polls = Question.objects.filter(user = user)
            answer = []
            lifetime_votes = 0
            for poll in polls:
                ans = Answer.objects.filter(title=poll)
                votes = 0
                for a in ans:
                    votes = votes + a.votes
                lifetime_votes = lifetime_votes + votes
                answer.append({'id':poll.id,'total_votes':votes,'poll_status':poll.status,'lfvotes':lifetime_votes})
        
            return JsonResponse({'ans':list(answer)})
    return redirect('login')
        
        

def create_poll(request):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.username)
        polls = Question.objects.filter(user=user)
        total_poll = polls.count()
        ongoing_poll = Question.objects.filter(user=user,status=True)
        ongoing_poll = ongoing_poll.count()
        total_votes = 0
        
        for poll in polls:
            ans = Answer.objects.filter(title=poll)
            for a in ans:
                total_votes = total_votes + a.votes
        return render(request, 'create_poll.html', {'user':user, 'polls':polls,'ongoing_poll':ongoing_poll,'total_poll':total_poll, 'total_votes':total_votes})
    return redirect('login')

def save_poll(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # For dashboard content
            user = User.objects.get(username = request.user.username)
            polls = Question.objects.filter(user=user)
            total_poll = polls.count()
            ongoing_poll = Question.objects.filter(user=user,status=True)
            ongoing_poll = ongoing_poll.count()
            total_votes = 0
            
            for poll in polls:
                ans = Answer.objects.filter(title=poll)
                for a in ans:
                    total_votes = total_votes + a.votes
            
            # For dashboard content
            
            title = request.POST.get('title')
            
            allow_comment = request.POST.get('allow_comment')

            comment = False
            if allow_comment == 'on':
                comment = True
            user = User.objects.get(username = request.user.username)
            title_model = Question(user=user, title = title, allow_comment=comment)
            title_model.save()
    
            
            num = 1
            while True:
                option = request.POST.get('option'+str(num))
                if option is not None:
                    option_model = Answer(title=title_model,option=option,votes=0)
                    option_model.save()
                    num = num +1
                else:
                    break
                
            
    
            
            return render(request,'poll_saved.html', {'user':user, 'polls':polls,'ongoing_poll':ongoing_poll,'total_poll':total_poll, 'total_votes':total_votes,'poll':title_model})
        return redirect('create_poll')

    return redirect('login')
        
def delete_poll(request,id):
    if request.user.is_authenticated:
        poll = Question.objects.get(id=id)
        poll.delete()
        return redirect('home')
    return redirect('login')
    
def activate_poll(request,id):
    if request.user.is_authenticated:
        poll = Question.objects.get(id=id)
        poll.status = True
        poll.save()
        return redirect('home')
    return redirect('login')
    
@csrf_exempt
def poll_action(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'deactivate_poll':
                print(action)
                poll = Question.objects.get(id=id)
                poll.status = False
                poll.save()

                return JsonResponse({'status':'ok'})
            
            elif action == 'activate_poll':
                poll = Question.objects.get(id=id)
                poll.status = True
                poll.save()

                return JsonResponse({'status':'ok'})
            
            elif action == 'delete_poll':
                poll = Question.objects.get(id=id)
                print(action)
                poll.delete()
                return redirect('home')
    
            
    if request.method == 'POST': 
        action = request.POST.get('action')      
        if action == 'post_comment':
            name = request.POST.get('name')
            comment = request.POST.get('comment')
            poll = Question.objects.get(id=id)
            new_commment = Comment(title=poll, name=name, comment=comment)
            new_commment.save()
            return JsonResponse({'status':'ok'})     
    return redirect('login')   

    
    
def polling(request,id):
    try:
        poll = Question.objects.get(id=id)
        if poll.status == True:
            ans = Answer.objects.filter(title=poll)
            comments = Comment.objects.filter(title=poll)
            ip = socket.gethostname()
            ip_add = socket.gethostbyname(ip)
            try:
                voter = Voter.objects.get(title=poll,ip_address = ip_add)
            except:
                voter = None
            total_votes = 0
            for a in ans:
                total_votes = total_votes + a.votes
                
            return render(request,'polling.html', {'poll':poll,'ans':ans,'comments': comments,'voter':voter,'total_votes':total_votes})
        
        return render(request,'polling.html', {'poll':None,'ans':None,'comments':None})
    except Exception as e:
        return render(request,'polling.html', {'poll':None,'ans':None,'comments':None})
    
def like_poll(request,id):
    poll = Question.objects.get(id=id)
    ip = socket.gethostname()
    ip_add = socket.gethostbyname(ip)
    voter = Voter.objects.get(ip_address=ip_add)
    voter.like = True
    voter.save()
    poll.likes = poll.likes + 1
    poll.save()
    return JsonResponse({'likes':poll.likes})
    
    
    
@csrf_exempt
def vote_count(request,id):
    if request.method == 'POST':
        ip = socket.gethostname()
        ip_add = socket.gethostbyname(ip)
        title = Question.objects.get(id=id)
        voter = Voter.objects.filter(title=title,ip_address=ip_add)
        print(len(voter))
        if voter is None or len(voter) == 0:
            print('working')
            answer = request.POST.get('answer')
            answer = Answer.objects.get(id=answer)
            title = Question.objects.get(id=id)
            answer.votes = answer.votes + 1
            voter = Voter(title=title,option=answer,ip_address=str(ip_add))
            voter.save()
            answer.save()
            return JsonResponse({'ok':'ok'})
        messages.error(request,'You already voted!')
        return redirect('polling/'+str(id))


def poll_detail(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.username)
        polls = Question.objects.filter(user=user)
        total_poll = polls.count()
        ongoing_poll = Question.objects.filter(user=user,status=True)
        ongoing_poll = ongoing_poll.count()
        total_votes = 0
        answer = []
        
        for poll in polls:
            ans = Answer.objects.filter(title=poll)
            for a in ans:
                answer.append(a)
                total_votes = total_votes + a.votes
                
        poll = Question.objects.get(id=id)
        responses = Answer.objects.filter(title=poll)

        
        return render(request, 'poll_detail.html',{'user':user, 'poll':poll,'ongoing_poll':ongoing_poll,'total_poll':total_poll, 'total_votes':total_votes,'answers':responses})

    return redirect('login')


def live_poll_detail(request, id):
    if request.user.is_authenticated:
        poll = Question.objects.get(id=id)
        options = Answer.objects.filter(title=poll)
        
        comments_models = Comment.objects.filter(title=poll)
        answers = []
        for a in options:
            answers.append({'id':a.id, 'votes':a.votes,})
        
        
        comments = []
        for comment in comments_models:
            comments.append({'name':comment.name,'comment':comment.comment})

        return JsonResponse({'answers':list(answers),'comments':list(comments),'likes':poll.likes})
    return redirect('login')


def search(request):
    if request.user.is_authenticated:
        query = request.POST.get('query')
        polls = []
        user = User.objects.get(username=request.user.username)
        all_polls = Question.objects.filter(user=user)
        for poll in all_polls:
            if str(query).lower() in str(poll.title).lower() or str(query).lower() in str(poll.likes).lower():
                print(poll)
                polls.append(poll)
                
            
                user = User.objects.get(username = request.user.username)
                
        pl = Question.objects.filter(user=user)
        total_poll = pl.count()
        ongoing_poll = Question.objects.filter(user=user,status=True)
        ongoing_poll = ongoing_poll.count()
        total_votes = 0
        answer = []
        
        for poll in pl:
            ans = Answer.objects.filter(title=poll)
            for a in ans:
                answer.append(a)
                total_votes = total_votes + a.votes
        
        return render(request, 'home.html',{'user':user, 'polls':polls,'ongoing_poll':ongoing_poll,'total_poll':total_poll, 'total_votes':total_votes,'ans':answer})
        
        
        
        
    return redirect('login')