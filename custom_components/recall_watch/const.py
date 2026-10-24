"""Constants and compatibility defaults for Recall Watch."""

from datetime import timedelta

DOMAIN = "recall_watch"
CONF_KEYWORDS = "keywords"
CONF_SOURCE = "source"
SOURCE_ID = "se_food"
SOURCE_NAME = "Swedish Food Agency"
SCAN_INTERVAL = timedelta(hours=6)
