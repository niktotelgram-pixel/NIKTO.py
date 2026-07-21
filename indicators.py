"""
Technical Indicators Module
Provides various technical analysis indicators
"""
import pandas as pd
import numpy as np
from ta import trend, momentum, volatility
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """Technical Analysis Indicators"""
    
    @staticmethod
    def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)
        """
        try:
            rsi = momentum.RSIIndicator(close=data['close'], window=period).rsi()
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return pd.Series(index=data.index, dtype=float)
    
    @staticmethod
    def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, 
                       signal: int = 9) -> tuple:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        Returns: (macd_line, signal_line, histogram)
        """
        try:
            macd = trend.MACD(close=data['close'], window_fast=fast, 
                            window_slow=slow, window_sign=signal)
            return (macd.macd(), macd.macd_signal(), macd.macd_diff())
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return (pd.Series(), pd.Series(), pd.Series())
    
    @staticmethod
    def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, 
                                  std: int = 2) -> tuple:
        """
        Calculate Bollinger Bands
        Returns: (upper_band, middle_band, lower_band)
        """
        try:
            bb = volatility.BollingerBands(close=data['close'], window=period, 
                                          window_dev=std)
            return (bb.bollinger_hband(), bb.bollinger_mavg(), 
                   bb.bollinger_lband())
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return (pd.Series(), pd.Series(), pd.Series())
    
    @staticmethod
    def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range (ATR)
        Measures volatility
        """
        try:
            atr = volatility.AverageTrueRange(high=data['high'], low=data['low'],
                                              close=data['close'], 
                                              window=period).average_true_range()
            return atr
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return pd.Series(index=data.index, dtype=float)
    
    @staticmethod
    def calculate_sma(data: pd.DataFrame, period: int) -> pd.Series:
        """
        Calculate Simple Moving Average (SMA)
        """
        try:
            return data['close'].rolling(window=period).mean()
        except Exception as e:
            logger.error(f"Error calculating SMA: {e}")
            return pd.Series(index=data.index, dtype=float)
    
    @staticmethod
    def calculate_ema(data: pd.DataFrame, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA)
        """
        try:
            return data['close'].ewm(span=period, adjust=False).mean()
        except Exception as e:
            logger.error(f"Error calculating EMA: {e}")
            return pd.Series(index=data.index, dtype=float)
    
    @staticmethod
    def calculate_stochastic(data: pd.DataFrame, k_period: int = 14, 
                            d_period: int = 3) -> tuple:
        """
        Calculate Stochastic Oscillator
        Returns: (k_line, d_line)
        """
        try:
            low_min = data['low'].rolling(window=k_period).min()
            high_max = data['high'].rolling(window=k_period).max()
            k_line = 100 * (data['close'] - low_min) / (high_max - low_min)
            d_line = k_line.rolling(window=d_period).mean()
            return (k_line, d_line)
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {e}")
            return (pd.Series(), pd.Series())
    
    @staticmethod
    def calculate_adx(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate Average Directional Index (ADX)
        Measures trend strength
        """
        try:
            adx = trend.ADXIndicator(high=data['high'], low=data['low'],
                                    close=data['close'], 
                                    window=period).adx()
            return adx
        except Exception as e:
            logger.error(f"Error calculating ADX: {e}")
            return pd.Series(index=data.index, dtype=float)
    
    @staticmethod
    def calculate_vpt(data: pd.DataFrame) -> pd.Series:
        """
        Calculate Volume Price Trend (VPT)
        """
        try:
            if 'volume' not in data.columns:
                return pd.Series(index=data.index, dtype=float)
            
            price_change = data['close'].pct_change()
            vpt = (price_change * data['volume']).cumsum()
            return vpt
        except Exception as e:
            logger.error(f"Error calculating VPT: {e}")
            return pd.Series(index=data.index, dtype=float)
    
    @staticmethod
    def add_all_indicators(data: pd.DataFrame) -> pd.DataFrame:
        """
        Add all indicators to dataframe
        """
        try:
            df = data.copy()
            
            # Momentum
            df['RSI'] = TechnicalIndicators.calculate_rsi(df)
            df['MACD'], df['MACD_SIGNAL'], df['MACD_HIST'] = TechnicalIndicators.calculate_macd(df)
            
            # Volatility
            df['BB_HIGH'], df['BB_MID'], df['BB_LOW'] = TechnicalIndicators.calculate_bollinger_bands(df)
            df['ATR'] = TechnicalIndicators.calculate_atr(df)
            
            # Trend
            df['SMA_20'] = TechnicalIndicators.calculate_sma(df, 20)
            df['SMA_50'] = TechnicalIndicators.calculate_sma(df, 50)
            df['EMA_12'] = TechnicalIndicators.calculate_ema(df, 12)
            df['EMA_26'] = TechnicalIndicators.calculate_ema(df, 26)
            df['ADX'] = TechnicalIndicators.calculate_adx(df)
            
            # Stochastic
            df['STOCH_K'], df['STOCH_D'] = TechnicalIndicators.calculate_stochastic(df)
            
            # Volume
            df['VPT'] = TechnicalIndicators.calculate_vpt(df)
            
            return df
        except Exception as e:
            logger.error(f"Error adding all indicators: {e}")
            return data
