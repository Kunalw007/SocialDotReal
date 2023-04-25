from django.urls import reverse
from django.shortcuts import render, HttpResponse,redirect
import instaloader
import joblib
import locale
from django.contrib import messages

# Create your views here.
def index(request):
    context={
        'device':'Hello world'
    }
    return render(request,"index.html",context)
    # return HttpResponse("This is Home Page")
def about(request):
    # return HttpResponse("This is about Page")
    return render(request,"about.html")

def detector(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        if(username != ''):
            return redirect('result', username=username)
        
    return render(request,"detector.html")
    
def result(request, username):
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except:
        # messages="ID not found"
        print("An exception occurred")
        messages.success(request, 'The Instagram ID entered is invalid. Please check your input and try again.')
        return redirect("detector")
    # posts_data = []
    media = profile.mediacount
    follower=profile.followers
    following=profile.followees
    profile_pic = profile.profile_pic_url
    print(profile_pic)
    str1 = "44884218_345707102882519_2446069589734326272_n.jpg"
    pp = not (str1 in profile_pic)
    hasProfile=int(pp==True)
    username = profile.username
    private = profile.is_private
    isPrivate=int(private==True)
    bio = profile.biography
    lengthbio=len(bio)
    username = profile.username
    digit = 0
    for i in username:
        if(i.isdigit()):
            digit+=1
    lengthUsername=len(profile.username)
    url = profile.external_url
    name=profile.full_name


    with open('media/logisticmodel.pkl', 'rb') as file:
        model = joblib.load(file)
    
    with open('media/knnmmodel.pkl', 'rb') as file:
        modelknn = joblib.load(file)

    with open('media/randommodel.pkl', 'rb') as file:
        modelrandom = joblib.load(file)

    # Use the model to make predictions
    result = model.predict([[follower,following,lengthbio,media,hasProfile,isPrivate,digit,lengthUsername]])
    resultknn = modelknn.predict([[follower,following,lengthbio,media,hasProfile,isPrivate,digit,lengthUsername]])
    resultrandom = modelrandom.predict([[follower,following,lengthbio,media,hasProfile,isPrivate,digit,lengthUsername]])
    followerArranged=human_format(follower)
    followingArranged=human_format(following)
    # posts_data.append({'username':username,'post':media,'bio':lengthbio,'Follower':follower,'following':following,'isPrivate':isPrivate,'profile_pic':pp,'isFake log':result[0],'isFake random':resultrandom[0],'resultknn':resultknn[0]})
    
    locale.setlocale(locale.LC_ALL, '')
    post='{:n}'.format(media)
    print(result," ",resultknn," ",resultrandom)
    reverse('result', kwargs={'username': username})
    resultfinal=result+resultknn+resultrandom
    resultfinal=resultfinal/3
    return render(request,"result.html", {'name':name,'username':username,'post':post,'Follower':followerArranged,'following':followingArranged,'bio':bio,'url':url,'profile_pic':profile_pic,'result':resultrandom})



def contactus(request):
    return render(request,"contactus.html")


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])