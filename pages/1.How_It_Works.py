import streamlit as st

st.title("How it Works")

st.write('Step 1 : Direct to the NavBar, from the left side')
st.write('Step 2 : Enter Stock Symbol (as mentioned in google finance website)')
st.write('Step 3 : Select Stock Exchange')
st.write('Step 4 : Hit "Get Data"')
st.write('or')
st.write('Step 1 : Locate to Fetch Historical Data')
st.write('Step 2 : Enter Stock Symbol (as mentioned in yahoo finance website), Exchange and interval')
st.write('Step 3 : Select Start date and End date')
st.write('Note   : for 1 min interval set max period for 2-3 weeks otherwise the api will not generate such huge data')
st.write('Step 4 : Hit "Get Historical Data"')
st.write('Step 5 : Download the data as it generates')
st.write('Step 4 : Go to the "AI analysis" page')
st.write('Step 4 : Upload the downloaded CSV file')
st.write('Step 4 : Ask AI about the historical data') 
st.write("Example: 'Analyse the data', 'show trends','Backtesting strategy' etc")
st.write('or')
st.write('Step 1 : Go to the "3.Live_price_watching_agent" page')
st.write('Step 2 : Enter Stock Symbol')
st.write('Step 3 : Select Stock Exchange')
st.write('step 4 : click Fetch button and the agent will fetch the current price and refresh in every 30 seconds')



st.write('Enjoy!')



        