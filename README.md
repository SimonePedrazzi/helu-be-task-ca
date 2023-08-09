# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

1. Why can we not easily split this project into two microservices?
2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?
3. What would be your plan to refactor the project to stick to the clean architecture?
4. How can you make dependencies between modules more explicit?

### Answers

1. The biggest problem I noticed is that the user subpackage, inside the usecases module, is importing the Item model from the item subpackage, as well as one of the repository methods, so it means that is trying to get data directly from the underlying database tables owned by the item subpackage. Apart from this, if I didn't miss anything else, there should be some code duplication needed, given that both subpackages are using common code in the root of the main package, where there's also the app entrypoint that exposes the asgi app necessary to start the server.
2. The models definitions are intertwined with some database details, in particular with a relational database flavour. Instead the models should be as agnostic as they can, since it should be possible to store them in many different ways and shapes, where potentially sql concepts do not apply in the same way. Also, the usecases are directly importing from the repository module, instead of receiving an instance of a known interface through dependency injection. Moreover, the usecases module of the user subpackage is also raising HTTPExceptions, which breaks the clean architecture rule of inner layers not using components from an outer layer. 
3. Define a repository interface, subclass it with a specific implementation (e.g. postgres) that should be then instantiated before calling the usecases, passing it as a dependency. Then refactor the models using pydantic (or native dataclasses), and define new models at the repository implementation level that map them in the specific chosen flavour of database. Lastly, to fix the HTTPExceptions problem, I would define and then raise some native exception classes in the usecases module, which would then be catched in the api module to translate them in the appropriate http status.
4. I never saw it as a big problem, since it's a pattern that once explained, it's pretty easy to follow, and to spot possible mistakes during code reviews. Anyway, if we're talking strictly about what a module can or cannot import, one idea that came to mind (even if I'm not sure it's 100% feasible) is to define a precise set of module names to use, and then use some code introspection inside a linting script to verify that each module contains only imports of inner modules.


Stretch goals:
* Fork the repository and start refactoring
* Write meaningful tests
* Replace the SQL repository with an in-memory implementation

## References
* [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Clean Architecture in Python](https://www.youtube.com/watch?v=C7MRkqP5NRI)
* [A detailed summary of the Clean Architecture book by Uncle Bob](https://github.com/serodriguez68/clean-architecture)

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.