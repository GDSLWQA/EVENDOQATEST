import subprocess
import sys
import os

tests_in_order = [
    "tests.test_1_registration",
    "tests.test_2_login",
    "tests.test_3_password_reset",
    "tests.test_4_fill_profile", # <-- ДОБАВЬТЕ ЭТУ СТРОКУ
]

for module_name in tests_in_order:
    print(f"\n{'='*20} RUNNING: {module_name} {'='*20}")
    
    result = subprocess.run([sys.executable, "-m", module_name])
    
    if result.returncode != 0:
        print(f"\n{'❌'*10} FAILED: {module_name} {'❌'*10}")
        break
    else:
        print(f"\n{'✅'*10} PASSED: {module_name} {'✅'*10}")