from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin
from pytz import timezone


KST = timezone("Asia/Seoul")

@declarative_mixin
class TimeStamp:
    created_at = Column(DateTime, default=datetime.now(tz=KST), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(tz=KST), nullable=False)