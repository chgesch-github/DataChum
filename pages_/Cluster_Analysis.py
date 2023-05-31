# Import moduls from local directories
from modules.utils.load_and_save_data import (
    convert_dataframe_to_csv,
    convert_dataframe_to_xlsx,
    read_csv,
    read_xlsx,
)

# Import the required libraries
import pandas as pd
import streamlit as st

# from streamlit_profiler import Profiler


def main():
    st.subheader("Cluster Analysis")

    # Profile the app
    #    streamlit_profiler = Profiler()
    #    streamlit_profiler.start()

    # Create file uploader object
    uploaded_file = st.file_uploader("Upload your database", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Read the file to a dataframe using pandas
        if uploaded_file.name[-3:] == "csv":
            # Read in the csv file
            data = read_csv(uploaded_file)
        elif uploaded_file.name[-4:] == "xlsx":
            # Read in the csv file
            data = read_xlsx(uploaded_file)
        else:
            st.write("Type should be .CSV or .XLSX")

        # Drop ID columns (or similar): Analyze whether all values of the column are unique
        # (count of unique values equals column's length)
        cols_all = data.columns.to_list()
        list_of_dropped_columns = []
        for column in cols_all:
            if len(data[column]) == len(data[column].unique()):
                data = data.drop(column, axis=1)
                list_of_dropped_columns.append(column)
        if len(list_of_dropped_columns) > 0:
            #            st.markdown(f"""**{str(string_to_be_displayed)}**""")
            st.markdown(
                ":red[**Following columns have been removed as all values of the column are unique:**] "
                + ", ".join(list_of_dropped_columns)
            )
        # Get column names (also NUMERICAL and CATEGORICAL)
        cols_num = data.select_dtypes(include=["float", "int"]).columns.to_list()
        cols_cat = data.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.to_list()
        # Create three columns
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.markdown(
                "Please check if the data types of the features were infered correctly (Integers will be handled as numerical variables)"  # noqa: E501
            )
        with col_2:
            cols_cat_df = pd.DataFrame({"Categorical Features": cols_cat})
            st.dataframe(cols_cat_df, use_container_width=True)
        with col_3:
            cols_num_df = pd.DataFrame({"Numerical Features": cols_num})
            st.dataframe(cols_num_df, use_container_width=True)
        st.subheader("**Cluster Modeling Setup**")
        # Create three tabs
        tab_s1, tab_s2, tab_s3 = st.tabs(
            [
                "**Procedure**",
                "**Preprocessing**",
                "**Models**",
            ]
        )
        # Tab 1: Procedure


if __name__ == "__main__":
    # Page setup
    st.set_page_config(
        page_title="DataChum", page_icon="assets/logo_01.png", layout="wide"
    )
    main()
