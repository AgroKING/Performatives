"""
Application Constants

Centralized constants to avoid magic numbers and strings.
"""

from typing import Final

# JWT Configuration
JWT_ALGORITHM: Final[str] = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 60
TOKEN_TYPE: Final[str] = "bearer"

# Pagination
DEFAULT_PAGE_SIZE: Final[int] = 50
MAX_PAGE_SIZE: Final[int] = 100
MIN_PAGE_NUMBER: Final[int] = 1

# Password Requirements
MIN_PASSWORD_LENGTH: Final[int] = 8
PASSWORD_REQUIRE_UPPERCASE: Final[bool] = True
PASSWORD_REQUIRE_LOWERCASE: Final[bool] = True
PASSWORD_REQUIRE_DIGIT: Final[bool] = True

# Username Requirements
MIN_USERNAME_LENGTH: Final[int] = 3
MAX_USERNAME_LENGTH: Final[int] = 100

# Email Configuration
MAX_EMAIL_LENGTH: Final[int] = 255

# Database
DB_POOL_SIZE: Final[int] = 5
DB_MAX_OVERFLOW: Final[int] = 10
DB_POOL_TIMEOUT: Final[int] = 30

# HTTP Status Codes
HTTP_200_OK: Final[int] = 200
HTTP_201_CREATED: Final[int] = 201
HTTP_204_NO_CONTENT: Final[int] = 204
HTTP_400_BAD_REQUEST: Final[int] = 400
HTTP_401_UNAUTHORIZED: Final[int] = 401
HTTP_403_FORBIDDEN: Final[int] = 403
HTTP_404_NOT_FOUND: Final[int] = 404
HTTP_422_UNPROCESSABLE_ENTITY: Final[int] = 422
HTTP_500_INTERNAL_SERVER_ERROR: Final[int] = 500

# Time Conversions
SECONDS_PER_HOUR: Final[int] = 3600
SECONDS_PER_DAY: Final[int] = 86400
HOURS_PER_DAY: Final[int] = 24

# Application Status Colors (for Chart.js)
COLOR_BLUE: Final[str] = "#3B82F6"
COLOR_GREEN: Final[str] = "#10B981"
COLOR_ORANGE: Final[str] = "#F59E0B"
COLOR_RED: Final[str] = "#EF4444"
COLOR_PURPLE: Final[str] = "#8B5CF6"

# Statistics
DEFAULT_STATS_DAYS: Final[int] = 30
MAX_STATS_DAYS: Final[int] = 365

# Logging
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

# API
API_V1_PREFIX: Final[str] = "/api/v1"

# CORS
DEFAULT_ALLOWED_ORIGINS: Final[list[str]] = [
    "http://localhost:3000",
    "http://localhost:8080"
]
