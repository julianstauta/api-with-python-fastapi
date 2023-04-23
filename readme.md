=====================================
Discogs Takehome Assignment: Currency
=====================================

Thanks for applying at Discogs!

We want to assess your technical ability, but we also think coding under pressure in an interview is a terrible way to do that.

So as a compromise, here's a takehome exercise that's a simplified version of work you'd be doing at Discogs if you were hired.

Our goal is for this to take a few hours (maybe four hours tops, if you're not very familiar with Python).
If it takes longer than that, we've failed, and you should let us know!

If we've made an error so grievous that you don't think you can finish the assignment, or you have any other questions after reviewing this document, feel free to email your contact at Discogs and let us know.



=====================================
Description of the Problem
=====================================

This project is an API for managing the messages in an inbox. The API allows clients to send messages, mark them as read, put them in the trash, or indicate that they are spam. This API has no security and has lots of opportunities for improvement. In order to make things easier, we have also included endpoints for creating users. Since this is a "real" API, we can't change the contract/interface, we can only change the internal logic.

**Task 1:** When a user reports a message as spam, the message sender has a spam count incremented in redis, so we can easily see how many spam messages have been reported for that sender. We would like to slightly modify this logic and only allow a given recipient (the user who recieved the message and is reporting it as a spam message) to be able to report a sender only once. So if user_2 marks five messages from user_1 as spam, the redis spam count would only be incremented once, all of those messages would still move to the recipient's spam folder. This then changes our spam counter to record how many users have reported this sender as a spammer, instead of how many messages. Please add tests to prove the validity of your work.

**Task 2:** The app/crud/update_messages method is not beautiful code and is doing too many things. Please refactor it and improve the testing around it.

**Task 3:** Bonus! Add something to make this API better. Show off your skills!



=====================================
Setup
=====================================

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



==========
Finished?
==========
Congrats!

To get the code back to us, please zip it up and email it to your contact at Discogs.

Thank you!

Discogs Engineering