# -------------- About the program -------------- #

This is a full-stack password manager web-app designed to manage passwords across
multiple devices without relying on services like Google or Microsoft. I wanted
to have full knowledge and control over security and data privacy, as well
as solve the problem of storing passwords on different devices that cannot
easily be accessed or updated from another.

What I did/learned:
 - Security best practices: Implemented secure password storage through hashing, encryption, session management, 
   and CryptoJS for client-side encryption. 
 - Back-end development: Constructed and queried databases using SQLite and PostgreSQL; I built a robust
   Flask server with RESTful API endpoints. 
 - Front-end development: Built a minimal, modern GUI using HTML, CSS, and JS; integrated front-end with
   back-end APIs via GET and POST requests.
 - Full-stack integration: End-to-end application architecture, including database design, secure server 
   logic, and client-side encryption workflows.

# --------------                   -------------- #



# -------------- Instructions to run program -------------- #

This web-app is written to be executed on localhost with minimal installation.

  1. Clone the GitHub repository: git clone https://github.com/dominiccc13/local_pwm.git
  2. CD into root directory: cd "C:\Path\To\Your\Directory\"
  2. Download and install Python 3.13.7 and VS Code if necessary: https://www.python.org/downloads/release/python-3137/ https://code.visualstudio.com/download
  3. Create a virtual environment: python -m venv .venv
  4. Activate it: .\.venv\Scripts\Activate
  5. Install packages: pip install -r requirements.txt
  6. Create and populate database: py .\init_db\init_db.py
  7. Run Flask server: py server_local.py
  8. Ctrl+click on local ip address printed to terminal.
  9. Refer to testing account information below to test the web-app.

# --------------                             -------------- #



# -------------- Information for testing -------------- #
Sample email, password, and encryption key for testing:

email: quick_fox@email.com
pass: wickersnake!
encryption key: keytest1

email: techy_turtle@email.com
pass: shadowriver#
encryption key: user2key
# --------------                         -------------- #