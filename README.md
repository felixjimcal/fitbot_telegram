# fitbot_telegram

Telegram bot for fitbot project, an automated fitness service.

The main idea was to create an automated fitness service that includes routines and a diet plan, which are adapted by asking the user questions such as their gender, age, experience, place of training, etc. <br />
To attract users I have indicated a '🥕 Demo 🏋' button where a simulation generates a meal plan and exercise routine, then the user can choose to 'Sign Up 🆕' in the application. <br />
Using Stripe payment's service
Telegram provides a lot of information about the user at all time, which allows us to have a closer touch with the user. <br />

For example the user_name in the app: <br />
![image](https://user-images.githubusercontent.com/8387061/156339945-065db469-1439-4dbb-975a-d682efb046ba.png)
![image](https://user-images.githubusercontent.com/8387061/156340463-9186093f-2a68-492a-947b-dd6eefa50721.png)

Using Stripe services, for card payments, I wanted to send a charge and proceed to register the user. You are probably thinking, without email or password? The telegram service itself allows you to adapt the sending data of an invoice, as well as indicate an email and also provides the unique id on the platform of each user.<br /><br />

In this way, the user's Telegram ID and email address could be stored in a database.<br />
![image](https://user-images.githubusercontent.com/8387061/156342623-0d337368-0d08-4b6c-8b6d-a72bde7ff49f.png)



## Tech Stack: <br />
Front:  Telegram Bots API ([Docs](https://core.telegram.org/bots/api))<br />
Backend: Python ([pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI))<br />
DataBase: SQLite ([Tutorial](https://likegeeks.com/es/tutorial-de-python-sqlite3/))<br /> 
Deploy: Heroku <br />
Payments: Telegram Bots Payments [Docs](https://core.telegram.org/bots/payments), Stripe API [Docs](https://stripe.com/docs/api/invoices/create?lang=python) <br />


## Some Examples:
Now I am going to show you a series of images in case you do not have Telegram or in case the service has been canceled.

### Demo Diet Plan 🥕:
![image](https://user-images.githubusercontent.com/8387061/156344923-dfd58e4b-ee44-4352-ac6e-5b8dbed5e89a.png)
![image](https://user-images.githubusercontent.com/8387061/156345177-335ea194-4aad-44b5-9e6e-fd1b9b4314b4.png)
<br />

### Demo Workout 🏋️
![image](https://user-images.githubusercontent.com/8387061/156347638-efe01d1e-331e-4f86-81e7-426ce4eaaa07.png)
<br />

### Sign Up 🆕 process:
The Stripe service allows you to load the list of products from the website and keep the prices updated at all time.
<br />
1. Type an email <br />
![image](https://user-images.githubusercontent.com/8387061/156346118-8ea8a5d2-b2f2-4439-aba6-2573c3e5f525.png)
<br />

2. Fill shipping address <br />
![image](https://user-images.githubusercontent.com/8387061/156348351-d96bd9fa-68e9-48e3-8fdb-a19b87bfbc39.png)
<br />

3. Last step with product name and description <br />
![image](https://user-images.githubusercontent.com/8387061/156348403-c053dee6-bda7-4c44-9948-87ab37095565.png)
<br />

4. Hurray message! <br />
![image](https://user-images.githubusercontent.com/8387061/156351041-62b8bb24-2de9-48ae-ba7f-a80ba3a38716.png)
<br />

5. Email with invoice <br />
![image](https://user-images.githubusercontent.com/8387061/156354518-af0aa126-8ddd-4cf5-ab9f-c1332de48819.png)
<br />
<br />

I know, there are a lot of images, I stop here, there's a menu for a logged user with the actual workout and Diet plan. On the first time the bot send a bunch of questions to be answered and generate those plans.
<br />
<br />

### Finally,
If you want to do a similar project I strongly recommend that you have a test bot. <br />
Finally, if you want to do a similar project, I strongly recommend that you have a test bot, all the data you see is test data and is deprecated.

### SETUP ...for future developemnts
GMAIL: fitbotweb@gmail.com
https://github.com/eternnoir/pyTelegramBotAPI
https://likegeeks.com/es/tutorial-de-python-sqlite3/
https://web.telegram.org/z/
https://core.telegram.org/bots/api#answershippingquery
https://core.telegram.org/bots/payments#step-by-step-process
https://stripe.com/docs/api/invoices/create?lang=python
https://dashboard.stripe.com/test/payments
https://towardsdatascience.com/creating-a-telegram-chatbot-quiz-with-python-711a43c0c424
FAKE CARD: 4242 4242 4242 4242
