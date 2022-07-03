# 개요
* DB 초기화 스크립트

# 스크립트
```sql

CREATE TABLE users (
    id serial PRIMARY KEY,
    name VARCHAR (50) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE projects (
	id serial PRIMARY KEY,
	user_id integer NOT NULL,
	name VARCHAR ( 50 ) UNIQUE NOT NULL,
    description VARCHAR ( 255 ),
	created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  project_id integer NOT NULL,
  name varchar(50) UNIQUE NOT NULL,
  github_url varchar(255) NOT NULL,
  github_branch varchar(255) NOT NULL,
  github_runfile varchar(255) NOT NULL,
  lang_type varchar(50) NOT NULL,
  lang_version varchar(50) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  CONSTRAINT fk_project_id FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE ON UPDATE CASCADE  
);


INSERT
    INTO users (name, created_at, updated_at)
    VALUES ('test-user', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
```