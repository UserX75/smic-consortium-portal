import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# SMIC Brand Colors
SMIC_BLUE = '#0a2540'
SMIC_GOLD = '#d4af37'
SMIC_LIGHT_BLUE = '#2a4b7c'
SMIC_DARK_BLUE = '#051a2c'

def create_pie_chart(df, names_col, values_col, title):
    fig = px.pie(df, names=names_col, values=values_col, title=title, hole=0.4,
                 color_discrete_sequence=[SMIC_BLUE, SMIC_LIGHT_BLUE, SMIC_GOLD, '#6c8fb3', '#4a6d8c'])
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='white', width=2)))
    fig.update_layout(title_font_color=SMIC_BLUE, title_font_size=18)
    return fig

def create_bar_chart(df, x_col, y_col, title, color=None):
    if color:
        fig = px.bar(df, x=x_col, y=y_col, title=title, color=color,
                     color_discrete_sequence=[SMIC_GOLD, SMIC_BLUE, SMIC_LIGHT_BLUE])
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=title,
                     color_discrete_sequence=[SMIC_GOLD])
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside',
                      marker=dict(color=SMIC_GOLD, line=dict(color=SMIC_BLUE, width=1)))
    fig.update_layout(title_font_color=SMIC_BLUE, xaxis_title_font_color=SMIC_BLUE,
                      yaxis_title_font_color=SMIC_BLUE)
    return fig

def create_line_chart(df, x_col, y_col, title):
    fig = px.line(df, x=x_col, y=y_col, title=title, markers=True,
                  color_discrete_sequence=[SMIC_GOLD])
    fig.update_traces(line=dict(width=3, color=SMIC_GOLD), 
                      marker=dict(size=8, color=SMIC_BLUE, symbol='circle'))
    fig.update_layout(title_font_color=SMIC_BLUE)
    return fig

def create_gauge(value, title, min_val=0, max_val=100, threshold=70):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'color': SMIC_BLUE}},
        delta={'reference': threshold},
        gauge={'axis': {'range': [min_val, max_val], 'tickcolor': SMIC_BLUE},
               'bar': {'color': SMIC_GOLD},
               'steps': [
                   {'range': [min_val, threshold], 'color': "#e6e6e6"},
                   {'range': [threshold, max_val], 'color': "#cce5ff"}],
               'threshold': {'line': {'color': SMIC_BLUE, 'width': 4}, 
                            'thickness': 0.75, 'value': threshold}}))
    fig.update_layout(height=300)
    return fig

def create_treemap(df, path, values, color, title):
    fig = px.treemap(df, path=path, values=values, color=color, 
                     title=title, color_continuous_scale=['#cce5ff', SMIC_BLUE])
    fig.update_layout(height=450, title_font_color=SMIC_BLUE)
    return fig

def create_correlation_heatmap(returns_df, title):
    corr = returns_df.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", 
                    color_continuous_scale=['#cce5ff', SMIC_GOLD, SMIC_BLUE], 
                    title=title)
    fig.update_layout(height=500, title_font_color=SMIC_BLUE)
    return fig

def create_waterfall_chart(values, labels, title, ylabel="Value (MM)"):
    fig = go.Figure(go.Waterfall(
        name="Contribution",
        orientation="v",
        measure=["relative"] * len(values),
        x=labels,
        y=values,
        text=[f"{v:+.1f}" for v in values],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker":{"color": SMIC_GOLD}},
        decreasing={"marker":{"color": SMIC_LIGHT_BLUE}}
    ))
    fig.update_layout(title=title, yaxis_title=ylabel, height=450, title_font_color=SMIC_BLUE)
    return fig