DROP TABLE IF EXISTS devices;

CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    mac_address TEXT NOT NULL,
    hostname TEXT NOT NULL,
    original_line TEXT NOT NULL
);
