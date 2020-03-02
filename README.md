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

## Reference
* [Dockerでローカル開発環境用MySQLサーバを動かす](https://qiita.com/rkunihiro/items/ea5d9d9274e30d4880c2)
* [MySQL :: MySQL Connector/Python Developer Guide :: Connector/Python Coding Examples](https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html)