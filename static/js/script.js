'use strict';

// Accssing body element
const body = document.querySelector('body');

// 'Log In' form DOM elements
const logInBtn = document.getElementById('log-in-btn');
const logInForm = document.getElementById('log-in-form');
const logInEmail = document.getElementById('log-in-email');
const logInPassword = document.getElementById('log-in-password');
const logInSubmitBtn = document.getElementById('log-in-submit-btn');

// Close button for each of the forms
const closeBtn = document.querySelectorAll('.close-btn');

// Create new div for the overlay effect
const overlayContainer = document.createElement('div');

// Opens the 'Log In' form modal window
logInBtn.addEventListener('click', () => {
    logInForm.style.display = 'block';
    overlayContainer.classList.toggle('overlay');
    body.appendChild(overlayContainer);
});

// This close button is form the login form.
closeBtn[0].addEventListener('click', (event) => {
    event.preventDefault();
    logInForm.style.display = 'none';
    overlayContainer.classList.toggle('overlay');
});

// Close the form wen clicked on the overlay itself
overlayContainer.addEventListener('click', () => {
    logInForm.style.display = 'none';
    overlayContainer.classList.toggle('overlay');
});
