#!/bin/bash
for i in {1..20}; do
    if [ $((i % 2)) -eq 0 ]; then
        continue
    fi

    if [ $i -eq 15 ]; then
        echo "Достигнуто число 15. Остановка."
        break
    fi

    echo "Нечетное число: $i"
done

