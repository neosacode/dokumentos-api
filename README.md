# Dokumentos-api

### .env
This file contains configurations about instance:
- `SECRET_KEY=your_secret_key`
Used to generate a hash for prevent atacks

- DEBUG=True
To show error messages

- ALLOWED_HOSTS=exemple.com,localhost,127.0.0.1`
Define wich host can acess the system

- DATABASE_URL=postgres://db_username:db_password@db_host_ip_or_domain:5432/db_database_name`
Sets the Exchange database using a URL scheme provided by the [dj-database-url](https://github.com/kennethreitz/dj-database-url) Django package.
