CREATE TABLE Category (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE Model (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category_id INTEGER,
    rmse REAL,
    loss REAL,
    parameters TEXT,
    FOREIGN KEY (category_id) REFERENCES Category(id)
);

CREATE TABLE Attribute (
    id INTEGER PRIMARY KEY,
    name TEXT,
    value TEXT,
    model_id INTEGER,
    FOREIGN KEY (model_id) REFERENCES Model(id)
);

CREATE TABLE Image (
    id INTEGER PRIMARY KEY,
    path TEXT,
    model_id INTEGER,
    FOREIGN KEY (model_id) REFERENCES Model(id)
);
