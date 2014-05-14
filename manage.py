#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    settings_module = "auf_savoirs_en_partage.settings"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
