SELECT category, COUNT(*) AS products_count
FROM products
GROUP BY category;

SELECT category, COUNT(*) AS products_count
FROM products
GROUP BY category
ORDER BY products_count DESC;