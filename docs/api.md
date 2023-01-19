# API

## Authentication

- url: api/auth/register

    ```json
    // request
    {
        "username": "admin",
        "email": "admin@bot.com",
        "password": "Password@123"
    }
    // response
    {
        "user": {
            "id": 2,
            "username": "admin1",
            "email": "admin1@bot.com"
        },
        "token": "790e890d571753148bbc9c4447f106e74ecf4d1404f080245f3e259703d58b09"
    }
    ```

- url: api/auth/login

```json
// request
{
    "username": "admin",
    "password": "Password@123"
}
//response
{
    "expiry": "2020-06-29T02:56:44.924698Z",
    "token": "99a27b2ebe718a2f0db6224e55b622a59ccdae9cf66861c60979a25ffb4f133e"
}
```
