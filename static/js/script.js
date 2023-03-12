'use strict';

// Accssing body element
const body = document.querySelector('body');

// 'Log In' form DOM elements
const logInBtn = document.getElementById('log-in-btn');
const logInForm = document.getElementById('log-in-form');
const logInEmail = document.getElementById('log-in-email');
const logInPassword = document.getElementById('log-in-password');
const logInSubmitBtn = document.getElementById('log-in-submit-btn');

// 'Log In' form DOM elements
const createAccountBtn = document.getElementById('create-account-btn');
const createAccountForm = document.getElementById('create-account-form');
const firstName = document.getElementById('first-name');
const lastName = document.getElementById('last-name');
const createAccountEmail = document.getElementById('create-account-email');
const createAccountPassword = document.getElementById(
    'create-account-password'
);
const createAccountConfirmPassword = document.getElementById(
    'create-account-confirm-password'
);
const createAccountSubmitBtn = document.getElementById(
    'create-account-submit-btn'
);

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

// Opens the 'Create Account' form modal window
createAccountBtn.addEventListener('click', () => {
    createAccountForm.style.display = 'block';
    overlayContainer.classList.toggle('overlay');
    body.appendChild(overlayContainer);
});

// This close button is form the login form
closeBtn[0].addEventListener('click', (event) => {
    event.preventDefault();
    logInForm.style.display = 'none';
    overlayContainer.classList.toggle('overlay');
});

// This close button is for the create account form
closeBtn[1].addEventListener('click', (event) => {
    event.preventDefault();
    createAccountForm.style.display = 'none';
    overlayContainer.classList.toggle('overlay');
});

// Close the form when clicked on the overlay itself
overlayContainer.addEventListener('click', () => {
    logInForm.style.display = 'none';
    createAccountForm.style.display = 'none';
    overlayContainer.classList.toggle('overlay');
});

createAccountForm.addEventListener('submit', (event) => {
    event.preventDefault();

    // Create a user object
    const userObject = {
        firstName: firstName.value,
        lastName: lastName.value,
        email: createAccountEmail.value,
        password: createAccountPassword.value,
        confirmPassword: createAccountConfirmPassword.value,
    };

    // Use fetch to send a post request to the Flask server
    fetch('/create-account/', {
        method: 'POST',
        // Convert user object to JSON string
        body: JSON.stringify(userObject),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        // Handle response from the server
        .then((response) => response.json())
        // Catch errors
        .then((data) => console.log(data))
        .catch((error) => {
            console.log(error);
        });
});
