# IntelliScan
INTELLISCAN is an AI-driven medical imaging solution to accurately diagnose and analyze conditions affecting the lungs, aiming at improving early detection , treatment planning and patient outcomes.

### Features
- [x] Login
- [ ] Logout ?!
- [x] User Register
- [x] User Fetch
- [x] User Update
- [x] User Delete
- [x] Inference Upload ?!

#### ?! Logout
Possibly implement a table to blacklist tokens when logout endpoint is called.

### How to run
- Create a virtualenv, then install the dependencies using:
    ```
    pip install -r requirements.txt
    ```
- Run the following commands in your shell:
    ```
    cd backend

    flask run
    ```
- Use the curls in the curls folder to test, copy a curl paste in your terminal run. (Only works on Unix type operating systems, if you are running windows you can run it from git bash if you have it installed or you could use postman like a regular person)

Don`t forget to set environment variables or use the .env since Python DotEnv is a dependency
