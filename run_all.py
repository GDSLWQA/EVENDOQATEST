# Файл: run_all.py

import subprocess
import sys
import os

# Список тестов в правильном порядке
tests_in_order = [
    "tests/test_1_registration.py",
    "tests/test_2_login.py",
    "tests/test_3_password_reset.py",
]

for test_path in tests_in_order:
    # Преобразуем путь к файлу в имя модуля
    # Например, "tests/test_1_registration.py" -> "tests.test_1_registration"
    module_name = test_path.replace(os.path.sep, ".").replace(".py", "")
    
    print(f"\n{'='*20} ЗАПУСК: {module_name} {'='*20}")
    
    # Запускаем скрипт как модуль с флагом "-m"
    result = subprocess.run([sys.executable, "-m", module_name])
    
    if result.returncode != 0:
        print(f"\n{'!'*20} ОШИБКА: Модуль {module_name} завершился с ошибкой! {'!'*20}")
        break
    else:
        print(f"\n{'*'*20} УСПЕХ: Модуль {module_name} выполнен. {'*'*20}")