#!/bin/bash
read -p "Введите массу в кг: " weight
read -p "Введите рост в см: " height_cm
height_m=$(echo "scale=2; $height_cm / 100" | bc)
bmi=$(echo "scale=0; $weight / ($height_m * $height_m)" | bc)
echo "Индекс массы тела (BMI): $bmi"
