


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
