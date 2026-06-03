SELECT * 
FROM prices 
WHERE price < 1000;

UPDATE prices
SET price = price * 1.10
WHERE price < 1000;