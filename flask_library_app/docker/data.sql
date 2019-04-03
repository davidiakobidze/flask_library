create table authors
(
  author_id   SERIAL primary key,
  first_name  text,
  last_name   text,
  age         integer,
  nationality text
);

CREATE TABLE books
(
  book_id  SERIAL primary key,
  isbn     TEXT,
  title    TEXT,
  language TEXT,
  length   integer,
  price    integer,
  genre    text
);

CREATE TABLE authors_books
(
  author_id integer,
  book_id integer,
  foreign key (author_id) references authors (author_id),
  foreign key (book_id) references books (book_id)
);

CREATE TABLE roles
(
  role_id SERIAL primary key,
  name    text
);

CREATE TABLE users
(
  user_id    SERIAL primary key,
  first_name text,
  last_name  text,
  user_name  text,
  password   text,
  role_id    integer,
  foreign key (role_id) references roles (role_id)
);

create table orders
(
  order_id      SERIAL primary key,
  price         real,
  total_price   real,
  shipping_data text,
  order_date    text,
  user_id       integer,
  foreign key (user_id) references users (user_id)
);

create table orders_books
(
  order_id integer,
  book_id integer,
  foreign key (order_id) references orders (order_id),
  foreign key (book_id) references books (book_id)
)
