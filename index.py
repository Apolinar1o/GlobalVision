import pandas as pd
import matplotlib.pyplot as plt

# Carregar os arquivos JSON
accounts = pd.read_json('accounts_anonymized.json')
cases = pd.read_json('support_cases_anonymized.json')

# Parte 1: Exploração dos Dados
print("Accounts Dataset:")
print(accounts.head())

print("\nSupport Cases Dataset:")
print(cases.head())

# Verificar valores ausentes
print("\nValores ausentes em Accounts:")
print(accounts.isnull().sum())

print("\nValores ausentes em Cases:")
print(cases.isnull().sum())

# Parte 2: Limpeza e Tratamento de Dados
# Preenchendo valores ausentes nas colunas 'account_country' e 'account_industry' com 'Unknown'
accounts['account_country'].fillna('Unknown', inplace=True)
accounts['account_industry'].fillna('Unknown', inplace=True)

# Remover registros no dataset de 'cases' onde 'account_sfid' é nulo (não há correspondência com 'accounts')
cases.dropna(subset=['account_sfid'], inplace=True)

# Juntar os datasets com base no account_sfid
merged_data = pd.merge(cases, accounts, on='account_sfid', how='inner')

# Visualizar dados mesclados
print("\nDados Mesclados:")
print(merged_data.head())

# Parte 3: Análise de Casos
# Contar o número de casos por conta
cases_per_account = merged_data.groupby('account_sfid').size().reset_index(name='TotalCases')
print("\nTotal de Casos por Conta:")
print(cases_per_account.head())

# Analisar os status dos casos
status_analysis = merged_data['case_status'].value_counts()
print("\nAnálise de Status dos Casos:")
print(status_analysis)

# Parte 4: Visualização dos Dados
# Gráfico de Barras: Número de Casos por Conta
plt.figure(figsize=(10, 6))
plt.bar(cases_per_account['account_sfid'], cases_per_account['TotalCases'], color='skyblue')
plt.title("Número de Casos por Conta", fontsize=16)
plt.xlabel("account_sfid", fontsize=12)
plt.ylabel("Total de Casos", fontsize=12)
plt.xticks(rotation=90)  # Girar os IDs se necessário
plt.tight_layout()
plt.show()

# Gráfico de Pizza: Distribuição dos Status dos Casos
plt.figure(figsize=(8, 8))
status_analysis.plot(kind='pie', autopct='%1.1f%%', startangle=140, title="Distribuição de Status dos Casos")
plt.ylabel("")  # Remove o rótulo do eixo Y
plt.show()

# Parte 5: Insights e Recomendações
# Gerar insights com base nos gráficos
print("\nInsights Derivados:")
print("- As contas com mais casos podem ser priorizadas para suporte.")
print("- O status mais comum pode indicar problemas recorrentes ou atrasos na resolução.")

# Propostas:
print("\nPropostas de Ação:")
print("1. Implementar um sistema de acompanhamento para as contas com maior número de casos.")
print("2. Revisar os processos para os casos com status mais comuns, buscando otimizar sua resolução.")