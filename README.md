# SMS_Survey_App

## SMS Market Survey Dashboard descriptions

1. Marketing team can input customer information (phone number, product type and customer name), edit messages, and send messages to customers;
2. Dashboard can reply to customers based on sentiment of customers;
3. Dashboard can judge if customers have sent feedback. (If yes, reply "Thank you for your feedback!");
4. Every message will be stored in database and be marked message type for searching(first message, first reply, feedback).
5. Dashboard is a responsive web app that can adjust to the size of window.

## Database

I used Mongo DB as the database.

## Implementation

1. Front-End
- I used HTML5, CSS3 and Javascript language, Bootstrap as framework to develop user interfaces.

2. Back-End
- I used Python Flask as backend framework. Twilio API and Microsoft Text Sentiment Analysis API are integrated to send custom SMS survey messages to customers and to send an auto-reply based on the sentiment of their feedback, which improved survey efficiency.

## Configuration descriptions

1. I used ngrok for local test which can generate a random url;
2. Change the webhook url of twilio account to the random url;
3. I connected the app with MongoDB on localhost.

## Running instructions

1. Start mongoDB sevice;
2. Run "python dashboard.py" under the folder of the app;
3. Start ngrok under the folder;
4. Change webhook url of twilio.
