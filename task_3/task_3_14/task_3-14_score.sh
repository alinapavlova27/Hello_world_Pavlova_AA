#!/bin/bash
echo "1. Студенты с оценкой выше 80:"
awk '$2 > 80 {print $1, $2}' students.txt
echo ""

echo "2. Студенты с оценкой ниже 70:"
awk '$2 < 70 {print $1, $2}' students.txt
echo ""

echo "3. Первая строка файла:"
awk 'NR == 1 {print $0}' students.txt
