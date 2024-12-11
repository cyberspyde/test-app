Obtaining a token:
    send a POST request to : localhost:8000/sign-up/
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

4. Get the user info (permission admin only)
    send GET request to : http://localhost:8000/users/

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

1. create a new Question using api (permission set to Admin only)
    send POST request to : http://localhost:8000/questions/
    required params : Auth token, {"question_text": "", "test" : {test id} }

2. read the Question using api (permission set to Admin only for all questions, allowAny for specific questions)
    send GET request to : http://localhost:8000/questions/
    required : Auth token

3. update the Question using api (permission set to Admin only)
    send PUT request to : http://localhost:8000/questions/<int:pk>
    required : Auth token, {params to change, "test" : {test_id} }

4. delete the Question using api (permission set to Admin only)
    send DELETE request to : http://localhost:8000/questions/<int:pk>
    required : Auth token

Answer tasks

1. create the Answer using api (any Authenticated users)
    send POST request to : http://localhost:8000/answers/
    required : Auth token, {"answer_text" : "", "test" : {test_id}, "question" : {question_id} }

2. read the Answer using api (permission set to Admin only)
    send GET request to : http://localhost:8000/answers/
    required : Auth token, id if for specific answers

3. update the Answer using api (permission set to Authenticated user only)
    send PUT request to : http://localhost:8000/answers/<int:pk>
    required : Auth token, 

4. delete the Answer using api (permission set to Admin only)
    send DELETE request to : http://localhost:8000/answers/<int:pk>
    required : Auth token, answer id


Live search by keywords
Terabox connection
Audio file testing
Leaderboard statistics
password change, user profile change
top authors
Search for:
    Test, User, Collection



