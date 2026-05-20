# 1D Spatial Prisoner's Dilemma 🧬

> **Trabalho da diciplina de Autômatos Celulares(UFRRJ)**
> Uma recriação computacional do Dilema do Prisioneiro em Autômatos Celulares Unidimensionais, focada na visualização de padrões evolutivos e invasão de estratégias.

---

## 🚀 Como Executar o Projeto

Para clonar e rodar esta simulação na sua própria máquina, siga os passos abaixo no terminal:

**1. Clone o repositório e entre na pasta:**
```bash
git clone [https://github.com/SEU_USUARIO/1d-pd-automata.git](https://github.com/SEU_USUARIO/1d-pd-automata.git)

cd 1d-pd-automata
```
**2. Crie e ative o ambiente virtual:**

No Linux/Mac/WSL:
```bash
python3 -m venv .venv

source .venv/bin/activate
```
No Windows (CMD/PowerShell):
```bash
python -m venv .venv

.venv\Scripts\activate
```

**3. Instale as dependências:**
```bash
pip install numpy matplotli
```
**4. Rode a simulação:**
```bash
python3 dilema.py
```
# 🔬 A Experiência e Regras do Sistema
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
