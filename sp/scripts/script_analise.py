
import pandas as pd
import os


##################### FUNÇÃO PARA PADRONIZAR MUNICÍPIOS #####################

def padronizar_municipios(df):

    df['Municipio'] = (
        df['Municipio']
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


##################### FUNÇÃO PARA PROCESSAR CADA ANO #####################

def processar_ano(ano):

    print(f'\nProcessando {ano}...')


    ##################### EVASÃO #####################

    abandono = pd.read_csv(
        fr'sp/dados_limpos/total_abandono_escolar_{ano}.csv',
        sep=';',
        decimal=',',
        encoding='utf-8'
    )

    abandono = padronizar_municipios(abandono)


    ##################### INFRAESTRUTURA #####################

    infra = pd.read_csv(
        fr'sp/dados_limpos/censo_escolar_{ano}_limpo.csv',
        encoding='utf-8'
    )

    infra = padronizar_municipios(infra)


    ##################### CONVERTER SIM/NÃO #####################

    mapeamento = {
        'Sim': 1,
        'Não': 0
    }

    colunas_infra = [
        'Acesso à internet para alunos',
        'Acesso ao Laboratório de informática',
        'Acesso à Biblioteca',
        'Acesso à Alimentação',
        'Acesso ao Refeitório',
        'Acesso à Água potável',
        'Acesso à Energia elétrica da rede pública',
        'Acesso à Esgoto da rede pública',
        'Acesso ao Banheiro',
        'Acesso à Quadra de esportes'
    ]

    for coluna in colunas_infra:
        infra[coluna] = infra[coluna].replace(mapeamento)


    ##################### AGRUPAR POR MUNICÍPIO #####################

    infra_agrupada = (
        infra
        .groupby('Municipio')[colunas_infra]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )


    ##################### JUNTAR TABELAS #####################

    relacao = abandono.merge(
        infra_agrupada,
        on='Municipio',
        how='inner'
    )

    relacao['Total Abandono Escolar'] = pd.to_numeric(
        relacao['Total Abandono Escolar'], errors='coerce'
    )


    ##################### MOSTRAR RESULTADOS #####################

    print('\nQuantidade de linhas:')
    print(relacao.shape)


    ##################### CORRELAÇÃO #####################

    print('\n========== CORRELAÇÕES COM EVASÃO ESCOLAR ==========')

    correlacoes = {
        'Internet':         'Acesso à internet para alunos',
        'Alimentação':      'Acesso à Alimentação',
        'Água potável':     'Acesso à Água potável',
        'Energia elétrica': 'Acesso à Energia elétrica da rede pública',
        'Esgoto':           'Acesso à Esgoto da rede pública',
        'Lab. informática': 'Acesso ao Laboratório de informática',
        'Biblioteca':       'Acesso à Biblioteca',
        'Refeitório':       'Acesso ao Refeitório',
        'Banheiro':         'Acesso ao Banheiro',
        'Quadra esportes':  'Acesso à Quadra de esportes',
    }

    for nome, coluna in correlacoes.items():
        corr = relacao['Total Abandono Escolar'].corr(relacao[coluna])
        print(f'{nome:<20} → {corr:.4f}')


    ##################### TOP 10 MAIOR EVASÃO #####################

    print('\n========== TOP 10 MUNICÍPIOS COM MAIOR EVASÃO ==========')

    top_evasao = (
        relacao
        .sort_values(by='Total Abandono Escolar', ascending=False)
        .head(30)[['Municipio', 'Total Abandono Escolar'] + colunas_infra]
        .reset_index(drop=True)
    )

    top_evasao.index += 1  # começa do 1 em vez do 0

    print(top_evasao.to_string())


##################### SALVAR #####################

    caminho = fr'sp/dados_limpos/relacao_evasao_infraestrutura_{ano}.xlsx'
    caminho_top_evasao = fr'sp/dados_limpos/top_evasao_{ano}.xlsx'

    if os.path.exists(caminho):
        os.remove(caminho)

    if os.path.exists(caminho_top_evasao):
        os.remove(caminho_top_evasao)

    # arquivo completo
    relacao.to_excel(caminho, index=False)

    # top 20 com correlações numa segunda aba
    top_evasao = (
        relacao
        .sort_values(by='Total Abandono Escolar', ascending=False)
        .head(30)[['Municipio', 'Total Abandono Escolar'] + colunas_infra]
        .reset_index(drop=True)
    )
    top_evasao.index += 1

    correlacoes_df = pd.DataFrame({
        'Infraestrutura': list(correlacoes.keys()),
        'Correlação com Evasão': [
            relacao['Total Abandono Escolar'].corr(relacao[col])
            for col in correlacoes.values()
        ]
    }).round(4)

    with pd.ExcelWriter(caminho_top_evasao, engine='openpyxl') as writer:
        top_evasao.to_excel(writer, sheet_name='Top 20 Evasão', index=True)
        correlacoes_df.to_excel(writer, sheet_name='Correlações', index=False)

    print(f'\nArquivos {ano} salvos com sucesso!')

##################### EXECUTAR #####################

processar_ano(2022)
processar_ano(2023)
processar_ano(2024)