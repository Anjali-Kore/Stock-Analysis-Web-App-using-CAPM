import streamlit as st
import pandas as pd
import yfinance as yf
import capm_func




st.set_page_config(page_title="CAPM",
                    page_icon="chart_with_upwards_trends",
                    layout="wide"
                  )

st.title("Capital Asset Pricing Model")

col1,col2=st.columns([1,1])
with col1:
  stocks_list=st.multiselect("Choose 4 stocks",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
with col2:
  year=st.number_input("Number of years",1,10)

import datetime
end = datetime.datetime.today()
start = datetime.datetime(end.year - year, end.month, end.day)

import pandas_datareader.data as web
SP500=web.DataReader(['sp500'],'fred',start,end)
print(SP500.head())

stocks_df=pd.DataFrame()

for stock in stocks_list:
  data=yf.download(stock,period=f'{year}y')
  stocks_df[f'{stock}']=data['Close']

stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)

SP500.columns=['Date','sp500']
stocks_df=pd.merge(stocks_df,SP500,on='Date',how='inner')

col1,col2=st.columns([1,1])
with col1:
  st.markdown('### Dataframe head')
  st.dataframe(stocks_df.head(),use_container_width=True)
with col2:
  st.markdown('### Dataframe tail')
  st.dataframe(stocks_df.tail(),use_container_width=True)


col1,col2=st.columns([1,1])
with col1:
  st.markdown('### Price of all the Stocks')
  st.plotly_chart(capm_func.interactive_plot(stocks_df))
with col2:
  st.markdown('### Price of all the Stocks after normalization')
  st.plotly_chart(capm_func.interactive_plot(capm_func.normalize(stocks_df)))

beta={}
alpha={}

stocks_daily_return=capm_func.daily_return(stocks_df)
for i in stocks_daily_return.columns:
  if i !='Date' and i !='sp500':
    b,a=capm_func.calculate_beta(stocks_daily_return,i)
    beta[i]=b
    alpha[i]=a
print(beta,alpha)

beta_df=pd.DataFrame(columns=['Stock','Beta Value'])
beta_df['Stock']=beta.keys()
beta_df['Beta Value'] = [round(value, 2) for value in beta.values()]


with col1:
  st.markdown('### Calculated Beta Value')
  st.dataframe(beta_df,use_container_width=True)

rf=0
rm=stocks_daily_return['sp500'].mean()*252

return_df=pd.DataFrame()
return_value=[]
for stock,value in beta.items():
  return_value.append(str(round(rf+(value*(rm-rf)),2)))

return_df['Stock']=stocks_list
return_df["Return Value"]=return_value

with col2:
  st.markdown("### Calculated return using CAPM")
  st.dataframe(return_df,use_container_width=True)
