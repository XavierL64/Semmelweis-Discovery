import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# display floats with 2 digits after decimal point
pd.options.display.float_format = '{:,.2f}'.format

# create locators for ticks on the time axis
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# read and explore data
df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
df_monthly = pd.read_csv('monthly_deaths.csv', parse_dates=['date'])

df_yearly.info()
df_yearly.describe()
df_yearly.head()
df_yearly.isna().values.any()
df_yearly.duplicated().values.any()

df_monthly.info()
df_monthly.describe()
df_monthly.head()
df_monthly.isna().values.any()
df_monthly.duplicated().values.any()

# Plot monthly births and deaths on chart with twin y-axes
plt.figure(figsize=(14,8), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
 
ax1 = plt.gca()
ax2 = ax1.twinx()
 
ax1.set_ylabel('Births', color='skyblue', fontsize=18)
ax2.set_ylabel('Deaths', color='crimson', fontsize=18)

 
ax1.grid(color='grey', linestyle='--')

ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
 
ax1.plot(df_monthly['date'], 
         df_monthly['births'], 
         color='skyblue', 
         linewidth=3)
 
ax2.plot(df_monthly['date'], 
         df_monthly['deaths'], 
         color='crimson', 
         linewidth=2, 
         linestyle='--')
 
plt.show()

# create a chart with proportion of yearly deaths by clinic
df_yearly['pct_deaths'] = df_yearly['deaths'] / df_yearly['births']

line = px.line(df_yearly, 
               x='year', 
               y='pct_deaths',
               color='clinic',
               title='Proportion of Yearly Deaths by Clinic')
 
line.show()

# create chart showing death rate and 6-month moving average before/after before handwashing was introduced (monthly data)
handwashing_start = pd.to_datetime('1847-06-01')
df_monthly['pct_deaths'] = df_monthly['deaths']/df_monthly['births']

plt.figure(figsize=(14,8), dpi=200)
plt.title('Percentage of Monthly Deaths over Time', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
 
plt.ylabel('Percentage of Deaths', fontsize=18)
 
ax = plt.gca()
ax.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
 
plt.grid(color='grey', linestyle='--')
 
moving_average_line, = plt.plot(rolling_average_df.index, 
                               rolling_average_df['pct_deaths'], 
                               color='crimson', 
                               linewidth=3, 
                               linestyle='--',
                               label='6m Moving Average')

before_handwashing_line, = plt.plot(before_handwashing.date, 
                                   before_handwashing['pct_deaths'],
                                   color='black', 
                                   linewidth=1, 
                                   linestyle='--', 
                                   label='Before Handwashing')

after_handwashing_line, = plt.plot(after_handwashing.date, 
                                   after_handwashing['pct_deaths'], 
                                   color='skyblue', 
                                   linewidth=1, 
                                   marker='o',
                                   label='After Handwashing')
 
plt.legend(handles=[moving_average_line, before_handwashing_line, after_handwashing_line],
           fontsize=18)
 
plt.show()


# create box plots showing how death rate changed before and after handwashing
df_monthly['washing_hands'] = np.where(df_monthly['date'] < handwashing_start, 'No', 'Yes')

box = px.box(df_monthly, 
             x='washing_hands', 
             y='pct_deaths',
             color='washing_hands',
             title='How Have the Stats Changed with Handwashing?')
 
box.update_layout(xaxis_title='Washing Hands?',
                  yaxis_title='Percentage of Monthly Deaths',)
 
box.show()

# create a Kernel Density Estimate (KDE) chart to visualise death rate change
plt.figure(dpi=200)
sns.kdeplot(before_washing['pct_deaths'], shade=True, clip=(0,1))
sns.kdeplot(after_washing['pct_deaths'], shade=True, clip=(0,1))
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.xlim(0, 0.40)
plt.show()
