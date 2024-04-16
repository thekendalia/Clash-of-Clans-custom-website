CREATE TABLE IF NOT EXISTS clash (
    id SERIAL,
    clashname VARCHAR(255) NOT NULL,
    optin BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

