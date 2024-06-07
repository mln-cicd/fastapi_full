


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
```



METADATA: typing.Final = sa.MetaData()


class Base(orm.DeclarativeBase):



git remote set-url origin git@github.com-mln-cicd/fastapi_full.git
git remote set-url origin git@github.com-mln-cicd:mln-cicd/fastapi_full.git