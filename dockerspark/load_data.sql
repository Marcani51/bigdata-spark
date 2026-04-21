-- SQL Initialization for DBeaver
-- This script registers your existing Parquet data as tables in the Spark Thrift Server.

-- 1. Register Transactions Data
CREATE TABLE IF NOT EXISTS transactions 
USING PARQUET 
LOCATION '/output/retail_parquet';

-- 2. Register Customer Segments (from K-Means results)
CREATE TABLE IF NOT EXISTS customer_segments 
USING PARQUET 
LOCATION '/output/customer_segments';

-- 3. Verify
SHOW TABLES;

-- Tip: Use 'DESCRIBE transactions' to see the schema.
