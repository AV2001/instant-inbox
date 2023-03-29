'use strict';

const btnOutlookLogin = document.getElementById('btn-outlook-login');

if (btnOutlookLogin) {
    btnOutlookLogin.addEventListener(
        'click',
        () => (window.location.href = '/login')
    );
}
