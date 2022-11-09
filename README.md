# backend-blog-app

Blog application, with simple HTML interface.

In implementation was used MySQL database with one-to-many relationship between People schema and Notes schema. Each person can have many notes, related with primary key to person.

Also was used ORM (SQLAlchemy) to create model schema of tables.

With connexion package and yaml file, was made respresentation of CRUD operations in swagger. 
