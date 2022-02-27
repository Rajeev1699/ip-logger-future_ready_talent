from flask import Flask, render_template, request, session, redirect,url_for,flash
# from flask_pymongo import PyMongo
from datetime import datetime, time
import string
import random
import json
import requests
import gunicorn
from user_agents import parse
from models import Creators, Visitors, Contact
from mongoengine import connect
from flask import send_from_directory
import os
import pytz




def getDateTime():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    datetime_ist = datetime_ist.strftime('%Y-%m-%d %H:%M:%S')
    return datetime_ist



uri = "mongodb+srv://ipfy:ipfy@cluster0.9je56.mongodb.net/ipfy"
connect(host=uri)
#uri = "mongodb://localhost:27017/ipfy"
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def home():
    # print(request.host_url)
    return render_template("index.html",error = "")


@app.route("/shorturl", methods=['POST'])
def shorturl():
    try:
        link = request.form.get('url')
        try:
            ip = request.access_route[-1]
            # ip = ip[0:-6]
                
        except Exception as e:
            print(e)
            ip = request.environ['HTTP_X_FORWARDED_FOR']
            # ip = ip[0:-6]
            
        user_agent = request.user_agent
        user_agent = str(user_agent)

        N = 6
        short_url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
        print(short_url)
        
        track = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=N))
        
        tracking_url = "track/"+track
        print(tracking_url)
        if 'http' not in link:
            link = 'http://' + link
            
        creator = Creators(
            ip = ip,
            user_agent = user_agent,
            original_url = link,
            short_url = short_url,
            tracking_url = tracking_url,
            time = getDateTime()

        )
        creator.save()

        return redirect(tracking_url)
    except Exception as e:
        print(e)
        return render_template('index.html',error = "The given url is not valid !!!")

@app.route('/track/<string:track>',methods=['GET','POST'])
def track(track):
    if request.method=='GET':
        print(track)
        # try:
        creator = Creators.objects.get(tracking_url = "track/"+track)
        if creator:
            creator.short_url = request.host_url + creator.short_url
            creator.tracking_url = request.host_url + creator.tracking_url
            
            visitors = Visitors.objects(tracking_url = "track/"+track)
            countVisitors = 0
            for visitor in visitors:
                countVisitors = countVisitors + 1
            
            return render_template('track.html',creator = creator, visitors = visitors,countVisitors=countVisitors)
        # except Exception as e:
        #     print(e)
        #     return redirect("/")

        
    else:
        print(track)
        try:
            creator = Creators.objects.get(tracking_url = "track/"+track)
            if creator:
                                
                visitors = Visitors.objects(tracking_url = "track/"+track)
                countVisitors = 0
                
                return json.dumps(visitors)
        except Exception as e:
            print(e)
            return redirect("/")

        
    
    
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/<string:short>")
def short(short):
    try:
        data = Creators.objects.get(short_url = short)
        if data:
            original_link = data.original_url
            # getting client info

            try:
                ip = request.access_route[-1]
                print("The IP is "+str(ip))
                # ip = ip[0:-6]
                
            except Exception as e:
                print(e)
                ip = request.environ['HTTP_X_FORWARDED_FOR']
                print("The IP issss "+str(ip))
                # ip = ip[0:-6]

            print(ip)
            
            header = request.user_agent
            header = str(header)
            user_agent = parse(header)
            browser = user_agent.browser.family +" "+user_agent.browser.version_string
            os = user_agent.os.family +" "+ user_agent.os.version_string
            device = user_agent.device.family 
            
            url = 'http://ip-api.com/json/'+ip
            r = requests.get(url).json()
            print(r)
            try:
                country = r['country']
                state = r['regionName']
                city = r['city']
                isp = r['isp']
                timezone = r['timezone']
            except:
                country = "Hidden"
                state = "Hidden"
                city = "Hidden"
                isp = "Hidden"
                timezone = "Hidden"
                            
            visitor = Visitors(
                ip = ip,
                user_agent = header,
                browser = browser,
                os = os,
                device = device,
                country = country,
                state = state,
                city = city,
                timezone = timezone,
                isp = isp,
                tracking_url = data.tracking_url,
                time = getDateTime()
            )
            visitor.save()
            

            return redirect(original_link)
    except Exception as e:
        print(e)    
        return redirect("/")
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='GET':
        return render_template('contact.html')
    if request.method=='POST':
        name =request.form.get('name')
        email =request.form.get('email')
        message =request.form.get('message')
        print(name)
        print(email)
        print(message)

        contact = Contact(
            name = name,
            email = email,
            message = message,
            time = getDateTime()
        )
        contact.save()
        response = "Thank for contacting. We will reach to you soon."
        flash("Thank for contacting. We will reach to you soon.","error")
        
        return render_template('contact.html',response = response)
        # return redirect(url_for('contact',response=True))

@app.route("/api")
def api():
    return render_template('api.html')    

@app.route("/fetch_test",methods=['POST'])
def fetch_test():
    print(request.json)
    return "hello"
    

# let a = fetch('http://127.0.0.1:5000/fetch_test', {
#       method: 'POST',
#       headers: {
#         "Content-Type": 'application/json'
#       }
#     });



if __name__ == '__main__':
    app.run(host ='0.0.0.0', debug = True)