# Watcher.py

Утилита наблюдения за изменением директории или файла. 
Имеет три консольных способа запуска, отличие только в способе подачи аргументов скрипту.

## Аргументы
Скрипт должен принять два аргумента:

- Путь - Директория наблюдения
- Команда - Bash команда выполняющаяся при каждом изменение директории

## Запуск с файла

Аргументы передаются в файле формата JSON

**config.json**
```json
{
  "watcher_directory": "temp/",
  "watcher_command": "php -f script.php < config.json"
}
```

> Ключи "watcher_directory" "watcher_command" обязательны

**bash**
```bash
python3 watcher.py config.json
```


## Запуск консольный с параметрами

На этот раз аргументы передаются в терминальной строке, первый аргумент Путь, второй Команда

**bash**
```bash
python3 watcher.py 'temp/' 'php -f script.php < config.json'
```


## Установить и добавить ссылку

**bash**
```bash
cd /opt
git clone THIS_RIPO
ln -sf /opt/watcher/watcher.py /usr/local/bin/watcher
chmod +x /usr/local/bin/watcher
```

Или установить на прямую:

**bash**
```bash
cp watcher.py /usr/local/bin/watcher
```