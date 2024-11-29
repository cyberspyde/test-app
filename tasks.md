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

1. create a new Test using api (permission set to Admin only)
    send POST request to : http://localhost:8000/tests/
    params required: {"test_title": "test_title", Authorization: Token {token} }

2. read the Test using api (permission set to Authenticated users)
    send GET request to : http://localhost:8000/tests/ or with <int:pk>
    required : Auth token

3. update the test using api (permission set to Admin only)
    send PUT request to : http://localhost:8000/tests/<int:pk>
    required params : Auth token and {params to update}

4. delete the test using api (permission set to Admin only)
    send DELETE request to : http://localhost:8000/tests/<int:pk>
    required : Auth token

Question tasks

1. create a new Question using api ()

2. read the Question using api ()

3. update the Question using api ()

4. delete the Question using api ()

Answer tasks

1. create the Answer using api ()

2. read the Question using api ()

3. update the Answer using api ()

4. delete the Answer using api ()



