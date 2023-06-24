## Motivation

Are you a Django developer? Are you bored and want to try something else but fill at home ? [fastapi](https://fastapi.tiangolo.com/) perhaps?
Then this project can be relevant to you. This project is a setup of the well known fastapi web framework and [tortoise-orm](https://tortoise.github.io/index.html),
an async-based ORM that is inspired by Django ORM. This project is aimed to alleviate the hustle of going through a long
steps of configuration of fastapi project before having something that suits your development workflow. It is just as project
stater that you can customize it to suite your needs. It is not aimed to be framework or something like that. Fill free to fork and customize. Happy coding 😄.

## Limitations

The current setup is not suited for parallel test running, because it supposes that all tests are running on a the same test database instance.
