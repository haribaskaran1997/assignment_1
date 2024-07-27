import streamlit as st
import mysql.connector
import pandas as pd

# MySQL connection parameters
db_sql = {
    'host': 'localhost',
    'database': 'buses',
    'user': 'root',
    'password': 'Dextral@11'
}

# Function to execute SQL queries
def search_buses(operator, bus_type, From_Location, To_Location, duration):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_sql)
        if connection.is_connected():
            cursor = connection.cursor()

            # SQL query
            query = """
            SELECT Operator, Type, Departure, Duration, Arrival, Date, FromLocation, ToLocation, Rating, Price, SeatsAvailable
            FROM buses_data
            WHERE Operator LIKE %s AND Type LIKE %s AND FromLocation LIKE %s AND ToLocation LIKE %s AND duration LIKE %s
            """
            # Execute query with input values
            cursor.execute(query, ('%' + operator + '%', '%' + bus_type + '%', '%' + From_Location + '%', '%' + To_Location + '%', '%' + duration + '%'))
            results = cursor.fetchall()

            # Convert results to DataFrame
            df = pd.DataFrame(results, columns=[i[0] for i in cursor.description])

            # Close cursor and connection
            cursor.close()
            connection.close()

            return df

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")

def main():
    st.markdown("""
    <style>
     /* Custom CSS for text inputs */
    .stTextInput > div > div > input {
        border: 2px solid #e60012;
        border-radius: 5px;
    }
    """, unsafe_allow_html=True)

    st.title("Redbus")

    col1, col2 = st.columns([1, 1])
    col3, col4, col5= st.columns([1,1,1])
    # Input fields for searching
    with col1:
        operator = st.text_input("Enter Operator Name:")
    with col2:
        bus_type = st.text_input("Enter Bus Type:")
    with col3:
        From_Location = st.text_input("Enter From location:")
    with col4:
        To_Location = st.text_input("Enter To Location:")
    with col5:
        duration = st.text_input("Enter Duration")

    if st.button("Search"):
        if operator or bus_type or From_Location or To_Location  or duration:
            results = search_buses(operator, bus_type, From_Location, To_Location, duration)
            if results is not None and not results.empty:
                st.dataframe(results)
            else:
                st.warning("No results found.")
        else:
            st.warning("Please enter both Operator and Bus Type.")

if __name__ == '__main__':
    main()