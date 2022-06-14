from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Person, PollQuestion,Choice
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db import  IntegrityError
# Create your views here.

def home(request):
    if request.method =="POST":
        pn = request.POST.get('pollname')
        # print(request)
    return render(request,'home.html')

# ALL POLLS
def all_Polls(request):
    poll = PollQuestion.objects.all()
    # choice = []
    # for i in poll :
    #     choice.append(Choice.objects.filter(poll_question=i))
    # print(poll)
    # print(len(poll))
    # print(choice)
    # print(len(choice))
    return render(request,'all_Polls.html',{"polls" : poll})

# CREATION OF POLL
def create_poll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please SignIn First To Create A POLL")
        return redirect('signin')
    if request.method =="POST":
        created_by = request.user
        anonymous=request.POST.get('anonymous')
        poll_name=request.POST.get("pollname")
        poll_que = request.POST.get('PollQuestionText')
        poll_visiblity = request.POST.get('visible')
        poll_image=request.FILES.get('image')
        obj1 = PollQuestion(created_by=created_by,poll_name = poll_name,que_text=poll_que,que_image=poll_image,anonymous=anonymous,visiblity=poll_visiblity)
        obj1.save() 
        messages.success(request,"Poll Question Made Successfully")
        pollid = obj1.id
        request.session['pollid']= pollid
        # print(pollid)
        return redirect('add_option')
    else :
        pass
    return render(request,'create_poll.html')

# ADDITION OF OPTIONS TO POLL
def add_option(request):
    poll_id = request.session['pollid']
    # print(poll_id)
    que = PollQuestion.objects.filter(pk=poll_id)[:1].get()
    # print(que)
    # print(que[0])
    choices = Choice.objects.filter(poll_question=que)
    # return render(request,'options.html',{"que":que})
    if request.method=="POST":
        poll_option = request.POST.get('poll_option')
        poll_image = request.FILES.get('poll_image')
        if poll_image == None and poll_option == '' :
            messages.warning(request,"BOTH FIELDS EMPTY NOT ALLOWED")
        else :    
            obj = Choice(poll_question=que,choice_text=poll_option,choice_image=poll_image)
            PollQuestion.objects.filter(id=que.id).update(noofchoices=que.noofchoices+1)
            messages.success(request,"Poll Choice Made")
            obj.save()
    else :
        pass
    return render(request,'options.html',{"que":que,"choices":choices})




# DELETION OF OPTION IF REQUIRED
def delete_option(request,id):
    obj_delete = Choice.objects.filter(pk=id)
    obj_delete.delete()
    return redirect('add_option')

# POLL CREATED SUCCESSFULLY
def poll_created(request):
    pollid= request.session['pollid']
    # print(pollid)
    messages.success(request,"Poll Created")
    return render(request,"poll_created.html",{"id":pollid})

    
def vote_ask_id(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please SignIn First To VOTE")
        return redirect('signin')
    user = request.user
    # print(user.users.all())
    return render(request,"vote_ask_id.html")

def vote(request):
    if request.method=="POST" and "searchid" in request.POST:
        pollid = request.POST.get('PollID')
        if PollQuestion.objects.filter(pk=pollid) :
            pollque = PollQuestion.objects.filter(pk=pollid)[:1].get()
            pollchoices = Choice.objects.filter(poll_question=pollque)
            return render(request,"vote.html",{"pollque":pollque,"pollchoices":pollchoices})
        else :
            messages.error(request,"POLL NOT EXISTS")
            return redirect('home')
        pollque = PollQuestion.objects.filter(pk=pollid)[:1].get()
        print(pollque)
        pollchoices = Choice.objects.filter(poll_question=pollque)
        return render(request,"vote.html",{"pollque":pollque,"pollchoices":pollchoices})

    if request.method=="POST" and "vote_poll" in request.POST :
        id = request.POST.get('checkbox')
        poll_option = Choice.objects.filter(pk=id)[0:1].get()
        v = poll_option.votes
        a = poll_option.voted.all()
        print(a)
        # DONT UPDATE IF ALREADY VOTED
        if request.user in a :
            messages.success(request,"U Have Already Voted For This Choice");
            return redirect('home')
            return redirect('votechange')
            return HttpResponse('U HAVE VOTED ALREADY : | ')
        

        Choice.objects.filter(pk=id).update(votes=(v+1))
        poll_option.voted.add(request.user)
        messages.success(request,"Voted Successfully")
        return redirect('voted')

    return render(request,"vote.html")

def askingForChangeVote(request):
    return render(request,'votechange.html')
    return HttpResponse('U HAVE VOTED ALREADY : | ')
    

def vote_option(request,id):
    poll_option = Choice.objects.filter(pk=id)[0:1].get()
    v = poll_option.votes
    Choice.objects.filter(pk=id).update(votes=(v+1))
    messages.success(request,"Voted Successfully")
    return redirect('voted')

def voted(request):
    return render(request,"voted.html")
    

def poll_result(request):
    if not request.user.is_authenticated :
        messages.warning(request,"Please SignIn First To See Results")
        return redirect('signin')
    if request.method=="POST":
        curruser = request.user
        n = request.POST.get('pollNo')
        que = PollQuestion.objects.filter(pk=n)[:1].get() 
        choice = Choice.objects.filter(poll_question=que)
        return render(request,"result.html",{"que":que,"choice":choice,"curr_user":curruser})
    return render(request,"see_result.html")

def signin(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None :
            login(request,user)
            messages.success(request,"User Logged In")
            return redirect('home')
        else :
            messages.error(request,"Invalid Credentials")
    return render(request,"signin.html")

def signup(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phoneNumber')
        birthday = request.POST.get('birthday')
        fn = request.POST.get('fn')
        ln = request.POST.get('ln')
        print(username,email,fn,ln,phone,birthday)
        Password1 = request.POST.get('Password1')
        Password2 = request.POST.get('Password2')
        if Password1!=Password2:
            messages.error(request,"Check Password Again !")
            return render(request,"signup.html")
        else :
            try:
               obj = User.objects.create_user(username=username,first_name=fn,last_name=ln,email=email,password=Password1)
            except IntegrityError :
                messages.error(request,"User Already Exists With Username")
                return redirect('signup')
            else :
                Obj2 = Person(username=obj,phone=phone,birthday=birthday,email=email)
                Obj2.save()
                messages.success(request,"USER CREATED")
                return redirect('signin')
    return render(request,"signup.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged Out")
    return redirect('home')