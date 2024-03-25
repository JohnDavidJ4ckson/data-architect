The given data set has a json structure, the schema should be extracted and transformed to a Table that can be queried as requested by the team needs. As an example, here is the syntax for the corresponding service in AWS (https://aws.amazon.com/blogs/big-data/analyze-and-visualize-nested-json-data-with-amazon-athena-and-amazon-quicksight/)

CREATE EXTERNAL TABLE financials ( 
    table string,
    rows ARRAY<
        struct<Fecha: date,
             Saldo_Inversion: decimal(13, 2),
             saldo_clientes: decimal(13, 2),
             num_ingresos_hoy: bigint,
             num_egresos_hoy: bigint,
             Saldo_Flujos: decimal(13, 2),
             dia_semana: integer,
             dia_del_mes: integer,
             mes: integer,
             año: bigint>>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://data-architect/database/data.jso'

Now from the table financials queries can be written to extract the desired values:

1. select avg(saldo_clientes) from financials
2. select sum(Saldo_Flujos) from financials
3. select sum(num_ingresos_hoy) as Saldos_Entrantes, sum(num_egresos_hoy) as Saldos_Salientes from financials
4.  a) select sum(Saldo_Inversion) from financials group by año
    b) select sum(Saldo_Inversion) from financials group by mes
    c) select sum(Saldo_Inversion) from financials group by dia_del_mes
    d) select sum(Saldo_Inversion) from financials group by dia_semana

Note that a time filter has to be applied in the aforementioned queries with a filtering where statement similar to this:

where    Fecha >= '?'  -- always use unambiguous ISO format for User_Lowerbound_input
and    Fecha <= '?';  -- same for User_Higherbound_input

5.
To implement a predictive model one first has to create such a model by deciding the specific model (NNL, XGBOOST, etc) and topology (number of neuron layers, size of a tree/forest, etc). After such a model exists different sql environments offer different ways to load and use such a model. A simple example of the syntax would be as follows:

  -- Load the trained machine learning model into SQL environment
  LOAD MODEL 'path/to/trained_model';

  -- Define a user-defined function (UDF) to apply the model for prediction
  CREATE FUNCTION predict_using_model(feature1, feature2, ...) RETURNS prediction_type
  
  -- Use the UDF to add predictions as a column in a table query
  SELECT *, predict_using_model(feature1, feature2, ...) AS prediction_column
  FROM your_table;

These are all the details concerning the database requested by the exercises.
