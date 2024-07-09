import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout='wide')

data = pd.read_csv('tir_tib.csv')
base_mon = pd.read_csv('base_mon.csv')
m1 = pd.read_csv('m1.csv')
m2 = pd.read_csv('m2.csv')
m3 = pd.read_csv('m3.csv')
money = pd.read_csv('money.csv')
inf_empl = pd.read_csv('inf_empl.csv')
tir_inf = pd.read_csv('tir_inf.csv')

st.title("Estadísticas monetarias")

tab1, tab2, tab3 = st.tabs(['Tasas',
                            'Dinero',
                            'Inflación'])


data['Fecha'] = pd.to_datetime(data['Fecha'])
data = data.set_index('Fecha')
base_mon['fecha'] = pd.to_datetime(base_mon['fecha'])
base_mon = base_mon.set_index('fecha')
m1['fecha'] = pd.to_datetime(m1['fecha'])
m1 = m1.set_index('fecha')
m2['fecha'] = pd.to_datetime(m2['fecha'])
m2 = m2.set_index('fecha')
m3['fecha'] = pd.to_datetime(m3['fecha'])
m3 = m3.set_index('fecha')
money['fecha'] = pd.to_datetime(money['fecha'])
money = money.set_index('fecha')

tir_inf['fecha'] = pd.to_datetime(tir_inf['fecha'])
tir_inf = tir_inf.set_index('fecha')

inf_empl['fecha'] = pd.to_datetime(inf_empl['fecha'])


# Plotting the series with improved aesthetics

with tab1: 
    fig = go.Figure()

    # Add the main inflation line
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['TIB'],
                            mode='lines',
                            name='TIB',
                            line=dict(color='#1f77b4', width=2)))

    # Add the target inflation line
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['TIR'],
                            mode='lines',
                            name='TIR',
                            line=dict(color='#ff7f0e', width=2, dash='dash')))

    # Fill the range between lower_range and upper_range around series1
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['exp'],
                            mode='lines',
                            line=dict(width=0),
                            showlegend=False))
    fig.add_trace(go.Scatter(x=data.index,
                            y=data['cont'],
                            mode='lines',
                            line=dict(width=0),
                            fill='tonexty',
                            fillcolor='rgba(31, 119, 180, 0.2)',
                            showlegend=False))

    # Customize the layout to mimic The Economist style
    fig.update_layout(
        title=dict(text='Estabilidad macro', font=dict(size=16, color='#333333'), x=0.01, xanchor='left'),
        xaxis=dict(title='Fecha', title_font=dict(size=14, color='#333333'), tickformat='%Y-%m', tickfont=dict(size=12, color='#333333')),
        yaxis=dict(title='Tasas', title_font=dict(size=14, color='#333333'), tickfont=dict(size=12, color='#333333')),
        legend=dict(font=dict(size=12), borderwidth=0, x=1,  # Adjust this value to place the legend on the left side
        xanchor='right',  # Anchor the legend box to the left
        y=1,  # Position at the top
        yanchor='top'),
        margin=dict(l=40, r=20, t=40, b=40),  # Tight layout
    )

    st.plotly_chart(fig)

    fig = go.Figure()

    # Add the main inflation line
    fig.add_trace(go.Scatter(x=tir_inf.index,
                            y=tir_inf['TIR'],
                            mode='lines',
                            name='TIR',
                            line=dict(color='#30C5FF', width=2)))

    # Add the target inflation line
    fig.add_trace(go.Scatter(x=tir_inf.index,
                            y=tir_inf['Meta de inflación'],
                            mode='lines',
                            name='Meta de inflación',
                            line=dict(color='#2A2D34', width=2, dash='dash')))

    # Fill the range between lower_range and upper_range around series1
    fig.add_trace(go.Scatter(x=tir_inf.index,
                            y=tir_inf['Tasa de desempleo (%)'],
                            mode='lines',
                            name='Tasa de desempleo',
                            line=dict(color='#5C946E', width=2)))
    fig.add_trace(go.Scatter(x=tir_inf.index,
                            y=tir_inf['Inflación total'],
                            mode='lines',
                            name='Inflación total',
                            line=dict(color='#80C2AF', width=2, dash='dash')))

    # Customize the layout to mimic The Economist style
    fig.update_layout(
        title=dict(text='TIB vs. TIR ', font=dict(size=16, color='#333333'), x=0.01, xanchor='left'),
        xaxis=dict(title='Fecha', title_font=dict(size=14, color='#333333'), tickformat='%Y-%m', tickfont=dict(size=12, color='#333333')),
        yaxis=dict(title='Tasas', title_font=dict(size=14, color='#333333'), tickfont=dict(size=12, color='#333333')),
        legend=dict(
        font=dict(size=12),
        borderwidth=0,
        x=0.5,  # Center the legend horizontally
        xanchor='center',
        y=-0.2,  # Position below the plot
        yanchor='top',
        orientation='h'  # Horizontal legend
    ),
        margin=dict(l=40, r=20, t=40, b=40),  # Tight layout
    )

    st.plotly_chart(fig)

