import random
import statistics
from datetime import datetime
random.seed(datetime.now())


increasing = True
decreasing = False


class VolumeData:
    def __init__(self, price_up, price_down):
        self.price_up = price_up
        self.price_down = price_down


def if_modify(prob):
    return random.random() < prob


class Generator:
    def __init__(self, prices, volumes):
        assert len(prices) == len(volumes)
        self.prices = prices
        self.volumes = volumes
        self.price_diffs = []
        self.volume_diffs = []
        self.total = len(prices)
        self.volumes_down = []
        self.volumes_up = []
        self.volume_trend_keeps_up = []
        self.volume_trend_keeps_down = []
        self.volume_trend_change_to_up = []
        self.volume_trend_change_to_down = []
        self.volume_average = statistics.mean(self.volumes)
        self.volumes_dev = statistics.stdev(self.volumes)
        self.generate_stats()

    def generate_stats(self):
        volume_trend = increasing  # need to initialize somehow
        self.price_diffs.append(0.0)
        self.volume_diffs.append(0.0)
        for i in range(1, len(self.prices)):
            self.price_diffs.append(self.prices[i] - self.prices[i - 1])
            self.volume_diffs.append(self.volumes[i] - self.volumes[i - 1])
            if self.volume_diffs[i] > 0:
                self.volumes_up.append(self.price_diffs[i] / self.prices[i])
                if volume_trend == increasing:
                    self.volume_trend_keeps_up.append(self.volume_diffs[i] / self.volumes[i])
                else:
                    self.volume_trend_change_to_up.append(self.volume_diffs[i] / self.volumes[i])
                    volume_trend = increasing
            else:
                self.volumes_down.append(self.price_diffs[i] / self.prices[i])
                if volume_trend == decreasing:
                    self.volume_trend_keeps_down.append(self.volume_diffs[i] / self.volumes[i])
                else:
                    self.volume_trend_change_to_down.append(self.volume_diffs[i] / self.volumes[i])
                    volume_trend = decreasing

    def generate_price(self, volume_trend, current_price):
        if volume_trend == increasing:
            cases = self.volumes_up
        else:
            cases = self.volumes_down
        return cases[random.randrange(len(cases))] * current_price + current_price

    def regulate_decrease(self, volumes, index):
        if index == 0:
            return 0.0
        standard_min = self.volume_average - self.volumes_dev
        prob = 0.0
        if standard_min > volumes:
            prob = 1 - (volumes / standard_min)
        return prob

    def generate_volume(self, current_volume, current_trend):
        if current_trend == increasing:
            volume_increase = self.volume_trend_keeps_up
            volume_decrease = self.volume_trend_change_to_down
        else:
            volume_decrease = self.volume_trend_keeps_down
            volume_increase = self.volume_trend_change_to_up
        total_cases = len(volume_increase) + len(volume_decrease)
        bound = len(volume_increase)
        index = random.randrange(total_cases)
        modify_prob = self.regulate_decrease(current_volume, index)
        if if_modify(modify_prob):
            index = random.randrange(index)
        if index < bound:
            diff = volume_increase[index]
        else:
            index = index - bound
            diff = volume_decrease[index]
        new_volume = current_volume * diff + current_volume
        return new_volume

    def forecast(self):
        current_volume = self.volumes[-1]
        current_price = self.prices[-1]
        volume_trend = self.volume_diffs[-1] > 0
        future_volumes = []
        future_prices = []
        for i in range(0, self.total):
            new_volume = self.generate_volume(current_volume, volume_trend)
            volume_trend = new_volume > current_volume
            future_volumes.append(current_volume)
            current_volume = new_volume
            new_price = self.generate_price(volume_trend, current_price)
            future_prices.append(new_price)
            current_price = new_price
        return future_prices, future_volumes


