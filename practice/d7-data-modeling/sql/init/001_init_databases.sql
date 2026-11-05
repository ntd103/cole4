-- Initialize databases for different modeling techniques
CREATE DATABASE IF NOT EXISTS data_vault_1;
CREATE DATABASE IF NOT EXISTS data_vault_2;
CREATE DATABASE IF NOT EXISTS scd_demo;
CREATE DATABASE IF NOT EXISTS big_fact;
CREATE DATABASE IF NOT EXISTS star_schema;
CREATE DATABASE IF NOT EXISTS snowflake_schema;

-- Set up users and permissions
CREATE USER IF NOT EXISTS 'demo_user' IDENTIFIED BY 'demo_pass';
GRANT ALL ON data_vault_1.* TO demo_user;
GRANT ALL ON data_vault_2.* TO demo_user;
GRANT ALL ON scd_demo.* TO demo_user;
GRANT ALL ON big_fact.* TO demo_user;
GRANT ALL ON star_schema.* TO demo_user;
GRANT ALL ON snowflake_schema.* TO demo_user;