with tab2:


    economist_colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

    fig, axes = plt.subplots(4, 2, figsize=(14, 12), sharex=True)
    axes[0, 1].set_ylim(0, 1)
    axes[1, 1].set_ylim(0, 1)
    axes[2, 1].set_ylim(0, 1)
    axes[3, 1].set_ylim(0, 1)

        # Plot the data
    base_mon[['Efectivo', 'Reserva Bancaria']].plot(kind='area', stacked=True, ax=axes[0, 0], color=economist_colors[:2], alpha=0.6)
    axes[0, 0].set_title('Base Monetaria', loc='left', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Amount', fontsize=10)
    base_mon[['Efectivo', 'Reserva Bancaria']].div(base_mon['Total'], axis=0).plot(kind='area', stacked=True, ax=axes[0, 1], color=economist_colors[:2], alpha=0.6)
    axes[0, 1].set_title('Base Monetaria (Normalizada)', loc='left', fontsize=12, fontweight='bold')

    m1.plot(kind='area', stacked=True, ax=axes[1, 0], color=economist_colors[:2], alpha=0.6)
    axes[1, 0].set_title('M1', loc='left', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Amount', fontsize=10)
    m1.div(m1['Cuentas Corrientes'] + m1['Efectivo'], axis=0).plot(kind='area', stacked=True, ax=axes[1, 1], color=economist_colors[:2], alpha=0.6)
    axes[1, 1].set_title('M1 (Normalizada)', loc='left', fontsize=12, fontweight='bold')

    m2.plot(kind='area', stacked=True, ax=axes[2, 0], color=economist_colors[:2], alpha=0.6)
    axes[2, 0].set_title('M2', loc='left', fontsize=12, fontweight='bold')
    axes[2, 0].set_ylabel('Amount', fontsize=10)
    m2.div(m2['Cuasidineros'] + m2['m1'], axis=0).plot(kind='area', stacked=True, ax=axes[2, 1], color=economist_colors[:2], alpha=0.6)
    axes[2, 1].set_title('M2 (Normalizada)', loc='left', fontsize=12, fontweight='bold')

    m3.plot(kind='area', stacked=True, ax=axes[3, 0], color=economist_colors[:2], alpha=0.6)
    axes[3, 0].set_title('M3', loc='left', fontsize=12, fontweight='bold')
    axes[3, 0].set_ylabel('Amount', fontsize=10)
    m3.div(m3['Depósitos en poder del público'] + m3['Efectivo'], axis=0).plot(kind='area', stacked=True, ax=axes[3, 1], color=economist_colors[:2], alpha=0.6)
    axes[3, 1].set_title('M3 (Normalizada)', loc='left', fontsize=12, fontweight='bold')

        # Improve layout
    for ax in axes[:, 0]:
        ax.legend(frameon=False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

    for ax in axes[:, 1]:
        ax.legend().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

    fig.patch.set_visible(False)
    fig.tight_layout()

    st.pyplot(fig)

    

    economist_colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

        # Plotting
    fig, ax = plt.subplots(figsize=(14, 8))

    money.plot(kind='area', stacked=False, alpha=0.4, color=economist_colors, ax=ax)

        # Set title and labels with a specific font
    ax.set_title('Dinero en el tiempo', fontsize=16, fontweight='bold', loc='left', color='#333333')
    ax.set_xlabel('Fecha', fontsize=12, color='#333333')
    ax.set_ylabel('Valor', fontsize=12, color='#333333')

        # Customize the legend
    ax.legend(frameon=False, loc='upper left', fontsize=10)

        # Remove unnecessary spines and add grid lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

        # Customize tick parameters
    ax.tick_params(axis='x', colors='#333333')
    ax.tick_params(axis='y', colors='#333333')

        # Remove unnecessary borders
    fig.patch.set_visible(False)

    fig.tight_layout()

    st.pyplot(fig)

with tab3:

    inf_empl['Fecha'] = inf_empl['fecha'].dt.strftime("%Y-%m")
       # Sample data
    fig = px.scatter(inf_empl,
                    x='Tasa de desempleo (%)',
                    y='Inflación total',
                    title='Curva de Phillips',
                    hover_data="Fecha")

    # Customize the layout to mimic The Economist style
    fig.update_traces(marker=dict(color='#1f77b4',  # Economist blue
                                opacity=0.6,      # Adjust transparency
                                line=dict(width=0.5, color='white')))  # White edges for markers

    fig.update_layout(
        title=dict(text='Curva de Phillips', font=dict(size=16, color='#333333'), x=0.01, xanchor='left'),
        xaxis=dict(title='Tasa de desempleo (%)', title_font=dict(size=12, color='#333333'), tickfont=dict(color='#333333')),
        yaxis=dict(title='Inflación total', title_font=dict(size=12, color='#333333'), tickfont=dict(color='#333333')),
   )

    st.plotly_chart(fig)

    

    fig = go.Figure()

    # Add the main inflation line
    fig.add_trace(go.Scatter(x=inf_empl['fecha'],
                            y=inf_empl['Inflación total'],
                            mode='lines',
                            name='Inflación',
                            line=dict(color='#1f77b4', width=2)))

    # Add the target inflation line
    fig.add_trace(go.Scatter(x=inf_empl['fecha'],
                            y=inf_empl['Meta de inflación'],
                            mode='lines',
                            name='Meta de inflación',
                            line=dict(color='#ff7f0e', width=2, dash='dash')))

    # Fill the range between lower_range and upper_range around series1
    fig.add_trace(go.Scatter(x=inf_empl['fecha'],
                            y=inf_empl['Límite superior'],
                            mode='lines',
                            line=dict(width=0),
                            showlegend=False))
    fig.add_trace(go.Scatter(x=inf_empl['fecha'],
                            y=inf_empl['Límite inferior'],
                            mode='lines',
                            line=dict(width=0),
                            fill='tonexty',
                            fillcolor='rgba(31, 119, 180, 0.2)',
                            showlegend=False))

    # Customize the layout to mimic The Economist style
    fig.update_layout(
        title=dict(text='Inflación', font=dict(size=16, color='#333333'), x=0.01, xanchor='left'),
        xaxis=dict(title='Fecha', title_font=dict(size=14, color='#333333'), tickformat='%Y-%m', tickfont=dict(size=12, color='#333333')),
        yaxis=dict(title='Inflación', title_font=dict(size=14, color='#333333'), tickfont=dict(size=12, color='#333333')),
        legend=dict(font=dict(size=12), borderwidth=0, x=0,  # Adjust this value to place the legend on the left side
        xanchor='left',  # Anchor the legend box to the left
        y=1,  # Position at the top
        yanchor='top'),
        margin=dict(l=40, r=20, t=40, b=40),  # Tight layout
    )

    st.plotly_chart(fig)