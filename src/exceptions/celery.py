"""
celery exception
"""


class CeleryNotEnvs(Exception):
    def __init__(self, message="Cannot find neccessary envs for celery setup"):
        super().__init__(message)
