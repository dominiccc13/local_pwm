sessionStorage.removeItem('encryptionKey');

const loginBtn = document.getElementById('login');
loginBtn.addEventListener('click', login);

function login() {
    const email = document.getElementById('email').value;
    const pass = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email: email, pass: pass})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;     
        } else {
            document.getElementById('notice').innerText = data.notice;
        }
    });
}