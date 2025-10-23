# File: run_api_tests.py

import subprocess
import sys
import os

tests_in_order = [
    "api_tests.test_1_registration",
    "api_tests.test_2_login",
    "api_tests.test_3_password_reset",
    "api_tests.test_4_fill_profile",
    "api_tests.test_5_change_password",
]

for module_name in tests_in_order:
    print(f"\n{'='*20} RUNNING API TEST: {module_name} {'='*20}")
    
    result = subprocess.run([sys.executable, "-m", module_name])
    
    if result.returncode != 0:
        print(f"\n{'❌'*10} FAILED: {module_name} {'❌'*10}")
        break
    else:
        print(f"\n{'✅'*10} PASSED: {module_name} {'✅'*10}")