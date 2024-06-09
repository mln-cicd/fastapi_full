


```sql

INSERT INTO products (
	name, price, inventory
	)
VALUES (
	'Scooter', 1150, 42
) returning *;



DELETE FROM products
WHERE inventory = 0;

UPDATE products SET name = 'flour tortilla'
WHERE id = 4;

SELECT posts.*, COUNT(votes.post_id) FROM posts
LEFT JOIN votes on post.id = votes.id WHERE posts.id = 1
```



METADATA: typing.Final = sa.MetaData()


class Base(orm.DeclarativeBase):



git remote set-url origin git@github.com-mln-cicd/fastapi_full.git
git remote set-url origin git@github.com-mln-cicd:mln-cicd/fastapi_full.git



in the VM

```sh

# Display env variables
cd ~ && ls -la



# export env variables from a .env file
set -o allexport; source /home/<user>/.env; set +o allexport


# To make it permanent, insert the line from above in:
nano .profile


#gunicorn process manager
pip install httptools uviloop gunicorn

# start with 4 uvicorn workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:80

# nginx
sudo apt install nginx -y

```

Get pytest to hide warnings and stop as soon as there's a failed test (`-x`):
```py
pytest -s -v --disable-warnings
```
