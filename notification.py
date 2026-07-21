"""
Notification Module
Handles alerts via Telegram, Discord, Email, etc.
"""
import logging
import requests
from typing import Dict, List
from datetime import datetime
from config import config

logger = logging.getLogger(__name__)

class NotificationManager:
    """
    Manages trading alerts and notifications
    """
    
    def __init__(self):
        """Initialize notification manager"""
        self.telegram_token = config.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = config.TELEGRAM_CHAT_ID
        self.telegram_api_url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
    
    def send_telegram_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        """
        Send notification via Telegram
        
        Args:
            message: Message text (supports HTML formatting)
            parse_mode: 'HTML' or 'Markdown'
        
        Returns:
            True if successful
        """
        try:
            if not config.ENABLE_TELEGRAM or not self.telegram_token or not self.telegram_chat_id:
                logger.warning("Telegram not configured")
                return False
            
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(self.telegram_api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("Telegram message sent successfully")
                return True
            else:
                logger.error(f"Telegram error: {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def send_buy_signal(self, signal: Dict) -> bool:
        """
        Send BUY signal alert
        """
        try:
            message = f"""<b>🟢 BUY SIGNAL</b>
<b>Symbol:</b> {signal.get('symbol', 'N/A')}
<b>Price:</b> ${signal.get('current_price', 0):.8f}
<b>Strength:</b> {signal.get('signal_strength', 'N/A')}
<b>Confidence:</b> {signal.get('confidence', 0)}%

<b>📊 Indicators:</b>
RSI: {signal.get('rsi', 0):.2f}
MACD: {signal.get('macd', 0):.8f}
ATR: {signal.get('atr', 0):.8f}

<b>💰 Entry Levels:</b>
Entry: ${signal.get('entry_price', 0):.8f}
TP1: ${signal.get('suggested_tp1', 0):.8f}
TP2: ${signal.get('suggested_tp2', 0):.8f}
SL: ${signal.get('suggested_sl', 0):.8f}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            return self.send_telegram_message(message)
        
        except Exception as e:
            logger.error(f"Error sending buy signal: {e}")
            return False
    
    def send_sell_signal(self, signal: Dict) -> bool:
        """
        Send SELL signal alert
        """
        try:
            message = f"""<b>🔴 SELL SIGNAL</b>
<b>Symbol:</b> {signal.get('symbol', 'N/A')}
<b>Price:</b> ${signal.get('current_price', 0):.8f}
<b>Strength:</b> {signal.get('signal_strength', 'N/A')}
<b>Confidence:</b> {signal.get('confidence', 0)}%

<b>📊 Indicators:</b>
RSI: {signal.get('rsi', 0):.2f}
MACD: {signal.get('macd', 0):.8f}
ATR: {signal.get('atr', 0):.8f}

<b>💰 Entry Levels:</b>
Entry: ${signal.get('entry_price', 0):.8f}
TP1: ${signal.get('suggested_tp1', 0):.8f}
TP2: ${signal.get('suggested_tp2', 0):.8f}
SL: ${signal.get('suggested_sl', 0):.8f}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            return self.send_telegram_message(message)
        
        except Exception as e:
            logger.error(f"Error sending sell signal: {e}")
            return False
    
    def send_tp_notification(self, symbol: str, tp_level: str, 
                            price: float, profit_percent: float) -> bool:
        """
        Send Take Profit notification
        """
        try:
            message = f"""<b>📈 TAKE PROFIT ALERT</b>
<b>Symbol:</b> {symbol}
<b>Level:</b> {tp_level}
<b>Price:</b> ${price:.8f}
<b>Profit:</b> {profit_percent:+.2f}%

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            return self.send_telegram_message(message)
        
        except Exception as e:
            logger.error(f"Error sending TP notification: {e}")
            return False
    
    def send_sl_notification(self, symbol: str, price: float, loss_percent: float) -> bool:
        """
        Send Stop Loss notification
        """
        try:
            message = f"""<b>⛔ STOP LOSS HIT</b>
<b>Symbol:</b> {symbol}
<b>Price:</b> ${price:.8f}
<b>Loss:</b> {loss_percent:.2f}%

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            return self.send_telegram_message(message)
        
        except Exception as e:
            logger.error(f"Error sending SL notification: {e}")
            return False
    
    def send_order_box_alert(self, box_type: str, level: float, symbol: str) -> bool:
        """
        Send Order Box/Breaker Block alert
        """
        try:
            emoji = "📦" if box_type == "ORDER_BOX" else "🔌"
            message = f"""<b>{emoji} {box_type} DETECTED</b>
<b>Symbol:</b> {symbol}
<b>Level:</b> ${level:.8f}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            return self.send_telegram_message(message)
        
        except Exception as e:
            logger.error(f"Error sending order box alert: {e}")
            return False
    
    def send_error_alert(self, error_message: str) -> bool:
        """
        Send error notification
        """
        try:
            message = f"""<b>❌ ERROR ALERT</b>
{error_message}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            return self.send_telegram_message(message)
        
        except Exception as e:
            logger.error(f"Error sending error alert: {e}")
            return False
