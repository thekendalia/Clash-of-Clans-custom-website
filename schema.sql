CREATE TABLE IF NOT EXISTS clash (
    id SERIAL,
    clashname VARCHAR(255) NOT NULL,
    optin BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    code int,
    PRIMARY KEY (id)
);