import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3
from sqlite3 import Connection
# if 'x' not in st.session_state:
	# st.session_state.x =0

# increment = st.button("increment")
# if increment:
	# st.session_state.x += 1
# st.write('count' , st.session_state.x)



URI_SQLITE_DB = "test.db"


def main():
    st.title("Tell me a secret.")
    st.markdown("Go on, I won't tell anybody :) ")
    
    conn = get_connection(URI_SQLITE_DB)
    init_db(conn)
    build_input(conn)
    # build_sidebar(conn)
    display_data(conn)
    run_calculator(conn)


def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS test
            (
                INPUT BLOB
            );"""
    )
    conn.commit()


def build_input(conn: Connection):
	input = st.text_input('Whisper into the fountain of secrets.')
	if st.button("Save to database"):
		conn.execute(f"INSERT INTO test (INPUT) VALUES ({input}")
		conn.commit()

#def build_sidebar(conn: Connection):
#    st.sidebar.header("Configuration")
 #   input1 = st.sidebar.slider("Input 1", 0, 100)
  #  input2 = st.sidebar.slider("Input 2", 0, 100)
   # if st.sidebar.button("Save to database"):
    #    conn.execute(f"INSERT INTO test (INPUT1, INPUT2) VALUES ({input1}, {input2})")
     #   conn.commit()


def display_data(conn: Connection):
    if st.checkbox("Display data in sqlite databse"):
        st.dataframe(get_data(conn))


def run_calculator(conn: Connection):
    if st.button("Run calculator"):
        st.info("Run your function")
        df = get_data(conn)
        st.write(df.sum())


def get_data(conn: Connection):
    df = pd.read_sql("SELECT * FROM test", con=conn)
    return df


@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)


if __name__ == "__main__":
    main()
