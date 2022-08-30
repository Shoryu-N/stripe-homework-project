# Stripe Homework Project

1. clone the repository and run pip3 to install dependencies:

```
git clone git@github.com:Shoryu-N/stripe-homework-project.git && cd stripe-homework-project
pip3 install -r requirements.txt
```

or

```
git clone https://github.com/Shoryu-N/stripe-homework-project.git && cd stripe-homework-project
pip3 install -r requirements.txt
```
If pip is not installed, update to Python 3.4 or later.


2. Add an .env file with your private and publishable keys in the following format.
```
STRIPE_SECRET_KEY=<your-secret-key>
STRIPE_PUBLISHABLE_KEY=<your-publishable-key> 
```


3. Run the application locally:

```
flask run
```

Navigate to [http://localhost:5000](http://localhost:5000) to view the index page.

4. Choose one of the three books.

5. Enter your email address and the test card information provided by Stripe.

You can use the cards in the [link](https://stripe.com/docs/testing).

6. If you use the test card for success, you will be redirected to the Success page, where you will see the amount of your order and the paymentIntent ID. If you use the test card for failure, you will not be redirected to the Success page, but will see a message informing you of the error.
