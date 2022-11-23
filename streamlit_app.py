# streamlit_app.py

import streamlit as st
import snowflake.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
    user = "ds300",
    account = "mgb-mgbprod.privatelink",
    warehouse = "edw_adhoc_all_wh",
    database = "edw_workspace",
    schema = "mee",
    role = "sfedw_ws_mee",
    authenticator = "externalbrowser"
)

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from fiscaldb_physician_crosswalk;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
