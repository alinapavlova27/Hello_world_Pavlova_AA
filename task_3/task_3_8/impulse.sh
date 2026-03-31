#!/bin/bash

if [ $# -eq 2 ]; then
    gene_name="$1"
    expression_level="$2"
elif [ $# -eq 1 ]; then
    echo "Ошибка: недостаточно входящих данных."
    gene_name="$1"
    read -p "Введите уровень экспрессии: " expression_level
else
    echo "Ошибка: недостаточно входящих данных."
    read -p "Введите имя гена: " gene_name
    read -p "Введите уровень экспрессии: " expression_level
fi

echo "Экспрессия гена $gene_name составляет $expression_level единиц"
