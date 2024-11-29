Obtaining a token:
    send a POST request to : localhost:8000/api-token-auth/
    params: {"phone_number": "", "password": ""}

User tasks

1. create a new user using api (permission set to any)
    send POST request to : http://localhost:8000/users/
    params required: {"phone_number" : "", "name":"", "password": ""}

2. update the user using api (permission user only)
    send PUT request to : http://localhost:8000/users/<int:pk>/
    params required: {Authorization: Token {token}, params to change}

3. delete the user using api (permission admin only)
    send DELETE request to : http://localhost:8000/users/<int:pk>/

Test tasks

1. create a new Test using api ()

2. update the test using api ()

3. delete the test using api ()
 
Question tasks

1. create a new Question using api ()

2. update the Question using api ()

3. delete the Question using api ()

Answer tasks

1. create the Answer using api ()

2. update the Answer using api ()

3. delete the Answer using api ()



