import pandas as pd
import numpy as np
import yfinance as yf
import scipy.optimize as sco

from numpy.linalg import multi_dot
from scipy.stats import norm
from tabulate import tabulate

def markowitz(df_symbols: pd.DataFrame, st):
    def portfolio_stats(weights, returns):
        weights = np.array(weights)[:, np.newaxis]
        port_rets = weights.T @ np.array(returns.mean() * 252)[:, np.newaxis]
        port_vols = np.sqrt(multi_dot([weights.T, returns.cov() * 252, weights]))

        return np.array([port_rets, port_vols, port_rets/port_vols]).flatten()


    def min_sharpe_ratio(weights, returns):
        return -portfolio_stats(weights, returns)[2]


    def min_variance(weights, returns):
        return portfolio_stats(weights, returns)[1]**2


    def min_volatility(weights, returns):
        return portfolio_stats(weights, returns)[1]


    def wallet_reposition(reposition, array_weights, dict_data, opt_sharpe, returns):
        data = array_weights

        if reposition == "retorno":
            index_port = 0
        if reposition == "volatilidade":
            index_port = 1
        if reposition == "sharpe":
            index_port = 2
            data = opt_sharpe['x']

        if len([i for i in range(len(dict_data[reposition])) if round(dict_data[reposition][i], 4) % portfolio_stats(data, returns)[index_port] <= 0.005]):
            return [i for i in range(len(dict_data[reposition])) if round(dict_data[reposition][i], 4) % portfolio_stats(array_weights, returns)[index_port] <= 0.005][0] - 1
        
        return None


    def Var_Port(weights, returns):
        port_ret = np.dot(returns, weights)
        port_mean = port_ret.mean()
        port_mean

        port_stdev = np.sqrt(multi_dot([weights.T, returns.cov(), weights]))
        port_stdev.flatten()[0]

        pVaR_90 = norm.ppf(1-0.90, port_mean, port_stdev).flatten()[0]
        pVaR_95 = norm.ppf(1-0.95, port_mean, port_stdev).flatten()[0]
        pVaR_99 = norm.ppf(1-0.99, port_mean, port_stdev).flatten()[0]

        return pVaR_90, pVaR_95, pVaR_99


    def CVar_Port(weights, returns):
        Port = np.dot(returns, weights)
        Port.sort()

        hVaR_99 = np.quantile(Port, 0.01)
        hVaR_95 = np.quantile(Port, 0.05)
        hVaR_90 = np.quantile(Port, 0.1)

        CVaR_90 = Port[Port <= hVaR_90].mean()
        CVaR_95 = Port[Port <= hVaR_95].mean()
        CVaR_99 = Port[Port <= hVaR_99].mean()

        return CVaR_90, CVaR_95, CVaR_99, hVaR_90, hVaR_95, hVaR_99

    
    df = df_symbols.copy(deep=True)

    numofasset = len(df.columns)
    numofportfolio = 5000

    returns = df.pct_change().dropna()

    # fig = plot_normalized_price(df)
    # st.pyplot(fig)

    annual_returns = (returns.mean() * 252)
    
    # fig = plot_annualized_returns(annual_returns)
    # st.pyplot(fig)

    vols = returns.std()
    annual_vols = vols*np.sqrt(252)
    
    # fig = plot_annualized_volatility(annual_vols)
    # st.pyplot(fig)

    wts = numofasset * [1./numofasset]
    wts = np.array(wts)[:, np.newaxis]

    array_weights = np.full((numofasset, 1), 1/numofasset)
    # array_weights = np.array([[0.15], [0.05], [0.07], [0.15], [0.05], [0.14], [0.15], [0.15], [0.05], [0.04]])

    # Initialize the lists
    rets = []
    vols = []
    wts = []

    # Simulate 5,000 portfoliosplot_index
    for i in range(5000):
        # Generate random weights
        weights = np.random.random(numofasset)[:, np.newaxis]
        # st.write(weights)
        # Set weights such that sum of weights equals 1

        weights /= sum(weights)
        # st.write(weights)
        # Portfolio statistics
        rets.append(weights.T @ np.array(returns.mean() * 252)[:, np.newaxis])
        vols.append(np.sqrt(multi_dot([weights.T, returns.cov()*252, weights])))
        wts.append(weights.flatten())

    # Record values
    port_rets = np.array(rets).flatten()
    port_vols = np.array(vols).flatten()
    port_wts = np.array(wts)

    msrp_df = pd.DataFrame({
        'returns': port_rets,
        'volatility': port_vols,
        'sharpe_ratio': (port_rets - 0.015)/port_vols,
        'weights': list(port_wts)
    })

    msrp = msrp_df.iloc[msrp_df['sharpe_ratio'].idxmax()]

    # fig = plot_monte_carlo_simulated_allocation(msrp, port_vols, port_rets)
    # st.pyplot(fig)

    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in range(numofasset))
    initial_wts = numofasset*[1./numofasset]

    opt_sharpe = sco.minimize(min_sharpe_ratio, initial_wts, args=(returns,), method='SLSQP', bounds=bnds, constraints=cons)

    opt_var = sco.minimize(min_variance, initial_wts, args=(returns,), method='SLSQP', bounds=bnds, constraints=cons)
    array_weights = array_weights.flatten()

    targetrets = np.linspace(port_rets.min(), port_rets.max(), 250)
    tvols = []

    tweights = []

    for tr in targetrets:
        ef_cons = ({'type': 'eq', 'fun': lambda x: portfolio_stats(x, returns)[0] - tr},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

        opt_ef = sco.minimize(min_volatility, initial_wts, args=(returns,), method='SLSQP', bounds=bnds, constraints=ef_cons)

        tvols.append(opt_ef['fun'])
        tweights.append(np.round(opt_ef['x'], 2))

    targetweights = np.array(tweights)
    targetvols = np.array(tvols)

    dict_data = {}

    dict_data['retorno'] = targetrets
    dict_data['volatilidade'] = targetvols
    dict_data['sharpe'] = targetrets/targetvols
    dict_data['weight'] = targetweights

    # index_dict = [i for i in range(len(dict_data["retorno"])) if round(dict_data["retorno"][i], 4) % portfolio_stats(array_weights, returns)[0] <= 0.005]

    # retorno_print = np.round(dict_data['retorno'][index_dict[0] - 1], 2)
    # vol_print = np.round(dict_data['volatilidade'][index_dict[0] - 1], 2)
    # weights_plot = [f"{str(np.round(i, 2))}%" for i in dict_data['weight'][index_dict[0] - 1]]

    # df_atv_table = pd.DataFrame( np.array([[retorno_print, vol_print, weights_plot]]), columns=['Retorno', 'Volatilidade', 'Peso'])
    # st.table(df_atv_table)

    # st.write(f"Retorno: {retorno_print}")
    # st.write(f"volatilidade: {vol_print}")
    # st.write(f"weight: {weights_plot}")
    # st.write(f"somaweight: {sum(dict_data['weight'][index_dict[0] - 1])*100}")

    index_dict = wallet_reposition("retorno", array_weights, dict_data, opt_sharpe, returns)

    # TODO: when the slider is pressed the page can't reload
    # plot_index = st.slider('Movimento sua cartira dentro da fronteira eficiente', 0, 249, 1)
    # fig = plot_int(plot_index, targetvols, targetrets, opt_sharpe, opt_var, dict_data, array_weights, returns, st)
    # st.pyplot(fig)