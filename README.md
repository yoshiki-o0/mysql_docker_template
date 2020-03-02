# Manipulate MySQL on Docker

## Get Started
Git clone this repository.

Activate Docker application.

Activate terminal and move to the local repository of this package.

- Start
  Run
  ```
  $ docker-compose up -d
  ```
- phpMyAdmin  
  Access `http://localhost:8080` from web browser.

- Stop
  ```
  docker-compose stop
  ```

- Run these commands when applied changes to conf files or SQL.
  ```
  docker-compose down
  docker-compose up -d
  ```

## Access database from other applications.

 |||
 |:---|:---|
 |Host|localhost|
 |Port|3306|
 |DB|sample|
 |User|test|
 |Pass|passwd|
