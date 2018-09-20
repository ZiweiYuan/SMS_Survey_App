from flask import Flask, send_from_directory, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from config import MongoDB
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import config, urllib, json, requests

app = Flask(__name__)
mongo = PyMongo(app)
app.config.from_object(config)
# text analysis config
subscription_key="3639203c28b0470488cd82f99da1bcef"
assert subscription_key
text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_api_url = text_analytics_base_url + "sentiment"
# twilio config
account_sid = "AC48eca84c9efb66a84d676482d47f736a"
auth_token = "7343b6884f3700655843022ecf70265b"
client = Client(account_sid, auth_token)

# judge if customers have sent feedback, their phone number is the key
ifFeedback = {}

@app.route("/")
def index():
    return render_template('dashboard.html')

# send first messages to customers
@app.route('/send', methods=['POST'])
def sendSMS():
    global poResponse, neResponse, productType, cusName
    firstMs = request.form['firstMess']
    productType = request.form['productType']
    cusName = request.form['cusName']
    firstMs = firstMs.replace("<firstName>", cusName).replace("<productType>", productType)
    poResponse = request.form['poResponse'].replace("<productType>", productType)
    neResponse = request.form['neResponse'].replace("<productType>", productType)
    phoneNum = request.form['phoneNum']
    message = client.messages.create(
        to=phoneNum,
        from_="+16094548571",
        body=firstMs
    )
    ifFeedback[phoneNum] = False
    # store first messages metedata in MongoDB
    mongo.db.messages.insert({'phoneNum': phoneNum, 'productType':productType, \
    'cusName':cusName, 'sendMs':firstMs, 'type':'firstMs'})
    return redirect(url_for('index'))
    # return render_template('dashboard.html')

# response when customers reply
@app.route('/reply', methods=['POST'])
def reply():
    response = MessagingResponse()
    MsSid = request.form['MessageSid']
    cusMsg = client.messages(MsSid) \
                   .fetch().body
    phoneNum = client.messages(MsSid) \
                     .fetch().from_
    phoneNum = phoneNum.replace("u", "", 1)
    # judge if customers have sent feedback,if not, reply a message based on sentiment
    # if yes, reply "Thank you!"
    if not ifFeedback[phoneNum]:
        documents = {'documents' : [{'id': '1', 'language': 'en', 'text': cusMsg}]}
        headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
        respon  = requests.post(sentiment_api_url, headers=headers, json=documents)
        results = respon.json()
        sentiment = results['documents'][0]['score']
        # decide positive or negative
        if sentiment >= 0.5:
            response.message(poResponse)
            # store customers reply and our second messages (positive) metedata in MongoDB
            mongo.db.messages.insert({'phoneNum': phoneNum, 'productType':productType, \
            'cusName':cusName, 'replyMs': cusMsg, 'send':poResponse, 'type':'replyPo'})
        else:
            response.message(neResponse)
            # store customers reply and our second messages (negative) metedata in MongoDB
            mongo.db.messages.insert({'phoneNum': phoneNum, 'productType':productType, \
            'cusName':cusName, 'replyMs': cusMsg, 'send':neResponse, 'type':'replyNe'})
    else:
        response.message("Thank you for your feedback!")
        mongo.db.messages.insert({'phoneNum': phoneNum, 'productType':productType, \
        'cusName':cusName, 'replyMs': cusMsg, 'type':'feedback'})
    ifFeedback[phoneNum] = True
    return str(response)

if __name__ == "__main__":
    app.run()
