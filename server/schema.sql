drop table if exists players;
create table players(
  id integer primary key autoincrement,
  name text not null,
  password text not null,
  score integer,
  options text
);
