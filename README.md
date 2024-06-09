# Networking
REST API's to connect with any user

## Pre-Setup
1. create ```.env``` file in the root directory
2. add the below content in ```.env``` file
   ```bash
   POSTGRES_USERNAME="Enter your username(Ex: postgres)"
   POSTGRES_DATABASE="Enter a database name(Ex: postgres)"
   POSTGRES_PASSWORD="Enter a password(Ex:Networking@123)"
   POSTGRES_PORT="Enter port(Ex: 5432)"
   ```

## Running instructions

1. Run your application
    ```bash
    docker-compose build --no-cache && docker-compose up -d
    ```

2. To setup your super user:
   
   a. Enter into backend container
   ```bash
   docker exec -it networking-backend-server /bin/bash 
   ```
   b. Create a super user using the following command - it will ask for username, email, password and confirm password
   ```bash
   python manage.py createsuperuser
   ```

## Verdict

You can now access the backend server in [http://127.0.0.1:7000/](http://127.0.0.1:7000/signup/). 

It will initially ask you signup, you can diectly login using your admin account by going to [login](http://127.0.0.1:7000/login/) page OR follow the template provided to create a seperate account


## List of all API's

| API Description                                 | URL                                                                                      |
|-------------------------------------------------|------------------------------------------------------------------------------------------|
| Signup                                          | [http://127.0.0.1:7000/signup/](http://127.0.0.1:7000/signup/)                           |
| Login                                           | [http://127.0.0.1:7000/login/](http://127.0.0.1:7000/login/)                             |
| Logout                                          | [http://127.0.0.1:7000/logout/](http://127.0.0.1:7000/logout/)                           |
| Search for users                                | [http://127.0.0.1:7000/api/users/?query=<name/emailid>&page=<page number>](http://127.0.0.1:7000/api/users/?query=<name/emailid>) |
| Check your friend requests sent by other users | [http://127.0.0.1:7000/api/friend-requests/](http://127.0.0.1:7000/api/friend-requests/) |
| Create a friend request                        | [http://127.0.0.1:7000/api/friend-requests/](http://127.0.0.1:7000/api/friend-requests/) |
| Accept a friend request                        | [http://127.0.0.1:7000/api/friend-requests/request-id/accept/](http://127.0.0.1:7000/api/friend-requests/<request-id>/accept/) |
| Reject a friend request                        | [http://127.0.0.1:7000/api/friend-requests/request-id/reject/](http://127.0.0.1:7000/api/friend-requests/<request-id>/reject/) |
| Check your friend list                         | [http://127.0.0.1:7000/api/friends/](http://127.0.0.1:7000/api/friends/)                 |




