# Standard Python imports
from enum import Enum
from datetime import datetime, timedelta

# Third-party imports
import streamlit as st

# Local package imports
from Option_Pricing import BinomialTreeModel, Ticker
from Option_Pricing.AmericanBinomialTreeModel import AmericanBinomialTreeModel


class OPTION_PRICING_MODEL(Enum):
    BINOMIAL = 'Binomial Model'


@st.cache(allow_output_mutation=True)
def get_historical_data(ticker, start_date, end_date):
    """Get and cache historical data."""
    return Ticker.get_historical_data(ticker, start_date, end_date)


# Ignore the Streamlit warning for using st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

# Main title
st.title('Option pricing')

# User selected model from sidebar
pricing_method = st.sidebar.radio('Please select option pricing method', options=[
                                  model.value for model in OPTION_PRICING_MODEL])

# Displaying specified model
st.subheader(f'Pricing method: {pricing_method}')

if pricing_method == OPTION_PRICING_MODEL.BINOMIAL.value:
    # Parameters for Binomial-Tree model
    S = st.number_input('Stock Price (S)', min_value=0.01, value=100.0)
    K = st.number_input('Strike Price (K)', min_value=0.01, value=100.0)
    r = st.slider('Risk-Free Rate (r)', 0.0, 1.0, 0.05)
    v = st.slider('Volatility (v)', 0.01, 1.0, 0.3)
    T = st.number_input('Time to Expiry (T)', min_value=0.01, value=20.0)
    n = st.number_input('Number of Time Steps (n)', min_value=1, value=17)
    option_type = st.selectbox('Option Type', ['European', 'American'])

    if st.button('Calculate Option Prices'):
        if option_type == "European":
            BOPM = BinomialTreeModel(S, K, T, r, v, n, option_type)
            optionMatrix = BOPM.calculate_option_prices()
            putMatrix, callMatrix = BOPM.calculate_european_option_prices(
                optionMatrix)
        elif option_type == "American":
            BOPM = AmericanBinomialTreeModel(
                S, K, T, r, v, n, option_type)
            optionMatrix = BOPM.calculate_option_prices()
            putMatrix, callMatrix = BOPM.calculate_american_option_prices(
                optionMatrix)

        # Display the option prices as a matrix
        st.subheader('Option Prices Matrix:')
        st.write(optionMatrix)

        st.subheader('Option Put Prices Matrix:')
        st.write(putMatrix)

        st.subheader(
            f'Selon le modèle CRR, le prix du put est : {putMatrix[0][0]}')

        st.subheader('Option Call Prices Matrix:')
        st.write(callMatrix)

        st.subheader(
            f'Selon le modèle CRR, le prix du call est : {callMatrix[0][0]}')
