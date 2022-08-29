/**
 * Clientside helper functions
 */

const STRIPE_PUB_KEY =
  'pk_test_51Iv0s0Aa6ZBB07qbkXSaVs1sgvn0dTionVci7lmot1O9Ml5xO86V9O21TuO6lpCMLbjbDpjdOSMi01VpLag5eCay00VcpbIwCS';

// To handle Stripe element form on checkout.html
async function handlePaymentForm() {
  const params = new URLSearchParams(window.location.search);
  const item = Number(params.get('item'));

  const clientSecret = await createStripePaymentIntent(item);

  const stripe = Stripe(STRIPE_PUB_KEY);

  const elements = renderStripeElement(stripe, clientSecret);

  document
    .getElementById('submit-payment')
    .addEventListener('click', async (e) => {
      e.preventDefault();
      const error = await confirmStripePayment(stripe, elements, item);
      if (error.type === 'card_error' || error.type === 'validation_error') {
        console.log(error.message);
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerText = `A Payment error has occurred. Please check your card.`;
      } else {
        console.log(error.message);
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerText = `An unexpected payment error has occurred. Please contact us: sample@example.com.`;
      }
    });
}

async function confirmStripePayment(stripe, elements, item) {
  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: `${window.location.protocol}//${window.location.host}/success?item=${item}`,
    },
  })

  return error
}

async function createStripePaymentIntent(item) {
  const res = await fetch('/create-payment-intent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ item: item }),
  });
  const data = await res.json();
  const { clientSecret, error } = data;
  if (error) {
    alert(error)
  } else {
    return clientSecret;
  }
}

function renderStripeElement(stripe, clientSecret) {
  elements = stripe.elements({ appearance: { theme: 'stripe' }, clientSecret });

  const paymtenElement = elements.create('payment');
  paymtenElement.mount('#payment-element');

  return elements;
}

// To handle payment success on success.html
async function handlePaymentSuccess() {
  const params = new URLSearchParams(window.location.search);
  const itemId = params.get('item');
  const item = await getItem(itemId);

  const paymentIntentClientSecret = params.get('payment_intent_client_secret');
  const intent = await getPaymentIntent(paymentIntentClientSecret);

  updateUI(item, intent);
}

function updateUI(item, intent) {
  const purchaseImg = document.getElementById('purchase-img');
  purchaseImg.src = `/images/${item.item.img}`;

  const amount = document.getElementById('amount');
  const amountToDollar = (intent.paymentIntent.amount / 100).toFixed(2);
  amount.innerText = `Your order detail: ${item.item.title} for $${amountToDollar}`;
  const payment_intent_id = document.getElementById('payment_intent_id');
  payment_intent_id.innerText = `Your payment id: ${intent.paymentIntent.id}`;
}

async function getPaymentIntent(paymentIntentClientSecret) {
  const stripe = Stripe(STRIPE_PUB_KEY);
  const intent = await stripe.retrievePaymentIntent(paymentIntentClientSecret);

  return intent;
}

async function getItem(itemId) {
  const res = await fetch(`/items/${itemId}`);
  return await res.json();
}

$(document).ready(function () {
  var amounts = document.getElementsByClassName('amount');

  for (var i = 0; i < amounts.length; i++) {
    amount = amounts[i].getAttribute('data-amount') / 100;
    amounts[i].innerHTML = amount.toFixed(2);
  }

  const on_form_page = document.getElementById('stripe-payment-form');
  if (on_form_page) {
    handlePaymentForm();
  }

  const on_success_page = document.getElementById('payment-success');
  if (on_success_page) {
    handlePaymentSuccess();
  }
});
