"""
Money Management Module
Calculates position sizing, risk/reward ratios, and stop-loss levels
"""
import logging
from typing import Dict, Tuple
from config import config

logger = logging.getLogger(__name__)

class MoneyManager:
    """
    Manages risk, position sizing, and profit targets
    """
    
    def __init__(self, account_balance: float, risk_percentage: float = None):
        """
        Initialize Money Manager
        
        Args:
            account_balance: Current account balance in USDT
            risk_percentage: Percentage of account to risk per trade (default from config)
        """
        self.account_balance = account_balance
        self.risk_percentage = risk_percentage or config.DEFAULT_RISK_PERCENTAGE
        self.position_size = config.DEFAULT_POSITION_SIZE
        self.daily_loss = 0.0
        self.daily_profit = 0.0
    
    def calculate_risk_amount(self) -> float:
        """
        Calculate the maximum amount to risk in one trade
        
        Returns:
            Risk amount in USDT
        """
        try:
            risk_amount = (self.account_balance * self.risk_percentage) / 100
            return risk_amount
        except Exception as e:
            logger.error(f"Error calculating risk amount: {e}")
            return 0.0
    
    def calculate_position_size(self, entry_price: float, stop_loss_price: float,
                               risk_amount: float = None) -> float:
        """
        Calculate position size based on entry, stop loss, and risk amount
        
        Args:
            entry_price: Entry price
            stop_loss_price: Stop loss price
            risk_amount: Amount to risk (uses calculated if not provided)
        
        Returns:
            Position size in base currency
        """
        try:
            if risk_amount is None:
                risk_amount = self.calculate_risk_amount()
            
            price_difference = abs(entry_price - stop_loss_price)
            
            if price_difference == 0:
                logger.warning("Price difference is zero, cannot calculate position size")
                return 0.0
            
            position_size = risk_amount / price_difference
            return round(position_size, 8)
        
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0.0
    
    def calculate_profit_targets(self, entry_price: float, stop_loss_price: float,
                                risk_reward_ratio: float = 2.0) -> Dict[str, float]:
        """
        Calculate take profit levels based on risk/reward ratio
        
        Args:
            entry_price: Entry price
            stop_loss_price: Stop loss price
            risk_reward_ratio: Desired risk/reward ratio
        
        Returns:
            Dictionary with TP1 and TP2 levels
        """
        try:
            risk_distance = abs(entry_price - stop_loss_price)
            
            # Determine direction
            if entry_price > stop_loss_price:  # Long position
                tp1 = entry_price + (risk_distance * config.TAKE_PROFIT_1_PERCENTAGE / 100)
                tp2 = entry_price + (risk_distance * config.TAKE_PROFIT_2_PERCENTAGE / 100)
                tp_full = entry_price + (risk_distance * risk_reward_ratio)
            else:  # Short position
                tp1 = entry_price - (risk_distance * config.TAKE_PROFIT_1_PERCENTAGE / 100)
                tp2 = entry_price - (risk_distance * config.TAKE_PROFIT_2_PERCENTAGE / 100)
                tp_full = entry_price - (risk_distance * risk_reward_ratio)
            
            return {
                'TP1': round(tp1, 8),
                'TP2': round(tp2, 8),
                'TP_FULL': round(tp_full, 8)
            }
        
        except Exception as e:
            logger.error(f"Error calculating profit targets: {e}")
            return {'TP1': 0.0, 'TP2': 0.0, 'TP_FULL': 0.0}
    
    def calculate_risk_reward_ratio(self, entry_price: float, 
                                   stop_loss_price: float,
                                   take_profit_price: float) -> float:
        """
        Calculate the risk/reward ratio for a trade
        
        Returns:
            Risk/reward ratio
        """
        try:
            risk = abs(entry_price - stop_loss_price)
            reward = abs(take_profit_price - entry_price)
            
            if risk == 0:
                return 0.0
            
            ratio = reward / risk
            return round(ratio, 2)
        
        except Exception as e:
            logger.error(f"Error calculating R/R ratio: {e}")
            return 0.0
    
    def calculate_stop_loss_by_atr(self, entry_price: float, atr: float,
                                   multiplier: float = 2.0,
                                   position_type: str = 'LONG') -> float:
        """
        Calculate stop loss based on ATR (Average True Range)
        
        Args:
            entry_price: Entry price
            atr: Average True Range value
            multiplier: ATR multiplier
            position_type: 'LONG' or 'SHORT'
        
        Returns:
            Stop loss price
        """
        try:
            atr_distance = atr * multiplier
            
            if position_type == 'LONG':
                stop_loss = entry_price - atr_distance
            else:
                stop_loss = entry_price + atr_distance
            
            return round(stop_loss, 8)
        
        except Exception as e:
            logger.error(f"Error calculating ATR stop loss: {e}")
            return 0.0
    
    def check_daily_loss_limit(self, loss_amount: float) -> bool:
        """
        Check if daily loss exceeds maximum allowed loss
        
        Args:
            loss_amount: Loss amount in USDT
        
        Returns:
            True if can trade, False if daily loss limit exceeded
        """
        try:
            max_daily_loss = (self.account_balance * config.MAX_DAILY_LOSS) / 100
            self.daily_loss += abs(loss_amount)
            
            if self.daily_loss > max_daily_loss:
                logger.warning(f"Daily loss limit exceeded: {self.daily_loss} > {max_daily_loss}")
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error checking daily loss limit: {e}")
            return False
    
    def update_daily_stats(self, profit_loss: float):
        """Update daily P&L statistics"""
        try:
            if profit_loss > 0:
                self.daily_profit += profit_loss
            else:
                self.daily_loss += abs(profit_loss)
        except Exception as e:
            logger.error(f"Error updating daily stats: {e}")
    
    def reset_daily_stats(self):
        """Reset daily statistics (call at start of each day)"""
        self.daily_loss = 0.0
        self.daily_profit = 0.0
    
    def get_account_summary(self) -> Dict:
        """Get account summary"""
        try:
            return {
                'account_balance': self.account_balance,
                'risk_percentage': self.risk_percentage,
                'risk_amount': self.calculate_risk_amount(),
                'daily_profit': self.daily_profit,
                'daily_loss': self.daily_loss,
                'daily_net': self.daily_profit - self.daily_loss,
                'max_daily_loss': (self.account_balance * config.MAX_DAILY_LOSS) / 100
            }
        except Exception as e:
            logger.error(f"Error getting account summary: {e}")
            return {}
