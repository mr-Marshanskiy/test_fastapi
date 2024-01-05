# fastapi-test

Clone this repository and install using `pip`.

```bash
$ pip install --editable .
```

## How to run

Configure the relevant DSN string to your Postgres backend database in `.env` file, 
or provide it from the environment variable `MYAPI_DATABASE__DSN`.

To run the application use following.

```bash
$ uvicorn app.main:app
```

## License

MIT License (see [LICENSE](LICENSE)).