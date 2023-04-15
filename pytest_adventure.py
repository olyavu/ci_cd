import pyodbc
import pandas as pd
import pytest


def get_connection():
    connection = pyodbc.connect(
        'Driver={SQL Server};'
        'SERVER=EPAMYERW027B\SQLEXPRESS;'
        'DATABASE=AdventureWorks2012;')
    return connection


class TestDB:
    @classmethod
    def setup_class(cls):
        cls.conn = get_connection()


    @classmethod
    def teardown_class(cls):
        cls.conn.close()


@pytest.mark.count_rows_person_address
def test_count_rows_person_address():
    conn = get_connection()
    query = 'SELECT COUNT(*) as count FROM [Person].[Address]'
    df = pd.read_sql(query, conn)
    row_count = df['count'].iloc[0]
    expected_count = 19614
    assert row_count == expected_count, 'Rows count is wrong'


@pytest.mark.count_rows_person_address
def test_addressline_not_null():
    conn = get_connection()
    query = 'SELECT COUNT(*) as count FROM [Person].[Address] WHERE AddressLine1 IS NULL'
    df = pd.read_sql(query, conn)
    null_count = df['count'].iloc[0]
    assert null_count == 0, 'There are NULLs in AddressLine1'


@pytest.mark.test_unique_document_nodes
def test_unique_document_nodes():
    conn = get_connection()
    query_distinct_nodes = 'SELECT COUNT(DISTINCT DocumentNode) as count FROM [Production].[Document]'
    df_distinct_nodes = pd.read_sql_query(query_distinct_nodes, conn)
    distinct_node_count = df_distinct_nodes['count'].iloc[0]

    query_total_rows = 'SELECT COUNT(*) as count FROM [Production].[Document]'
    df_total_rows = pd.read_sql_query(query_total_rows, conn)
    total_row_count = df_total_rows['count'].iloc[0]
    assert distinct_node_count == total_row_count, 'Not unique values'


@pytest.mark.test_document_titles_not_null
def test_document_titles_not_null():
    conn = get_connection()
    query_null_titles = 'SELECT COUNT(*) as count FROM [Production].[Document] WHERE Title IS NULL'
    df_null_titles = pd.read_sql_query(query_null_titles, conn)
    null_title_count = df_null_titles['count'].iloc[0]
    assert null_title_count == 0, 'Nulls in Title column'


@pytest.mark.test_doc_unitmeasures_dups
def test_doc_unitmeasures_dups():
    conn = get_connection()
    query_duplicates = 'SELECT COUNT(*) as count FROM (SELECT [UnitMeasureCode], [Name], [ModifiedDate], COUNT(*) as cnt\
            FROM [Production].[UnitMeasure] GROUP BY [UnitMeasureCode], [Name], [ModifiedDate] HAVING COUNT(*) > 1\
        ) as duplicates'
    df_unitmesures_dups = pd.read_sql_query(query_duplicates, conn)
    duplicate_row_count = df_unitmesures_dups['count'].iloc[0]
    assert duplicate_row_count == 0, 'Duplicates in the [Production].[UnitMeasure]'


@pytest.mark.test_unit_measure_structure
def test_unit_measure_structure():
    conn = get_connection()
    query_columns = '''SELECT COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'Production' AND TABLE_NAME = 'UnitMeasure'
        ORDER BY ORDINAL_POSITION'''
    df_columns = pd.read_sql_query(query_columns, conn)
    actual_structure = df_columns.to_dict('records')
    expected_structure = [
        {'COLUMN_NAME': 'UnitMeasureCode', 'DATA_TYPE': 'nchar'},
        {'COLUMN_NAME': 'Name', 'DATA_TYPE': 'nvarchar'},
        {'COLUMN_NAME': 'ModifiedDate', 'DATA_TYPE': 'datetime'}
    ]
    assert actual_structure == expected_structure, 'Table structure is wrong'
