import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['figure.figsize'] = 16, 8

import pandas as pd
import numpy as np

def plot_normalized_price(df):
    fig = plt.figure(figsize=(16, 8))
    ax = plt.axes()

    ax.set_title('Normalized Price Plot')
    ax.plot(df[-252:]/df.iloc[-252] * 100)
    
    ax.legend(df.columns, loc='upper left')
    ax.grid(True)

    return fig

def plot_annualized_returns(annual_returns):
    fig = plt.figure()
    ax = plt.axes()

    ax.bar(annual_returns.index, annual_returns *
        100, color='royalblue', alpha=0.75)
    ax.set_title('Annualized Returns (in %)')

    return fig

def plot_annualized_volatility(annual_vols):
    fig = plt.figure()
    ax = plt.axes()

    ax.bar(annual_vols.index, annual_vols*100, color='orange', alpha=0.5)
    ax.set_title('Annualized Volatility (in %)')

    return fig

def plot_monte_carlo_simulated_allocation(msrp, port_vols, port_rets):
    fig = plt.figure()
    ax = plt.axes()

    ax.set_title('Monte Carlo Simulated Allocation')

    # Simulated portfolios
    fig.colorbar(ax.scatter(port_vols, port_rets, c=port_rets / port_vols, marker='o', cmap='RdYlGn', edgecolors='black'), label='Sharpe Ratio')

    # Maximum sharpe ratio portfolio
    ax.scatter(msrp['volatility'], msrp['returns'], c='red', marker='*', s=300, label='Max Sharpe Ratio')

    ax.set_xlabel('Expected Volatility')
    ax.set_ylabel('Expected Return')
    ax.grid(True)

    return fig

