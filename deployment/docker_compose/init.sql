CREATE DATABASE chatbot_core;

CREATE TABLE connectors (
    id INT,
    name VARCHAR(255),
    source VARCHAR(30),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    PRIMARY KEY (id)
);