"""
Chart Generation Module
Creates visualizations with technical indicators
"""
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ChartGenerator:
    """
    Generates trading charts with indicators and signals
    """
    
    @staticmethod
    def create_candlestick_chart(data: pd.DataFrame, symbol: str = '',
                                 save_path: str = None) -> str:
        """
        Create candlestick chart with volume
        
        Args:
            data: OHLCV dataframe with indicators
            symbol: Trading pair symbol
            save_path: Path to save chart
        
        Returns:
            Path to saved chart or HTML string
        """
        try:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                              vertical_spacing=0.03,
                              row_heights=[0.7, 0.3])
            
            # Candlestick
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    name='Price'
                ),
                row=1, col=1
            )
            
            # SMA 20
            if 'SMA_20' in data.columns:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data['SMA_20'],
                             line=dict(color='orange', width=1),
                             name='SMA 20'),
                    row=1, col=1
                )
            
            # SMA 50
            if 'SMA_50' in data.columns:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data['SMA_50'],
                             line=dict(color='blue', width=1),
                             name='SMA 50'),
                    row=1, col=1
                )
            
            # Bollinger Bands
            if 'BB_HIGH' in data.columns:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data['BB_HIGH'],
                             line=dict(width=0),
                             showlegend=False),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=data.index, y=data['BB_LOW'],
                             line=dict(width=0),
                             fillcolor='rgba(0,100,80,0.2)',
                             fill='tonexty',
                             name='Bollinger Bands'),
                    row=1, col=1
                )
            
            # Volume
            colors = ['red' if data['close'].iloc[i] < data['open'].iloc[i] else 'green'
                     for i in range(len(data))]
            fig.add_trace(
                go.Bar(x=data.index, y=data['volume'],
                      marker_color=colors, name='Volume'),
                row=2, col=1
            )
            
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Price", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            
            title = f"{symbol} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            fig.update_layout(title_text=title, height=600, hovermode='x unified')
            
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Chart saved to {save_path}")
                return save_path
            else:
                return fig.to_html()
        
        except Exception as e:
            logger.error(f"Error creating candlestick chart: {e}")
            return ""
    
    @staticmethod
    def create_indicator_chart(data: pd.DataFrame, symbol: str = '',
                              save_path: str = None) -> str:
        """
        Create indicator analysis chart (RSI, MACD, etc.)
        """
        try:
            fig = make_subplots(
                rows=4, cols=1, shared_xaxes=True,
                vertical_spacing=0.05,
                row_heights=[0.3, 0.23, 0.23, 0.24],
                subplot_titles=("Price", "RSI", "MACD", "Volume")
            )
            
            # Price
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    name='Price'
                ),
                row=1, col=1
            )
            
            # RSI
            if 'RSI' in data.columns:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data['RSI'],
                             line=dict(color='purple', width=1),
                             name='RSI'),
                    row=2, col=1
                )
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            
            # MACD
            if 'MACD' in data.columns:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data['MACD'],
                             line=dict(color='blue', width=1),
                             name='MACD'),
                    row=3, col=1
                )
                fig.add_trace(
                    go.Scatter(x=data.index, y=data['MACD_SIGNAL'],
                             line=dict(color='red', width=1),
                             name='Signal'),
                    row=3, col=1
                )
                fig.add_trace(
                    go.Bar(x=data.index, y=data['MACD_HIST'],
                          name='Histogram'),
                    row=3, col=1
                )
            
            # Volume
            colors = ['red' if data['close'].iloc[i] < data['open'].iloc[i] else 'green'
                     for i in range(len(data))]
            fig.add_trace(
                go.Bar(x=data.index, y=data['volume'],
                      marker_color=colors, name='Volume', showlegend=False),
                row=4, col=1
            )
            
            title = f"{symbol} - Technical Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            fig.update_layout(title_text=title, height=900, hovermode='x unified')
            
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Indicator chart saved to {save_path}")
                return save_path
            else:
                return fig.to_html()
        
        except Exception as e:
            logger.error(f"Error creating indicator chart: {e}")
            return ""
    
    @staticmethod
    def create_order_box_chart(data: pd.DataFrame, order_boxes: list,
                              symbol: str = '', save_path: str = None) -> str:
        """
        Create chart highlighting order boxes and breaker blocks
        """
        try:
            fig = go.Figure()
            
            # Candlestick
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    name='Price'
                )
            )
            
            # Order Boxes
            for box in order_boxes[-10:]:  # Last 10 boxes
                color = 'rgba(0, 255, 0, 0.1)' if box['type'] == 'BULLISH' else 'rgba(255, 0, 0, 0.1)'
                fig.add_shape(
                    type="rect",
                    x0=box['date'],
                    y0=box['top'],
                    x1=data.index[-1],
                    y1=box['bottom'],
                    fillcolor=color,
                    line=dict(color="gray", width=1)
                )
                
                # Mid level line
                fig.add_hline(
                    y=box['mid_level'],
                    line_dash="dot",
                    line_color="gray",
                    annotation_text=f"Box Mid: {box['mid_level']:.8f}"
                )
            
            title = f"{symbol} - Order Boxes & Market Structure - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            fig.update_layout(title_text=title, height=600, hovermode='x unified')
            
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Order box chart saved to {save_path}")
                return save_path
            else:
                return fig.to_html()
        
        except Exception as e:
            logger.error(f"Error creating order box chart: {e}")
            return ""
