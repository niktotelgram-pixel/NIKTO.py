"""
Exchange Manager Module
Handles connections to multiple exchanges (Binance, LBank, MEXC)
"""
import ccxt
import logging
from typing import Dict, List, Optional
from config import config
import asyncio

logger = logging.getLogger(__name__)

class ExchangeManager:
    """
    Manages connections to multiple cryptocurrency exchanges
    """
    
    def __init__(self, exchange_name: str = 'binance'):
        """
        Initialize exchange connection
        
        Args:
            exchange_name: 'binance', 'lbank', or 'mexc'
        """
        self.exchange_name = exchange_name.lower()
        self.exchange = None
        self._initialize_exchange()
    
    def _initialize_exchange(self):
        """Initialize the selected exchange"""
        try:
            if self.exchange_name == 'binance':
                self.exchange = ccxt.binance({
                    'apiKey': config.BINANCE_API_KEY,
                    'secret': config.BINANCE_API_SECRET,
                    'enableRateLimit': True,
                })
            
            elif self.exchange_name == 'lbank':
                self.exchange = ccxt.lbank({
                    'apiKey': config.LBANK_API_KEY,
                    'secret': config.LBANK_API_SECRET,
                    'enableRateLimit': True,
                })
            
            elif self.exchange_name == 'mexc':
                self.exchange = ccxt.mexc({
                    'apiKey': config.MEXC_API_KEY,
                    'secret': config.MEXC_API_SECRET,
                    'enableRateLimit': True,
                })
            
            else:
                logger.error(f"Unsupported exchange: {self.exchange_name}")
                self.exchange = None
        
        except Exception as e:
            logger.error(f"Error initializing {self.exchange_name}: {e}")
            self.exchange = None
    
    def get_ohlcv(self, symbol: str, timeframe: str = '15m', 
                  limit: int = 100) -> List:
        """
        Get OHLCV (candlestick) data
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Timeframe (e.g., '1m', '5m', '15m', '1h')
            limit: Number of candles to fetch
        
        Returns:
            List of OHLCV data
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return []
            
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        
        except Exception as e:
            logger.error(f"Error fetching OHLCV from {self.exchange_name}: {e}")
            return []
    
    def get_ticker(self, symbol: str) -> Dict:
        """
        Get current ticker information
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
        
        Returns:
            Ticker data dictionary
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return {}
            
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        
        except Exception as e:
            logger.error(f"Error fetching ticker from {self.exchange_name}: {e}")
            return {}
    
    def get_balance(self) -> Dict:
        """
        Get account balance
        
        Returns:
            Balance dictionary with currencies
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return {}
            
            balance = self.exchange.fetch_balance()
            return balance
        
        except Exception as e:
            logger.error(f"Error fetching balance from {self.exchange_name}: {e}")
            return {}
    
    def create_limit_order(self, symbol: str, side: str, amount: float, 
                          price: float) -> Dict:
        """
        Create a limit order
        
        Args:
            symbol: Trading pair
            side: 'buy' or 'sell'
            amount: Order amount
            price: Order price
        
        Returns:
            Order data
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return {}
            
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            logger.info(f"Limit order created: {order}")
            return order
        
        except Exception as e:
            logger.error(f"Error creating limit order on {self.exchange_name}: {e}")
            return {}
    
    def create_market_order(self, symbol: str, side: str, amount: float) -> Dict:
        """
        Create a market order
        
        Args:
            symbol: Trading pair
            side: 'buy' or 'sell'
            amount: Order amount
        
        Returns:
            Order data
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return {}
            
            order = self.exchange.create_market_order(symbol, side, amount)
            logger.info(f"Market order created: {order}")
            return order
        
        except Exception as e:
            logger.error(f"Error creating market order on {self.exchange_name}: {e}")
            return {}
    
    def create_stop_loss_order(self, symbol: str, side: str, amount: float,
                              stop_price: float) -> Dict:
        """
        Create a stop loss order
        
        Args:
            symbol: Trading pair
            side: 'buy' or 'sell'
            amount: Order amount
            stop_price: Stop loss price
        
        Returns:
            Order data
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return {}
            
            # Note: Different exchanges have different stop loss implementations
            params = {
                'stopPrice': stop_price
            }
            
            order = self.exchange.create_order(symbol, 'limit', side, amount, None, params)
            logger.info(f"Stop loss order created: {order}")
            return order
        
        except Exception as e:
            logger.error(f"Error creating stop loss order on {self.exchange_name}: {e}")
            return {}
    
    def cancel_order(self, order_id: str, symbol: str = None) -> Dict:
        """
        Cancel an order
        
        Args:
            order_id: Order ID to cancel
            symbol: Trading pair (required for some exchanges)
        
        Returns:
            Cancelled order data
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return {}
            
            order = self.exchange.cancel_order(order_id, symbol)
            logger.info(f"Order cancelled: {order}")
            return order
        
        except Exception as e:
            logger.error(f"Error cancelling order on {self.exchange_name}: {e}")
            return {}
    
    def get_order(self, order_id: str, symbol: str = None) -> Dict:
        """
        Get order status
        
        Args:
            order_id: Order ID
            symbol: Trading pair
        
        Returns:
            Order data
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return {}
            
            order = self.exchange.fetch_order(order_id, symbol)
            return order
        
        except Exception as e:
            logger.error(f"Error fetching order from {self.exchange_name}: {e}")
            return {}
    
    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """
        Get list of open orders
        
        Args:
            symbol: Trading pair (optional, gets all if not specified)
        
        Returns:
            List of open orders
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return []
            
            orders = self.exchange.fetch_open_orders(symbol)
            return orders
        
        except Exception as e:
            logger.error(f"Error fetching open orders from {self.exchange_name}: {e}")
            return []
    
    def get_trades(self, symbol: str, limit: int = 50) -> List[Dict]:
        """
        Get recent trades
        
        Args:
            symbol: Trading pair
            limit: Number of trades to fetch
        
        Returns:
            List of trades
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return []
            
            trades = self.exchange.fetch_my_trades(symbol, limit=limit)
            return trades
        
        except Exception as e:
            logger.error(f"Error fetching trades from {self.exchange_name}: {e}")
            return []
    
    def get_supported_symbols(self) -> List[str]:
        """
        Get all supported trading pairs on exchange
        
        Returns:
            List of supported symbols
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return []
            
            symbols = self.exchange.symbols
            return symbols
        
        except Exception as e:
            logger.error(f"Error fetching supported symbols from {self.exchange_name}: {e}")
            return []
    
    def get_fee_info(self, symbol: str = None) -> Dict:
        """
        Get fee information
        
        Args:
            symbol: Trading pair (optional)
        
        Returns:
            Fee information
        """
        try:
            if not self.exchange:
                logger.error("Exchange not initialized")
                return {}
            
            fees = self.exchange.fetch_trading_fees(symbol)
            return fees
        
        except Exception as e:
            logger.error(f"Error fetching fees from {self.exchange_name}: {e}")
            return {}
