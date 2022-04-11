import streamlit as st
import pandas as pd
import numpy as np
if 'x' not in st.session_state:
	st.session_state.x =0

increment = st.button("increment")
if increment:
	st.session_state.x += 1
st.write('count' , st.session_state.x)