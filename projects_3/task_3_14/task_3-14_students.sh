#!/bin/bash
echo "1. Имена студентов:"
awk '{print $1}' students.txt
echo ""

echo "2. Оценки студентов:"
awk '{print $2}' students.txt
echo ""

echo "3. Номер строки и имя студента:"
awk '{print NR, $1}' students.txt
