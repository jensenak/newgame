## The Pip Game Server

This server provides RESTful JSON endpoints for the "players" database.

Contract is as follows:

### "/" GET

Returns a list of up to 10 player names and scores, ordered by score (descending). For example:

    {"result":[{"name":"Bob", "score":11}, {"name":"9q8afheapfh", "score":3}, {"name":"lame", "score":-357}]}

Error modes:

- 500 for any problem encountered while attempting to return the data.

### "/login" POST

Get an access token.

Accepts: {"name":\<string\>, "password":\<string\>}

Returns: {"result":{"token":\<token\>}}

Error modes:
- 400 {"error":\<description\>} for bad requests
- 401 {"error":"unauthorized"} for requests not including a token
- 500 for internal server errors

### "/player" POST

Add a new player.

Accepts: {"name":\<string\>, "password":\<string\>, "score":\<number\>, "options":\<object\>}

- Name is any string
- Password is any string (this isn't actually a secure service, don't do anything stupid).
- Score [OPTIONAL] expects an integer. Any fractional portion will be ignored. Defaults to 0.
- Options [OPTIONAL] is an object, and is opaque to the server. It is simply intended to hold additional data for the front end.

Returns: {"result":{"message":"success"}}

Error modes:

- 400 {"error":\<description\>} for bad requests
- 500 for internal server errors

### "/player" PUT

Update a player's settings [Login Required].

Accepts: {"token":\<token\>, "password":\<string\>, "options":\<object\>}

- Token is the token issued with the last request. Absence of a token will be considered an unauthorized request.
- Password [OPTIONAL] is a string. If included, user's password will be updated.
- Options [OPTIONAL] is an object. If included, user's options will be replaced with this object.

Returns: {"result":{"updated":("password"|"options"|"password+options"), "token":\<new token\>}}

Error modes:

- 400 {"error":\<description\>} for bad requests
- 401 {"error":"unauthorized"} for requests not including a token
- 404 {"error":"player not found"} for wrong player name
- 500 for internal server errors

### "/player" DELETE

Delete a player [Login Required].

Accepts: {"token":\<token\>}

- Token is the token issued with the last request. Absence of a token will be considered an unauthorized request.

Returns: {"result":{"message":"player \<player\> deleted", "token":\<new token\>}}

Error modes:

- 401 {"error":"unauthorized"} for requests not including a token
- 404 {"error":"player not found"} for wrong player name
- 500 for internal server errors

### "/score" POST

Set a player's score [Login Required].

Accepts: {"token":\<token\>, "score":\<score\>}

- Token is the token issued with the last request. Absence of a token will be considered an unauthorized request.
- Score is the new number to which the score should be set.

Returns: {"result":{"player":\<name\>, "score":\<score\>, "token":\<new token\>}}

- 400 {"error":\<description\>} for bad requests
- 401 {"error":"unauthorized"} for requests not including a token
- 404 {"error":"player not found"} for wrong player name
- 500 for internal server errors

### "/score" PUT

Increment a player's score [Login Required].

Accepts: {"token":\<token\>}

- Token is the token issued with the last request. Absence of a token will be considered an unauthorized request.

Returns: {"result":{"player":\<name\>, "score":\<score\>, "token":\<new token\>}}

- 401 {"error":"unauthorized"} for requests not including a token
- 404 {"error":"player not found"} for wrong player name
- 500 for internal server errors

### "/score" DELETE

Decrement a player's score [Login Required].

Accepts: {"token":\<token\>}

- Token is the token issued with the last request. Absence of a token will be considered an unauthorized request.

Returns: {"result":{"player":\<name\>, "score":\<score\>, "token":\<new token\>}}

- 401 {"error":"unauthorized"} for requests not including a token
- 404 {"error":"player not found"} for wrong player name
- 500 for internal server errors
