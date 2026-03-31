#!/bin/bash
check_root() {
    if [ $EUID -ne 0 ]; then
        echo "Требуется root"
        return 1
    fi
    echo "Скрипт запущен от имени root"
    return 0
}

check_root
