    // detect mobile or pc
    // const isMobile = /Mobi|Android/i.test(navigator.userAgent);

    // if (isMobile) {
    //     document.body.classList.add('mobile');
    // } else {
    //     document.body.classList.add('desktop');
    // }

    // initialize variables
    let encryptionKey;
    if (sessionStorage.getItem('encryptionKey') !== null) {
        encryptionKey = sessionStorage.getItem('encryptionKey');
    }
    let password;
    let encryptedPassword;
    let decryptedPassword;

    // get modal, buttons, selects, and add functions to buttons
    const addBtn = document.getElementById('add');
    addBtn.addEventListener('click', add_account);

    const getBtn = document.getElementById('get');
    getBtn.onclick = get_account;

    const datalist = document.getElementById('accounts');
    const selection = document.getElementById('account');

    const modal = document.getElementById("myModal");
    const openBtn = document.getElementById("openModalBtn");
    const modalSubmitBtn = document.getElementById('modal-submit');

    const fieldRows = document.querySelectorAll('.field-row');
    fieldRows.forEach(row => {
        row.addEventListener('click', (e) => get_row(e))
    });
    
    // Open modal code
    document.addEventListener("DOMContentLoaded", () => {display_modal();});

    function display_modal() {
        if (!sessionStorage.getItem('encryptionKey')) {
            const modal = document.getElementById('myModal');
            modal.style.display = 'block';
            load_accounts();
        } else {
            modal.style.display = 'none';
            load_accounts();
        }
    }

    // Upload key and close modal when finished
    modalSubmitBtn.onclick = function() {
        encryptionKey = document.getElementById('encryption-key').value;
        if (!encryptionKey) {
            document.querySelector('.modal-content p').innerText = 'Must enter an encryption key!'
        } else {
            sessionStorage.setItem('encryptionKey', encryptionKey);
            modal.style.display = 'none';
        }
    }

    function load_accounts() {
        fetch('/load_accounts')
        .then(response => response.json())
        .then(data => {
            data.forEach(account => {
                const option = document.createElement('option');
                option.class = 'option-class'
                option.value = account;
                option.textContent = account;
                datalist.appendChild(option);
            });
        })
    }

    function get_row(e) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            const row = e.currentTarget;
            const field = row.querySelector('.field').innerText;
    
            if (field === '') {
                navigator.clipboard.writeText('');
            } else if (e.target.className === 'copied-status') {
                navigator.clipboard.writeText('');
                e.target.innerText = '';
            } else {
                navigator.clipboard.writeText(field);
                row.querySelector('.copied-status').innerText = 'Copied to clipboard!'
            }
        }
    }

    // Get account info function
    function get_account(e) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText('');
        }

        const statuses = document.querySelectorAll('.copied-status');
        statuses.forEach(status => {
            status.innerText = '';
        })

        if (selection.value === null);
        else {
            fetch(`/get_account?account=${selection.value}`)
            .then(response => response.json())
            .then(res => {
                if (!res.arr) {
                    document.getElementById('get-account-notice').innerText = res.notice;
                } else {
                    document.getElementById('get-account-notice').innerText = '';
                    data = res.info;
                    encryptedPassword = data[4];
                    // if the following line does not work, do not update anything but give errors. if it does, update fields
                    decryptedPassword = CryptoJS.AES.decrypt(encryptedPassword, encryptionKey).toString(CryptoJS.enc.Utf8);
    
                    if (decryptedPassword !== '') {
                        document.getElementById('username').innerText = data[2];
                        document.getElementById('email').innerText = data[3];
                        document.getElementById('password').innerText = decryptedPassword;
                    } else {
                        document.getElementById('username').innerText = 'Something went wrong. Please try again.';
                        document.getElementById('email').innerText = 'Something went wrong. Please try again.';
                        document.getElementById('password').innerText = 'Something went wrong. Please try again.';
                    }
                }
            });
        }

    }

    function copyToClipboardFallback(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy'); // old-school copy
        } catch (err) {
            console.warn('Fallback copy failed', err);
        }
        document.body.removeChild(textarea);
    }

    // Add new account function
    function add_account() {
        let userId;
        const accountInput = document.getElementById('account-input').value;
        const usernameInput = document.getElementById('username-input').value;
        const emailInput = document.getElementById('email-input').value;
        const passInput = document.getElementById('pass-input').value;
        const encryptedPass = CryptoJS.AES.encrypt(passInput, encryptionKey).toString();

        fetch('/add_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({userId: userId, account: accountInput, username: usernameInput, email: emailInput, password: encryptedPass})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('add-notice').innerText = 'Account added successfully.';
            } else {
                document.getElementById('add-notice').innerText = data.notice;
            }
        });
    }