import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from datetime import datetime, timedelta

class MarkowitzOptimizer:
    def __init__(self):
        self.stocks = None
        self.returns = None
        self.mean_returns = None
        self.cov_matrix = None
        self.num_assets = None
        
    def fetch_data(self, tickers, start_date, end_date):
        """
        Fetch historical stock data from Yahoo Finance
        """
        try:
            # Download stock data
            data = pd.DataFrame()
            for ticker in tickers:
                stock_data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
                data[ticker] = stock_data
            
            self.stocks = data
            # Calculate daily returns
            self.returns = data.pct_change()
            # Calculate mean returns and covariance matrix
            self.mean_returns = self.returns.mean()
            self.cov_matrix = self.returns.cov()
            self.num_assets = len(tickers)
            
            return True
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return False

    def portfolio_performance(self, weights):
        """
        Calculate portfolio return and volatility
        """
        returns = np.sum(self.mean_returns * weights) * 252  # Annualized return
        volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
        return returns, volatility

    def negative_sharpe_ratio(self, weights):
        """
        Calculate negative Sharpe ratio (for minimization)
        """
        p_ret, p_vol = self.portfolio_performance(weights)
        risk_free_rate = 0.02  # Assuming 2% risk-free rate
        return -(p_ret - risk_free_rate) / p_vol

    def optimize_portfolio(self):
        """
        Optimize portfolio weights using Sharpe Ratio
        """
        # Constraints
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
        )
        # Bounds for weights (0 to 1)
        bounds = tuple((0, 1) for _ in range(self.num_assets))
        # Initial guess (equal weights)
        initial_weights = np.array([1/self.num_assets] * self.num_assets)
        
        # Optimize
        result = minimize(
            self.negative_sharpe_ratio,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result

    def plot_efficient_frontier(self, num_portfolios=1000):
        """
        Plot the efficient frontier
        """
        returns = []
        volatilities = []
        
        for _ in range(num_portfolios):
            weights = np.random.random(self.num_assets)
            weights = weights / np.sum(weights)
            p_ret, p_vol = self.portfolio_performance(weights)
            returns.append(p_ret)
            volatilities.append(p_vol)
            
        # Plot random portfolios
        plt.figure(figsize=(10, 6))
        plt.scatter(volatilities, returns, c='b', marker='o', s=10, alpha=0.3)
        
        # Plot optimal portfolio
        optimal_weights = self.optimize_portfolio().x
        opt_ret, opt_vol = self.portfolio_performance(optimal_weights)
        plt.scatter(opt_vol, opt_ret, c='r', marker='*', s=200, label='Optimal Portfolio')
        
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.title('Efficient Frontier')
        plt.legend()
        plt.show()

def main():
    # Example usage
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*3)  # 3 years of data
    
    # Initialize optimizer
    optimizer = MarkowitzOptimizer()
    
    # Fetch data
    if optimizer.fetch_data(tickers, start_date, end_date):
        # Optimize portfolio
        result = optimizer.optimize_portfolio()
        optimal_weights = result.x
        
        # Print results
        print("\nOptimal Portfolio Weights:")
        for ticker, weight in zip(tickers, optimal_weights):
            print(f"{ticker}: {weight:.4f}")
        
        # Calculate portfolio performance
        returns, volatility = optimizer.portfolio_performance(optimal_weights)
        print(f"\nPortfolio Performance:")
        print(f"Expected Annual Return: {returns:.4f}")
        print(f"Annual Volatility: {volatility:.4f}")
        print(f"Sharpe Ratio: {(returns - 0.02) / volatility:.4f}")
        
        # Plot efficient frontier
        optimizer.plot_efficient_frontier()

if __name__ == "__main__":
    main()
