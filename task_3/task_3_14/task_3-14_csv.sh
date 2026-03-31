#!/bin/bash
echo "1. Названия товаров:"
awk -F "," '{print $2}' data.csv
echo ""

echo "2. Товары дороже 20:"
awk -F "," '$3 > 20 {print $2, "-", $3}' data.csv
echo ""

echo "3. Общая стоимость:"
awk -F "," '{sum += $3} END {print sum}' data.csv
