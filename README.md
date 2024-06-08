# Networking
REST API's to connect with any userwad

## Pre-Setup
1. create ```.env``` file in the root directory
2. add the below content in ```.env``` file
   ```bash
   POSTGRES_USERNAME="Enter your username(Ex: postgres)"
   POSTGRES_DATABASE="Enter a database name(Ex: postgres)"
   POSTGRES_PASSWORD="Enter your password(Ex:Networking@123)"
   POSTGRES_PORT="Enter port(Ex: 5432)"
   ```

## Running instructions

1. Run your application
    ```bash
    docker-compose up -d --build
    ```

2. To setup your super user:
   a. Enter into backend container
   ```bash
   docker exec -it ding-backend-server /bin/bash 
   ```
   b. Create a super user using the following command - it will ask for username, email, password, confirm password
   ```bash
   python manage.py createsuperuser
   ```

## Verdict

You can access the backend server in [http://127.0.0.1:7000/](http://127.0.0.1:7000/signup/). 

It will initially ask you signup, you can either diectly login using your admin account by going to [login](http://127.0.0.1:8000/login/) page or follow the template provided to create a seperate account


## List of all API's

1. signup - [http://127.0.0.1:7000/signup/](http://127.0.0.1:7000/signup/)
2. login - [http://127.0.0.1:7000/login/](http://127.0.0.1:8000/login/)
3. logout - [http://127.0.0.1:7000/logout/](http://127.0.0.1:8000/logout/)
4. Search for users = [http://127.0.0.1:8000/api/users/?query=<name/emailid>](http://127.0.0.1:8000/api/users/?query=<name/emailid>)
5. Check your friend requests sent by other users - [http://127.0.0.1:8000/api/friend-requests/](http://127.0.0.1:8000/api/friend-requests/)
6. Create a friend request - [http://127.0.0.1:8000/api/friend-requests/](http://127.0.0.1:8000/api/friend-requests/) - need to update all of them with postman curl
7. Accept a friend request - [http://127.0.0.1:8000/api/friend-requests/<name>/accept/](http://127.0.0.1:8000/api/friend-requests/<name>/accept/)
8. Reject a friend request - [http://127.0.0.1:8000/api/friend-requests/<name>/reject](http://127.0.0.1:8000/api/friend-requests/<name>/reject/)
9. Check your friend list - [http://127.0.0.1:8000/api/friends/](http://127.0.0.1:8000/api/friends/)



