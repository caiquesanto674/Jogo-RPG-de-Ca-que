import datetime
import pytz
import calendar
from typing import Dict, Any, List, Optional

DEFAULT_TIMEZONE = 'America/Sao_Paulo'
GLOBAL_TIMEZONES = {
    "BRT": 'America/Sao_Paulo',
    "UTC": 'UTC',
    "CET": 'Europe/Paris',
    "JST": 'Asia/Tokyo'
}

class TimeSystem:
    def __init__(self, starting_year: int = 2026):
        self.current_year = starting_year
        self.day_of_year = 1
        self.tick_count = 0
        self.days_per_month = self._get_days_per_month(starting_year)

        self.default_timezone = pytz.timezone(DEFAULT_TIMEZONE)
        self.default_real_date = datetime.datetime.now(self.default_timezone)

    def _get_days_per_month(self, year: int) -> Dict[str, int]:
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        return {
            "January": 31, "February": 29 if is_leap else 28, "March": 31,
            "April": 30, "May": 31, "June": 30, "July": 31, "August": 31,
            "September": 30, "October": 31, "November": 30, "December": 31
        }

    def advance_time(self, ticks: int = 1):
        self.tick_count += ticks
        days_to_advance = self.tick_count // 100

        if days_to_advance > 0:
            self.tick_count %= 100

            current_date = datetime.date(self.current_year, 1, 1) + datetime.timedelta(days=self.day_of_year - 1)
            new_date = current_date + datetime.timedelta(days=days_to_advance)

            self.current_year = new_date.year
            self.day_of_year = new_date.timetuple().tm_yday

            if new_date.year != current_date.year:
                 self.days_per_month = self._get_days_per_month(self.current_year)

            self.default_real_date = datetime.datetime.now(self.default_timezone)

    def get_detailed_game_date(self) -> Dict[str, Any]:
        date = datetime.date(self.current_year, 1, 1) + datetime.timedelta(days=self.day_of_year - 1)

        utc_time = datetime.datetime.now(pytz.utc).strftime('%H:%M:%S UTC')

        return {
            "game_day": date.day,
            "game_month": date.strftime("%B"),
            "game_year": date.year,
            "game_day_of_week": date.strftime("%A"),
            "day_of_year": self.day_of_year,
            "universal_time_reference": utc_time
        }

    def get_simulated_timezone(self, zone: str) -> Optional[datetime.datetime]:
        if zone not in GLOBAL_TIMEZONES:
            return None

        tz = pytz.timezone(GLOBAL_TIMEZONES[zone])
        return datetime.datetime.now(tz)

    def generate_simple_annual_calendar(self, year: int) -> Dict[str, List[List[str]]]:
        annual_calendar = {}
        for month in range(1, 13):
            month_matrix = calendar.monthcalendar(year, month)
            month_name = calendar.month_name[month]
            formatted_days = []
            for week in month_matrix:
                formatted_days.append([str(day) if day != 0 else ' ' for day in week])
            annual_calendar[month_name] = formatted_days
        return annual_calendar
