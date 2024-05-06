DECLARE target_table_name STRING;

-- Find the latest validated table name
SET target_table_name = (
  SELECT table_name
  FROM (
    SELECT *
    FROM (
      SELECT table_options.*
      FROM assignment_data.INFORMATION_SCHEMA.TABLE_OPTIONS AS table_options
      WHERE table_options.table_name IN (
        SELECT DISTINCT table_name
        FROM assignment_data.INFORMATION_SCHEMA.TABLE_OPTIONS
        WHERE option_value LIKE '%validated%weekly%'
      )
      ORDER BY 
        table_options.option_name = 'expiration_timestamp',
        table_options.option_value DESC
      LIMIT 1
    )
  )
);

EXECUTE IMMEDIATE FORMAT(
  "CREATE OR REPLACE TABLE `group_3_dataset.last_validated_ecom` AS SELECT * FROM `assignment_data.%s`",
  target_table_name
);
