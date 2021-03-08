from snowflake import connector

def sf_connect():
    con = connector.connect(
        user='SOLOZANO0725',
        password='Sol3475810.',
        account='jm95885.canada-central.azure',
        warehouse='COMPUTE_WH',
        database='DEMO_DB',
        schema='PUBLIC'
    )
    return con
