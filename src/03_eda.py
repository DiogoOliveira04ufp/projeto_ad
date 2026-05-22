import pandas as pd

df = pd.read_csv("data/wec_clean.csv", low_memory=False)

print("=" * 60)
print("ANÁLISE EXPLORATÓRIA (EDA)")
print("=" * 60)

# Estatísticas gerais
print("\n--- Estatísticas descritivas ---")
print(df[["lap_time_s", "top_speed", "kph", "temperature", "precipitation"]].describe().round(2))

# Por fabricante
print("\n--- Tempo médio de volta por fabricante ---")
print(df.groupby("manufacturer")["lap_time_s"].agg(["mean", "std", "min"]).round(2).sort_values("mean"))

# Por classe
print("\n--- Tempo médio por classe ---")
print(df.groupby("class")["lap_time_s"].agg(["mean", "std"]).round(2))

# Por circuito
print("\n--- Velocidade máxima por circuito ---")
print(df.groupby("circuit")["top_speed"].agg(["mean", "max"]).round(2).sort_values("max", ascending=False))

# Distribuição de variáveis categóricas
print("\n--- Distribuição por classe ---")
print(df["class"].value_counts())

print("\n--- Distribuição por temporada ---")
print(df["season"].value_counts())

# Correlações
df["hour_numeric"] = pd.to_datetime(df["hour"], format="%H:%M:%S.%f").dt.hour + pd.to_datetime(df["hour"], format="%H:%M:%S.%f").dt.minute / 60

print("\n--- Correlação entre variáveis numéricas ---")
cols = ["lap_time_s", "top_speed", "kph", "hour_numeric", "temperature", "precipitation", "windspeed"]
print(df[cols].corr().round(2))

# Relação clima vs tempo de volta
print("\n--- Impacto da precipitação nos tempos ---")
df["chuva"] = df["precipitation"] > 0
print(df.groupby("chuva")["lap_time_s"].agg(["mean", "std", "count"]).round(2))

print("\n--- Correlação temperatura vs lap_time_s por circuito ---")
print(df.groupby("circuit")[["temperature", "lap_time_s"]].corr().unstack()["lap_time_s"]["temperature"].round(3))