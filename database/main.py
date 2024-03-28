import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd 

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA



def main():
    # Read data from JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Extracting data and loading into Dataframe
    df = pd.json_normalize(data['rows'], meta=['Fecha', 'saldo_clientes'])
    df.drop(columns=["Saldo_Inversion", "num_ingresos_hoy", "num_egresos_hoy", 
                     "Saldo_Flujos", "dia_semana", "dia_del_mes", "mes", "año"])

    # Setting date as table index
    df.index = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
    del df['Fecha']

    # Add exogenous variables representing monthly and yearly seasonality
    df['mes'] = df.index.month
    df['año'] = df.index.year

    # Setting thershold date for training and testing datasets for predictive models
    train = df[df.index < pd.to_datetime("2023-11-01", format='%Y-%m-%d')]
    test = df[df.index > pd.to_datetime("2023-11-01", format='%Y-%m-%d')]
    y = train['saldo_clientes']

    # Creating and Training predictive model
    SARIMAXmodel = SARIMAX(y, exog=train[['mes', 'año']], order = (5, 1, 5), seasonal_order=(1,1,1,30))
    SARIMAXmodel = SARIMAXmodel.fit()

    # Generating predicitons to compare with testing dataset
    y_pred = SARIMAXmodel.get_forecast(steps=len(test), exog=test[['mes', 'año']])
    y_pred_df = y_pred.conf_int(alpha = 0.05) 
    y_pred_df["Predictions"] = SARIMAXmodel.predict(start = y_pred_df.index[0], 
                                                    end = y_pred_df.index[-1],  # end = y_pred_df.index[-1],
                                                    exog=test[['mes', 'año']])
    y_pred_df.index = test.index
    y_pred_out = y_pred_df["Predictions"] 

    # Evaluating model 
    arma_rmse = np.sqrt(mean_squared_error(test["saldo_clientes"].values, y_pred_df["Predictions"]))
    print("RMSE: ",arma_rmse)


    # Forecast one more year of data beyond the testing set
    forecast_steps = 365
    forecast_index = pd.date_range(start=y_pred_df.index[0] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
    forecast_exog = pd.DataFrame({'month': forecast_index.month, 'year': forecast_index.year}, index=forecast_index)
    forecast = SARIMAXmodel.forecast(steps=forecast_steps, exog=forecast_exog)


    # Setting plot style for testing
    sns.set_theme(style="whitegrid", palette="pastel")
    plt.plot(train.index, train["saldo_clientes"], color = "black", label = "Training Dataset")
    plt.plot(test.index, test["saldo_clientes"], color = "red", label = "Testing Dataset")
    # plt.plot(y_pred_out, color='green', label = 'Predictions')
    plt.plot(y_pred_out, color='green', label = 'SARIMA Predictions')
    plt.plot(forecast_index, forecast, label='Forecast', color='blue')
    plt.legend()
    # plt.plot(df.index, df['saldo_clientes'], )
    plt.ylabel('Saldo de Clientes')
    plt.xlabel('Fecha')
    plt.xticks(rotation=45)
    plt.title("Train/Test split for Saldo de Clientes Data")
    plt.savefig('saldo_clientes.png')
    plt.show()

    return

if __name__ == "__main__":
    main()
