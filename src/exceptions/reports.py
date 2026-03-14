"""
Report exceptions
"""

from fastapi import HTTPException, status


class ReportNotExistsException(HTTPException):
    def __init__(self, detail: str = "Report not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
