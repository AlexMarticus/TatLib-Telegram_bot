DROP TABLE IF EXISTS users_to_words;
DROP TABLE IF EXISTS users_to_books;
DROP TABLE IF EXISTS possibles_answers;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;


CREATE TABLE users
(
    id serial PRIMARY KEY,
    login varchar NOT NULL UNIQUE,
    email varchar NOT NULL UNIQUE,
	tg_username varchar NOT NULL UNIQUE,
	tg_id int UNIQUE,
    hashed_password varchar NOT NULL,
	creation_date date DEFAULT '01.02.1998',
	is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE books
(
    id serial PRIMARY KEY,
    title varchar NOT NULL,
	author varchar NOT NULL,
    creator_id int,
    difficult_level varchar(6) NOT NULL
);

CREATE TABLE words
(
    id serial PRIMARY KEY,
	word_tat varchar NOT NULL UNIQUE,
    word_ru varchar NOT NULL UNIQUE
);

CREATE TABLE questions
(
    id serial PRIMARY KEY,
	question varchar NOT NULL UNIQUE
);

CREATE TABLE possibles_answers
(
    id serial PRIMARY KEY,
	question_id int NOT NULL REFERENCES questions(id),
	answer varchar NOT NULL,
	is_correct_answer boolean DEFAULT FALSE
);

CREATE TABLE users_to_books
(
    user_id int NOT NULL REFERENCES users(id),
    book_id int NOT NULL REFERENCES books(id),

    PRIMARY KEY(user_id, book_id)
);

CREATE TABLE users_to_words
(
    user_id int NOT NULL REFERENCES users(id),
    word_id int NOT NULL REFERENCES words(id),
    word_level int NOT NULL DEFAULT 0,
    next_date_training date DEFAULT '21-10-2022',

    PRIMARY KEY(user_id, word_id)
);
