1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py createsuperuser(create 3 users)
5. python manage.py collectstatic
6. python manage.py generate_data
7. python manage.py runserver

After running first 7 commands which set up initial data use Postman or analog software to check up further endpoints:
- http://127.0.0.1:8000/admin/ - admin page with data customization
- http://127.0.0.1:8000/token/ - simple authorization to retrieve token for further use
* example of body - {
    "username": "",
    "password": ""
}
- http://127.0.0.1:8000/chats/threads/ - [GET] retrieves data about all threads and messages of all users(UI point of view it's incorrect but kept just for the ease of use the same can be with the other endpoints which are not meantioned)
- http://127.0.0.1:8000/chats/threads/ - [POST] creates Thread between 2 users and sends messages
* example of body - {
            "participants": [
                {
                    "id": 1,
                    "username": "qwerty"
                },
                {
                    "id": 2,
                    "username": "asdf"
                }
            ],
            "messages": [{
                    "sender": 1,
                    "text": "Message 1 from user 1 to user",
                    "is_read": false
                },
                {
                    "sender": 1,
                    "text": "Message 2 from user 2 to user",
                    "is_read": false
                }]
        }
- http://127.0.0.1:8000/chats/threads/(id)/ - [GET] retrieves messages of specific Thread(automatically changes status of all unread messages to read)
* example of response - {
    "id": "2d480477-7d1b-4555-b033-21ea8a881ac9",
    "participants": [
        {
            "id": 1,
            "username": "qwerty"
        },
        {
            "id": 3,
            "username": "zxcv"
        }
    ],
    "messages": [
        {
            "id": "ea82f00e-16e0-4f6a-bbfd-157a514b224c",
            "sender": 1,
            "text": "Message 1 from user 1 to user",
            "is_read": true
        },
        {
            "id": "baf721ec-5260-4447-b9e5-91875f42b889",
            "sender": 3,
            "text": "Message 2 from user 3 to user",
            "is_read": false
        }
    ]
}
- http://127.0.0.1:8000/chats/threads/unread-count/ - [GET] retrieves number of unread messages
* example of response - [
    {
        "user_id": 1,
        "number_of_messages": 3
    },
    {
        "user_id": 2,
        "number_of_messages": 2
    }
]
- http://127.0.0.1:8000/chats/messages/ - [POST] creates message in the thread
* example of body - {
            "thread": "30fc6e76-036b-4121-ae9a-bf15fc960ff2",
            "sender": 1,
            "text": "Message 1 from user 1 to user",
            "is_read": false
        }
- http://127.0.0.1:8000/chats/messages/(id)/ - [PATCH] updates message in the thread
* example of body - {
    "thread": "30fc6e76-036b-4121-ae9a-bf15fc960ff2",
    "sender": 1,
    "text": "update test",
    "is_read": false
}
- http://127.0.0.1:8000/chats/messages/(id)/ - [DELETE] deleted message in the thread

P.S. I may miss out some other features, but I believe I've covered each essential stuff which was required.
P.S.S. I know I also needed to add swagger with detailed documentation but due to lack of time