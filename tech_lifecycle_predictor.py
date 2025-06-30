import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 1. 数据准备（带2004-2024年真实数据）
data = {
    'Year': range(2004, 2024),
    'Endoscopic Examination': [3, 4, 13, 6, 6, 4, 5, 9, 11, 18, 22, 38, 41, 21, 44, 24, 21, 55, 38, 38, 50],
    'Serum Biomarker Detection': [1, 2, 5, 2, 1, 4, 4, 1, 4, 2, 8, 9, 7, 8, 10, 6, 5, 6, 9, 11, 12],
    'AI - Endoscopy Fusion': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 11, 16, 20, 21, 27],
    'Imaging Examination': [5, 7, 22, 9, 13, 13, 20, 16, 31, 35, 64, 92, 109, 69, 101, 87, 112, 147, 111, 120, 159],
    'Liquid Biopsy': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 4, 1, 4, 7, 3, 13, 19, 10, 16, 12],
    'Genomic Profiling': [2, 0, 2, 2, 3, 1, 2, 3, 3, 6, 10, 17, 22, 9, 20, 16, 6, 36, 28, 20, 32],
    'Immunohistochemistry': [1, 0, 0, 0, 1, 1, 2, 0, 0, 2, 2, 0, 7, 1, 1, 3, 3, 6, 2, 4, 4],
    'Microbiome Analysis': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 4, 0, 1, 3, 0, 4, 3],
    'Metabolic Profiling': [0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 3, 0, 2, 0, 3, 0, 4, 2, 5, 6, 9]
}
df = pd.DataFrame(data)
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# 2. 计算复合年均增长率(CAGR)
def calculate_cagr(start, end, years):
    return (end/start)**(1/years) - 1 if start > 0 else np.nan

phases = {
    'Phase1': (2004, 2013),
    'Phase2': (2014, 2019), 
    'Phase3': (2020, 2024)
}

# 3. Prophet预测函数(含验证逻辑)
def forecast_technology(tech_series, periods=5):
    model = Prophet(
        seasonality_mode='multiplicative',
        changepoint_prior_scale=0.1,
        yearly_seasonality=True
    )
    
    prophet_df = pd.DataFrame({
        'ds': tech_series.index,
        'y': tech_series.values
    })
    
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=periods, freq='Y')
    forecast = model.predict(future)
    return forecast

# 4. 安全获取预测值
def get_forecast_value(forecast, target_year):
    result = forecast[forecast['ds'].dt.year == target_year]
    if not result.empty:
        row = result.iloc[0]
        return {
            'predicted': round(row['yhat'], 1),
            'ci_lower': round(row['yhat_lower'], 1),
            'ci_upper': round(row['yhat_upper'], 1)
        }
    return {'predicted': np.nan, 'ci_lower': np.nan, 'ci_upper': np.nan}

# 5. 执行分析与可视化
plt.figure(figsize=(15, 10))
rcParams['font.family'] = 'sans-serif'  # 使用无衬线字体

forecast_results = []
technologies = ['Endoscopic Examination', 'Serum Biomarker Detection', 'AI - Endoscopy Fusion', 'Liquid Biopsy']

for i, tech in enumerate(technologies, 1):
    plt.subplot(2, 2, i)
    tech_series = df.set_index('Year')[tech]
    forecast = forecast_technology(tech_series)
    
    # 绘制实际值与预测值
    plt.plot(tech_series.index, tech_series, 'b-', label='Actual')
    plt.plot(forecast['ds'], forecast['yhat'], 'r--', label='Forecast')
    plt.fill_between(
        forecast['ds'],
        forecast['yhat_lower'],
        forecast['yhat_upper'],
        color='pink', alpha=0.3, label='95% CI'
    )
    
    plt.title(f'{tech} Technology Publication Trends')
    plt.xlabel('Year')
    plt.ylabel('Quantity')
    plt.legend()
    plt.grid(True)
    
    # 保存预测结果
    for year in range(2025, 2030):
        values = get_forecast_value(forecast, year)
        forecast_results.append({
            'technology': tech,
            'year': year,
            **values
        })

plt.tight_layout()
plt.savefig('lifecycle_forecast.png', dpi=300)
plt.show()

# 6. 输出结构化预测结果
forecast_table = pd.DataFrame(forecast_results)
pivot_table = forecast_table.pivot(
    index='year', 
    columns='technology', 
    values=['predicted', 'ci_lower', 'ci_upper']
).round(1)

print("Forecast Results Summary:")
print(pivot_table)

# 7. 按技术输出详细预测表格
for tech in forecast_table['technology'].unique():
    tech_data = forecast_table[forecast_table['technology'] == tech]
    print(f"\n{tech} Technology Detailed Forecast:")
    print(tech_data[['year', 'predicted', 'ci_lower', 'ci_upper']].to_markdown(index=False))
