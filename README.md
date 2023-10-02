Как запустить проект:
Все описанное ниже относится к ОС Linux.

Клонируем репозиторий и и переходим в него:
git clone git@github.com:themasterid/yamdb_final.git
cd yamdb_final
Создаем и активируем виртуальное окружение:
python3 -m venv venv
Windows:
source venv/Scripts/activate
Linux:
source venv/bin/activate
Обновим pip:
python -m pip install --upgrade pip 
Ставим зависимости из requirements.txt:
pip install -r api_yamdb/requirements.txt 