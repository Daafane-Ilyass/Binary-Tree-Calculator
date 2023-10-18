# Imports
import numpy as np
import math as m


class BinomialTreeModel:
    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps, option_type):
        self.S = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity
        self.r = risk_free_rate
        self.sigma = sigma
        self.number_of_time_steps = number_of_time_steps
        self.option_type = option_type

    def calculate_option_prices(self):
        dt = self.T / self.number_of_time_steps
        u = m.exp(self.sigma * m.sqrt(dt))
        d = 1.0 / u
        price_matrix = np.zeros(
            (self.number_of_time_steps + 1, self.number_of_time_steps + 1))

        for j in range(self.number_of_time_steps + 1):
            for i in range(j + 1):
                price_matrix[i, j] = self.S * m.pow(d, i) * m.pow(u, j - i)

        # Calculate European option prices
        # option_prices = self.calculate_european_option_prices(price_matrix)

        return price_matrix

    def calculate_european_option_prices(self, price_matrix):
        n = self.number_of_time_steps
        S = self.S
        K = self.K
        r = self.r
        v = self.sigma
        T = self.T
        putMatrix, callMatrix = self.OptionsVal(n, S, K, r, v, T, price_matrix)

        # You can return putMatrix and callMatrix or any specific values as per your requirement
        return putMatrix, callMatrix

    def OptionsVal(self, n, S, K, r, v, T, priceMatrix):
        dt = T/n
        u = m.exp(v*m.sqrt(dt))
        d = 1/u
        p = (m.exp(r*dt)-d)/(u-d)
        putMatrix = np.zeros((n+1, n+1))
        callMatrix = np.zeros((n+1, n+1))

        for j in range(n+1, 0, -1):
            for i in range(j):
                if (j == n+1):
                    putMatrix[i, j-1] = max(K-priceMatrix[i, j-1], 0)
                    callMatrix[i, j-1] = max(priceMatrix[i, j-1]-K, 0)
                else:
                    putMatrix[i, j-1] = m.exp(-r*dt) * \
                        (p*putMatrix[i, j] + (1-p)*putMatrix[i+1, j])
                    callMatrix[i, j-1] = m.exp(-r*dt) * \
                        (p*callMatrix[i, j] + (1-p)*callMatrix[i+1, j])

        return putMatrix, callMatrix
