# Discogs Takehome Assignment: Currency

Thanks for applying at Discogs!

We want to assess your technical ability, but we also think coding under pressure in an interview is a terrible way to do that.

So as a compromise, here's a takehome exercise that's a simplified version of work you'd be doing at Discogs if you were hired.

Our goal is for this to take a few hours (maybe four hours tops, if you're not very familiar with Python).
If it takes longer than that, we've failed, and you should let us know!

If we've made an error so grievous that you don't think you can finish the assignment, or you have any other questions after reviewing this document, feel free to email your contact at Discogs and let us know.

Please avoid sharing this excerise publicly. We want everyone else to have as much fun as you. :)


---
## Description of the Problem

This project is an API for managing the messages in an inbox. The API allows clients to send messages, mark them as read, put them in the trash, or indicate that they are spam. This API has no security and has lots of opportunities for improvement. In order to make things easier, we have also included endpoints for creating users. Since this is a "real" API, we can't change the contract/interface, we can only change the internal logic.

**Task 1:** This application tracks a spam report count for each message sender. That variable is stored in redis and is incremented each time a message recipient reports a new message from that sender as spam. For example, if user_1 receives three messages from user_2 and reports them all as spam, we’ll add 3 to user_2’s spam count.

Instead, we want a single recipient to only be able to increment the spam count for a single sender once, regardless of how many messages the same user reports as spam. In the same example used above, if user_1 receives three messages from user_2 and reports them all as spam, we’ll only add 1 to user_2’s spam count.

This then changes our spam counter to record how many **users** have reported this sender as a spammer, instead of how many **messages**. Please add tests to prove the validity of your work.

**Task 2:** The `update_messages` method in `app/crud.py` is not beautiful code and is doing too many things. Please refactor it and improve the testing around it.

**Task 3:** Bonus! Add something to make this API better. Show off your skills!


---
## Setup

In this repository we've included everything you need for a FastAPI project running in Docker with Docker Compose. There is a SQLite database for storage and a Redis server for caching.

Docker Desktop is required and can be downloaded and installed from: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

Assuming you have a working Docker installation locally, you should be able to just run:

`docker-compose up`

It should be accessible on port 8000 of your docker machine's IP address. Probably [http://localhost:8000/](http://localhost:8000/)

To (re)start the containers
`docker compose up -d`

To run the tests
`docker compose run --rm web pytest .`

FastAPI provides documentation here: [http://localhost:8000/docs](http://localhost:8000/docs)


---
## Finished?

Congrats!

To get the code back to us, please zip it up and email it to your contact at Discogs.

Thank you!

Discogs Engineering