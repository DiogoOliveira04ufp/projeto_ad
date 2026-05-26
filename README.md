# projeto_ad

Projeto final da cadeira de Análise de Dados do curso de Engenharia Informática da Universidade Fernando Pessoa do aluno Diogo Oliveira.

Consiste na análise de um [dataset](https://www.kaggle.com/datasets/tristenterracciano/fia-wec-lap-data-20122022/) de todas as voltas de todas as corridas do Campeonato Mundial de Resistência da FIA, desde as 12 Horas de Sebring de 2012 até às 24 Horas de Le Mans de 2022.

Faz o merge a partir de um dataset feito a partir do API histórico do Open-Meteo, de onde vão ser tirados dados sobre a temperatura, precipitação e velocidade do vento de cada corrida.


## Execução

Este é um projeto `uv` portanto será necessário tê-lo instalado.

Para instalar todos os pacotes:

```sh
uv sync
```

Para correr os scripts:
* uv
```sh
uv run src/main.py
```

* Python
```
python3 src/main.py
```