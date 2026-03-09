sessionStorage.removeItem('encryptionKey');

const registerBtn = document.getElementById('register');
registerBtn.addEventListener('click', register);

function register() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmedPassword = document.getElementById('confirmed-password').value;

    if (password !== confirmedPassword) {
        document.getElementById('notice').innerText = 'Passwords do not match.';
    } else {
        fetch('/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email, password: password})
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('notice').innerText = data.data;
        });
    }
}