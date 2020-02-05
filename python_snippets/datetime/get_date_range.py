# pip install python-dateutil==2.8.1

import enum
from datetime import datetime, timedelta
from functools import partial
from typing import NamedTuple, List
from dateutil import parser
from werkzeug.exceptions import BadRequest
from dateutil.relativedelta import relativedelta


class DateTimeParams(NamedTuple):
    from_time: datetime
    to_time: datetime


class IntervalTime(enum.Enum):

    def __call__(self, *args, **kwargs):
        self.value(*args)

    @classmethod
    def entity(cls, value):
        return cls._member_map_.get(value)

    @classmethod
    def timedelta(cls, interval_value, interval_type) -> timedelta:
        return cls.entity(interval_type).value(interval_value)

    @classmethod
    def get_interval_by_bucket(cls, bucket: str):
        interval_timedelta = cls.timedelta(1, bucket)
        return interval_timedelta

    seconds = partial(lambda interval_value: timedelta(seconds=interval_value))
    minutes = partial(lambda interval_value: timedelta(minutes=interval_value))
    hours = partial(lambda interval_value: timedelta(hours=interval_value))
    days = partial(lambda interval_value: timedelta(days=interval_value))
    weeks = partial(lambda interval_value: timedelta(weeks=interval_value))
    months = partial(lambda interval_value: relativedelta(months=interval_value))
    years = partial(lambda interval_value: relativedelta(years=interval_value))


def current_utc_time() -> str:
    return datetime.utcnow().isoformat(timespec='seconds')


def datetime2str(date_time: datetime, timespec: str = 'seconds') -> str:
    return date_time.isoformat(timespec=timespec)


def time2str_by_format(date_time: datetime, format_str: str = '%Y%m%d%H%M') -> str:
    return date_time.strftime(format_str)


def str2datetime(str_time: str) -> datetime:
    return datetime.strptime(str_time, '%Y-%m-%dT%H:%M:%S')


def validate_time(from_time: datetime, to_time: datetime):
    if from_time > to_time:
        raise BadRequest('The from_time must not be bigger than to_time.')


def get_datetime_params(from_time: str, to_time: str) -> DateTimeParams:
    from_time = parser.parse(from_time)
    to_time = parser.parse(to_time)
    validate_time(from_time, to_time)

    return DateTimeParams(from_time=from_time, to_time=to_time)


def get_diff_seconds(from_time: datetime, to_time: datetime):
    return int((to_time - from_time).total_seconds())


def diff_second2timedelta(from_time: datetime, to_time: datetime):
    seconds = get_diff_seconds(from_time, to_time)
    return IntervalTime.timedelta(seconds, IntervalTime.seconds.name)


def get_date_range(from_time: datetime, to_time: datetime, bucket: str) -> List[dict]:
    dates = []
    interval_timedelta = IntervalTime.get_interval_by_bucket(bucket)
    post_second = timedelta(seconds=1)

    while True:
        date = dict()
        if from_time < to_time:
            if from_time + interval_timedelta <= to_time:
                date.update({'from': from_time})
                # to 는 다음 from - 1s
                date.update({'to': from_time + interval_timedelta - post_second})
                dates.append(date)
                from_time = date.get('to') + post_second
            else:
                interval_timedelta = diff_second2timedelta(from_time, to_time)
                # 일정 버킷 이후에 남는 자투리 시간차로 버킷 생성
                if interval_timedelta.total_seconds() != 0:
                    date.update({'from': from_time})
                    date.update({'to': from_time + interval_timedelta - post_second})
                    dates.append(date)
                    break
    return dates
