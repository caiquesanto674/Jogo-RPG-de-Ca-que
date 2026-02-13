import unittest
from datetime import datetime
from apolo_engine.systems.time import TimeSystem

class TestTimeSystem(unittest.TestCase):

    def setUp(self):
        self.time_system = TimeSystem(starting_year=2026)

    def test_initialization(self):
        self.assertEqual(self.time_system.current_year, 2026)
        self.assertEqual(self.time_system.day_of_year, 1)
        self.assertEqual(self.time_system.tick_count, 0)

    def test_advance_time_without_day_change(self):
        self.time_system.advance_time(50)
        self.assertEqual(self.time_system.tick_count, 50)
        self.assertEqual(self.time_system.day_of_year, 1)

    def test_advance_time_with_day_change(self):
        self.time_system.advance_time(150)
        self.assertEqual(self.time_system.tick_count, 50)
        self.assertEqual(self.time_system.day_of_year, 2)

    def test_advance_time_with_year_change(self):
        self.time_system.day_of_year = 365
        self.time_system.advance_time(100)
        self.assertEqual(self.time_system.current_year, 2027)
        self.assertEqual(self.time_system.day_of_year, 1)

    def test_leap_year(self):
        time_system_leap = TimeSystem(starting_year=2024)
        time_system_leap.day_of_year = 366
        time_system_leap.advance_time(100)
        self.assertEqual(time_system_leap.current_year, 2025)
        self.assertEqual(time_system_leap.day_of_year, 1)
        self.assertEqual(time_system_leap.days_per_month['February'], 28)

    def test_get_detailed_game_date(self):
        data = self.time_system.get_detailed_game_date()
        self.assertEqual(data['game_year'], 2026)
        self.assertEqual(data['game_month'], 'January')
        self.assertEqual(data['game_day'], 1)

    def test_generate_simple_annual_calendar(self):
        calendar = self.time_system.generate_simple_annual_calendar(2026)
        self.assertIn('January', calendar)
        self.assertEqual(len(calendar['January']), 5)

if __name__ == '__main__':
    unittest.main()