def plot_int(index, targetvols, targetrets, opt_sharpe, opt_var, dict_data, array_weights, returns, st):
    # Visualize the simulated portfolio for risk and return
    fig = plt.figure()
    ax = plt.axes()

    ax.set_title('Efficient Frontier Portfolio')

    # Efficient Frontier
    fig.colorbar(ax.scatter(targetvols, targetrets, c=targetrets / targetvols, marker='x', cmap='RdYlGn', edgecolors='black'), label='Sharpe Ratio')

    # Maximum Sharpe Portfolio
    ax.plot(portfolio_stats(opt_sharpe['x'], returns)[1], portfolio_stats(opt_sharpe['x'], returns)[0], 'r*', markersize=15.0)

    # Minimum Variance Portfolio
    ax.plot(portfolio_stats(opt_var['x'], returns)[1], portfolio_stats(opt_var['x'], returns)[0], 'b*', markersize=15.0)
    # Fronteira Eficiente
    ax.plot(dict_data["volatilidade"][int(index)], dict_data["retorno"][int(index)], 'o', markersize=10.0)
    # Nosso Portifolio
    ax.plot(portfolio_stats(array_weights, returns)[1], portfolio_stats(array_weights, returns)[0], 'h', color='green', markersize=15.0)

    ax.set_xlabel('Expected Volatility')
    ax.set_ylabel('Expected Return')
    ax.grid(True)
    # VaR Paramétrico
    pVaR_90, pVaR_95, pVaR_99 = Var_Port(dict_data['weight'][int(index)], returns)

    # VaR Histórico
    pCVaR_90, pCVaR_95, pCVaR_99, pHVaR_90, pHVaR_95, pHVaR_99 = CVar_Port(dict_data['weight'][int(index)], returns)

    
    # dict_data_weights = [f"{str(np.round(i, 2))}%" for i in dict_data['weight'][int(index)]]
    df_atv_table_dict_data = pd.DataFrame( 
                        np.array([[ f'Referente ao indice {index} da fronteira eficiente',
                                    np.round(dict_data['retorno'][int(index)]*100,2), 
                                    np.round(dict_data['volatilidade'][int(index)]*100,2),
                                    np.round((dict_data['retorno'][int(index)]/dict_data['volatilidade'][int(index)]),2),
                                    dict_data['weight'][int(index)]
                                ]]), 
                        columns=['Carteira', 'Retorno', 'Volatilidade', 'Indice Sharpe', 'Pesos'])
    # st.write(f"Carteira referente a fronteira eficiente")
    # st.table(df_atv_table_dict_data)

    # pesos_acao_print = 
    # st.write(f"Pesos para cada ação: {pesos_acao_print}")
    # st.write("VaR Paramétrico \n90 :", np.round(pVaR_90*100, 2), "/95 :", np.round(pVaR_95*100, 2), "/99 :", np.round(pVaR_99*100, 2))
    # st.write("VaR Histórico   \n90 :", np.round(pHVaR_90*100, 2), "/95 :", np.round(pHVaR_95*100, 2), "/99 :", np.round(pHVaR_99*100, 2))
    # st.write("CVaR Histórico \n 90 :", np.round(pCVaR_90*100, 2), "/95 :", np.round(pCVaR_95*100, 2), "/99 :", np.round(pCVaR_99*100, 2))
    
    df_atv_table_opt_sharpe = pd.DataFrame( 
                                np.array([[ 'Maior Indice Sharpe',
                                            np.round(portfolio_stats(opt_sharpe['x'], returns)[0]*100,2), 
                                            np.round(portfolio_stats(opt_sharpe['x'], returns)[1]*100,2), 
                                            np.round(portfolio_stats(opt_sharpe['x'], returns)[2],2), 
                                            np.round(opt_sharpe['x']*100,2)]]), 
                                columns=['Carteira', 'Retorno', 'Volatilidade', 'Indice Sharpe', 'Pesos'])
    # st.write('\nCarteira Fundamentalista com maior Indice Sharpe')
    # st.table(df_atv_table_opt_sharpe)
    
    df_atv_table_opt_var = pd.DataFrame( 
                                np.array([[ 'Menor volatilidade',
                                            np.round(portfolio_stats(opt_var['x'], returns)[0]*100, 2), 
                                            np.round(portfolio_stats(opt_var['x'], returns)[1]*100, 2), 
                                            np.round(portfolio_stats(opt_var['x'], returns)[2], 2), 
                                            np.round(opt_var['x']*100, 2)]]), 
                                columns=['Carteira', 'Retorno', 'Volatilidade', 'Indice Sharpe', 'Pesos'])
    # st.write('\nCarteira Fundamentalista com menor volatilidade')
    # st.table(df_atv_table_opt_var)
    

    df_atv_table_fundamentalista = pd.DataFrame( 
                                np.array([[ 'Portfolio inserido',
                                            np.round(portfolio_stats(array_weights, returns)[0]*100,2), 
                                            np.round(portfolio_stats(array_weights, returns)[1]*100,2),
                                            np.round(portfolio_stats(array_weights, returns)[2],2),
                                            np.round(array_weights*100,2)]]), 
                                columns=['Carteira', 'Retorno', 'Volatilidade', 'Indice Sharpe', 'Pesos'])
    # st.write('\nCarteira Fundamentalista')
    # st.table(df_atv_table_fundamentalista)
    

    df_all_wallet = pd.concat([df_atv_table_dict_data, df_atv_table_opt_sharpe, df_atv_table_opt_var, df_atv_table_fundamentalista])
    # df_all_wallet = pd.DataFrame([wallets_merge])
    st.table( df_all_wallet )
    
    
    # st.write(f"Retorno : {np.round(portfolio_stats(array_weights)[0]*100,2)}% \t/ Volatilidade : {np.round(portfolio_stats(array_weights)[1]*100,2)}% \t/ Indice Sharpe : ",np.round(portfolio_stats(array_weights)[2],2))
    # st.write("Pesos : ", np.round(array_weights*100,2))

    # st.write('\nCarteira Fundamentalista Com maior Indice Sharpe  ')
    # st.write(f"Retorno : {np.round(portfolio_stats(opt_sharpe['x'])[0]*100,2)}% \t/ Volatilidade : {np.round(portfolio_stats(opt_sharpe['x'])[1]*100,2)}% \t/ Indice Sharpe : ",np.round(portfolio_stats(opt_sharpe['x'])[2],2))
    # st.write("Pesos : ", np.round(opt_sharpe['x']*100,2))
    # st.write("VaR Paramétrico \n90 :",np.round(p1VaR_90*100,2),"/95 :",np.round(p1VaR_95*100,2),"/99 :",np.round(p1VaR_99*100,2))
    # st.write("VaR Histórico \n90 :",np.round(p1HVaR_90*100,2),"/95 :",np.round(p1HVaR_95*100,2),"/99 :",np.round(p1HVaR_99*100,2))
    # st.write("CVaR Histórico \n 90 :",np.round(p1CVaR_90*100,2),"/95 :",np.round(p1CVaR_95*100,2),"/99 :",np.round(p1CVaR_99*100,2))

    # st.write('\nCarteira Fundamentalista Com menor volatilidade  ')
    # st.write(f"Retorno : {np.round(portfolio_stats(opt_var['x'])[0]*100,2)}% \t/ Volatilidade : {np.round(portfolio_stats(opt_var['x'])[1]*100,2)}% \t/ Indice Sharpe : ",np.round(portfolio_stats(opt_var['x'])[2],2))
    # st.write("Pesos : ", np.round(opt_var['x']*100,2))
    # st.write("VaR Paramétrico \n90 :",np.round(p2VaR_90*100,2),"/95 :",np.round(p2VaR_95*100,2),"/99 :",np.round(p2VaR_99*100,2))
    # st.write("VaR Histórico \n90 :",np.round(p2HVaR_90*100,2),"/95 :",np.round(p2HVaR_95*100,2),"/99 :",np.round(p2HVaR_99*100,2))
    # st.write("CVaR Histórico \n 90 :",np.round(p2CVaR_90*100,2),"/95 :",np.round(p2CVaR_95*100,2),"/99 :",np.round(p2CVaR_99*100,2))

    # st.write('\nCarteira Fundamentalista  ')
    # st.write(f"Retorno : {np.round(portfolio_stats(array_weights)[0]*100,2)}% \t/ Volatilidade : {np.round(portfolio_stats(array_weights)[1]*100,2)}% \t/ Indice Sharpe : ",np.round(portfolio_stats(array_weights)[2],2))
    # st.write("Pesos : ", np.round(array_weights*100,2))
    # st.write("VaR Paramétrico \n 90 :",np.round(p3VaR_90*100,2),"/95 :",np.round(p3VaR_95*100,2),"/99 :",np.round(p3VaR_99*100,2))
    # st.write("VaR Histórico \n 90 :",np.round(p3HVaR_90*100,2),"/95 :",np.round(p3HVaR_95*100,2),"/99 :",np.round(p3HVaR_99*100,2))
    # st.write("CVaR Histórico \n 90 :",np.round(p3CVaR_90*100,2),"/95 :",np.round(p3CVaR_95*100,2),"/99 :",np.round(p3CVaR_99*100,2))

    return fig