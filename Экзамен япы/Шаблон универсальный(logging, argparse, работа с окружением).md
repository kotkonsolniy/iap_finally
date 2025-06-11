
Виртуальное окружение:
```python
python -m venv venv 
venv/Scripts/activate
pip freeze
pip freeze > requirements.txt
venv/Scripts/deactivate
```

Логирование и аргпарс:
```python
import logging
import argparse
import sys


logging.basicConfig(
    level=logging.DEBUG,
    filename='scanner.log',
    filemode='a',
    encoding='utf-8',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

parser = argparse.ArgumentParser() 
parser.add_argument('-host', type=str, default='172.16.243.129', help='Хост')
parser.add_argument('-v', '--verbose', action='store_true', help='Выводить дополнительную информацию')
args = parser.parse_args()
if args.verbose:
        print(f"Получены аргументы: {args}")
host = args.host
# if len(sys.argv) == 2:
#     host = args.host
# else:
#     host = '172.16.243.129'
```

