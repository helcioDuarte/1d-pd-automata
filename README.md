# 1D Spatial Prisoner's Dilemma 🧬

> **Trabalho da diciplina de Autômatos Celulares(UFRRJ)**
> Uma recriação computacional do Dilema do Prisioneiro em Autômatos Celulares Unidimensionais, focada na visualização de padrões evolutivos e invasão de estratégias.

---

## Como Executar o Projeto

Para clonar e rodar esta simulação na sua própria máquina, siga os passos abaixo no terminal:

**1. Clone o repositório e entre na pasta:**
```bash
git clone https://github.com/helcioDuarte/1d-pd-automata.git

cd 1d-pd-automata
```
**2. Criar e ativar o ambiente virtual (.venv) — passo a passo**

No Linux / macOS / WSL:
```bash
# cria o ambiente
python3 -m venv .venv

# ativa o ambiente
source .venv/bin/activate
```

No Windows (CMD):
```bat
python -m venv .venv
.venv\Scripts\activate
```

**3. Instalar dependências**

Com o ambiente ativado, instale tudo via `requirements.txt`:
```bash
pip install -r requirements.txt
```

**4. Executar a simulação**

Ainda com a `.venv` ativada, rode o script principal do projeto (nome do arquivo no repositório):
```bash
python3 dlema.py
```

Se estiver no Windows e o comando acima falhar, tente `python dlema.py`.
# A Experiência e Regras do Sistema
## 1. O Ambiente e as Condições Iniciais

- A simulação ocorre em uma matriz unidimensional (uma linha) com tamanho $L$. Para gerar os resultados finais, os autores usaram $L=1000$ células.
- Cada célula representa um jogador que possui um de dois estados (estratégias): $\theta=1$ para cooperador (cooperator) ou $\theta=0$ para desertor (defector).
- A configuração inicial do sistema no tempo $t=0$ é aleatória e segue uma distribuição uniforme.
- A quantidade de cooperadores iniciais é controlada pelo parâmetro $\rho_0$.

## 2. A Vizinhança e a Matriz de Pagamento (Payoffs)

- Cada jogador interage com uma vizinhança de tamanho $z$. Essa vizinhança pode ser simétrica ou assimétrica.
- Se o valor de $z$ for ímpar, o jogador joga contra os vizinhos ao seu redor e também contra si mesmo (autointeração).
- A pontuação do jogo utiliza os valores modificados de Tucker: a recompensa por cooperação mútua é $R=1$, e a punição por deserção mútua ($P$) e o ganho do "trouxa" ($S$) são zerados ($P=0$ e $S=0$).
-  A única variável da matriz de pagamento que você deve alterar durante as simulações é a Tentação ($T$), avaliada no intervalo de $1 < T \le 2$.
-  O ganho (payoff) específico do jogador $i$ ao interagir com o jogador $j$ é calculado pela fórmula: $g_{\theta_i,\theta_j} = \theta_i \theta_j + T(1-\theta_i \theta_j)\theta_j$.
-  O ganho total $P_i$ do jogador $i$ em uma rodada é a soma de todos os ganhos obtidos contra seus $z$ vizinhos.

## 3. Evolução
O sistema é totalmente determinístico e as regras de evolução darwiniana são aplicadas simultaneamente (de forma síncrona) a todos os jogadores:
1. Todos os jogadores jogam contra seus respectivos $z$ vizinhos e acumulam suas pontuações totais $P_i$.
2. O jogador $i$ olha para as pontuações totais de todos os vizinhos que fazem parte do seu grupo $z$.
3. Se a pontuação do jogador $i$ for maior ou igual à maior pontuação entre seus vizinhos, ele mantém sua estratégia (cooperador ou desertor) para a próxima rodada.
4. Se um ou mais vizinhos tiverem uma pontuação estritamente maior que a do jogador $i$, ele copia a estratégia do vizinho que obteve a maior pontuação absoluta e a utiliza no próximo passo de tempo.

## 4. Oque medir
Para ter certeza de que replicamos a experiência com sucesso, o nosso código deve ser capaz de gerar duas saídas principais:
- Gráficos de Proporção Assintótica ($\rho_\infty$): Você deve rodar o jogo até que ele alcance um equilíbrio estacionário (ou dinâmico médio) e medir a proporção final de cooperadores na grade. Ao variar o valor da Tentação ($T$) no eixo X, seu gráfico deve gerar "degraus" que mostram os pontos matemáticos exatos de transição onde a cooperação cai.
- Mapeamento de Padrões Espaço-Temporais: O grande diferencial desta pesquisa. Você deve plotar uma imagem 2D onde o eixo X representa as células (jogadores) e o eixo Y representa o avanço do tempo (rodadas). Ao colorir cooperadores de azul e desertores de vermelho, você deverá ser capaz de observar o surgimento de estruturas geométricas. Com o tempo, essas estruturas formam linhas retas conhecidas como "dedos" (fingers) e linhas diagonais chamadas de "planadores" (gliders) que viajam pelo espaço e colidem entre si.

## Uso avançado (CLI)

O script principal agora aceita argumentos via linha de comando e gera ensembles e varreduras em `T` automaticamente. Exemplos:

- Rodar uma execução única e salvar o mapa espaço-temporal:
```bash
source impl/venv/bin/activate
python3 impl/dlema.py --T 1.4 --L 500 --rho0 0.7 --z 7 --rodadas 500
```

- Rodar um ensemble para um valor de `T` (múltiplas sementes) e salvar CSV com resultados:
```bash
python3 impl/dlema.py --T 1.2 --ensembles 100 --out impl/out_results
```

- Fazer varredura em `T` e plotar `rho_infty vs T` (salva CSV + PNG em `--out`):
```bash
python3 impl/dlema.py --Tmin 1.0 --Tmax 2.0 --dT 0.05 --ensembles 100 --out impl/out_scan
```

Saídas geradas automaticamente em `--out` (ou em `out` por padrão):
- `ensemble_T{T}_ensemble.csv` — valores por run do ensemble;
- `rho_infty_vs_T.csv` — média e desvio por T (quando usar `--Tmin/--Tmax`);
- `rho_infty_vs_T.png` — gráfico com barras de erro mostrando `rho_infty` vs `T`.

Argumentos principais do CLI:
- `--L`, `--rho0`, `--T`, `--Tmin`, `--Tmax`, `--dT`, `--z`, `--rodadas`, `--ensembles`, `--seed`, `--out`, `--symmetric`, `--viz_esq`, `--viz_dir`, `--self_interaction`.

## Notas de implementação e desempenho

- Vetorização: os cálculos de payoff e a atualização foram vetorizados usando `numpy.roll` e operações em arrays, o que reduz significativamente o tempo por rodada em relação a loops Python puros.
- Paralelização: ensembles ainda são executados sequencialmente. Para acelerar ensembles grandes (por exemplo `ensembles >= 1000`), recomendo paralelizar `run_ensemble` com `multiprocessing` ou `joblib`.
- Reprodutibilidade: use `--seed` para controlar a RNG e permitir replicação dos resultados.
- Recomendações para reproduzir figuras do artigo: use `--L 1000`, `--rodadas 500` e ensembles grandes (100–1000) para calcular médias robustas; aumente `--dT`/escolha os `T` de interesse conforme as transições teóricas.
