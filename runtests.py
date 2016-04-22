#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'favicon.tests.settings'
    if len(sys.argv) == 1:
        django.setup()
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        failures = test_runner.run_tests(["favicon.tests"])
        sys.exit(bool(failures))
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
