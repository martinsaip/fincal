import pytz
import pandas as pd

class Venue:
    def __init__(self, timezone, regular_trading_hours, pre_regular_trading_hours, post_regular_trading_hours,
                 default_partial_trading_hours, regular_trading_days, partial_trading_days, non_trading_days,
                 data_provided_from_date, data_provided_through_date, market_holidays):
        self.timezone = pytz.timezone(timezone)
        #TODO: This code is brittle, and assumes alignment between the derived class and base class around gte/lte
        self.regular_trading_hours = [
            {"start": pd.Timestamp(trading_hours["gte"]), "end": pd.Timestamp(trading_hours["lt"])} for
            trading_hours in regular_trading_hours]

        # self.regular_trading_hours = [self._create_date_range(trading_hours)
        #                               for trading_hours in regular_trading_hours]
        # self.pre_regular_trading_hours = [self._create_date_range(trading_hours)
        #                                   for trading_hours in pre_regular_trading_hours]
        # self.post_regular_trading_hours = [self._create_date_range(trading_hours)
        #                                    for trading_hours in post_regular_trading_hours]
        self.default_partial_trading_hours = [
            {"start": pd.Timestamp(trading_hours["gte"]), "end": pd.Timestamp(trading_hours["lt"])} for
            trading_hours in regular_trading_hours]
        # self.default_partial_trading_hours = [self._create_date_range(trading_hours)
        #                                       for trading_hours in default_partial_trading_hours]
        self.regular_trading_days = regular_trading_days
        self.partial_trading_days = partial_trading_days
        self.non_trading_days = non_trading_days
        self.data_provided_from_date = data_provided_from_date
        self.data_provided_through_date = data_provided_through_date
        self.market_holidays = market_holidays

    @staticmethod
    def _create_date_range(trading_hours):
        start_key = next((key for key in ['gte', 'gt'] if key in trading_hours), None)
        end_key = next((key for key in ['lte', 'lt'] if key in trading_hours), None)

        start = pd.Timestamp(trading_hours[start_key])
        end = pd.Timestamp(trading_hours[end_key])

        if start_key == 'gt':
            start += pd.Timedelta(1, unit='ns')

        if end_key == 'lt':
            end -= pd.Timedelta(1, unit='ns')

        return pd.date_range(start=start, end=end, freq='N')

    def is_trading_time(self, timestamp):
        day_str = timestamp.strftime('%Y-%m-%d')

        # Get trading hours for the given day
        trading_hours, reason = self.get_trading_hours(day_str)

        # Return True if bool(x) is True for any x in the iterable. If the iterable is empty, return False.
        return any(
            period["start"] <= timestamp <= period["end"]
            for period in trading_hours
        )

    # TODO: Overload the boolean is_xxx_day functions with a version that also returns the reason
    # def is_non_trading_day(self, day, reason):

    def is_regular_trading_day(self, day):
        # Is this a day where trading will happen during the usual hours?
        _, reason = self.get_trading_hours(day)
        return reason == "Regular Trading Day"

    def is_non_trading_day(self, day, reason):
        # TODO: There should be a reason distinction between regular non-trading (weekends) and irregular non-trading
        # Is this a day where trading would normally have happened, but for some reason today will not?
        return day in self.non_trading_days

    def is_partial_trading_day(self, day):
        # Is this a day where regular trading hours would normally have occurred, but for some reason today will not?
        return day in self.partial_trading_days


    # TODO: create a "is_trading_moment" sort of function, to say whether trading was active at a given moment
    # Or maybe some interpolation of the expanded from/to intraday ranges, so you get a full and explicit picture of
    # 'hours' on any given trading day

    def get_trading_hours(self, day):
        day_of_week = pd.Timestamp(day).day_name()

        if self.is_non_trading_day(day):
            # TODO: get the non-trading reason from the overloaded is_xxx_reason
            # If it's a non-trading day, return an empty list and the reason
            return [], self.non_trading_days[day].get('reason', "Non-Trading Day")
        elif self.is_partial_trading_day(day):
            # Get trading hours for the given day using Python 3.8+ assignment expression (Walrus :=)
            # If 'hours' key exists in the dictionary for the given day, assign its value to 'trading_hours'
            # If 'hours' key doesn't exist, assign None to 'trading_hours'
            if trading_hours := self.partial_trading_days[day].get('hours'):
                # TODO: BRITTLE - This code assumes alignment between the derived class and base class around gte/lte
                return [{"start": pd.Timestamp(hour["gte"]), "end": pd.Timestamp(hour["lte"])} for hour in
                        trading_hours], self.partial_trading_days[day].get('reason', "Partial Trading Day")
            else:
                # 'trading_hours' is None, so return default partial hours
                # TODO: BRITTLE - This code assumes alignment between the derived class and base class around gte/lte
                return [{"start": pd.Timestamp(hour["gte"]), "end": pd.Timestamp(hour["lte"])} for hour in
                        self.default_partial_trading_hours], "Partial Trading Day"
        elif day_of_week in self.regular_trading_days:
            # TODO: exclude anticipated future holidays, beyond the hard-coded ones
            # If it isn't a partial or a non-trading day, it's a regular trading day, return regular hours
            return self.regular_trading_hours, "Regular Trading Day"
        else:
            # If it's not a regular trading day, return an empty list and "Non-Standard Trading Day" as the reason
            return [], "Non-Regular Trading Day"
