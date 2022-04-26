# Tinder bot for searching teammates
## Testing task to GoodGame
![Bot face](robot.png)

## Description
1. /start command fill full profile of the bot
2. /edit asks to edit exact field
3. /search runs searching algorithm
4. /disable and /enable clearly understand
## Hacks
- I use callback to store current context to per user and set timeout of class event to 600
- Maybe its not clear way so I would like to get feedback about my solution
- I use Message Loop thread so you dont need to attach webhook
## Deploying
First of all you need to fill .env according to .env.example and then just type

        sudo docker-compose up --build

or on windows
        
        python manage.py migrate
        python manage.py runserver