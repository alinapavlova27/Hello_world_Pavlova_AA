for i in {1..10}; do
    touch "test$i.txt"
    echo "Создан файл: test$i.txt"
done

counter=10
while [ $counter -ge 1 ]; do
    echo "Удаляю файл: test$counter.txt"
    rm "test$counter.txt"
    ((counter--))
    sleep 1
done
