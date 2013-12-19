drop table if exists spots;
create table spots (
    id integer primary key autoincrement,
    name text not null,
    latitude integer not null,
    longitude integer not null,
    photo text not null
);
drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    admin integer not null
);
