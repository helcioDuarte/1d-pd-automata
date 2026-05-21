import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class DilemaDoPrisioneiro1D:
    def __init__(self, L=500, rho_0=0.7, T=1.20, z=7, rodadas=200):
        self.L = L
        self.T = T
        self.z = z 
        
        # Vizinhança 
        self.viz_esq = 2
        self.viz_dir = 4
        
        self.rodadas = rodadas
        
        # Inicia o grid (1 = Cooperador, 0 = Desertor)
        self.grid = np.random.choice([0, 1], size=L, p=[1 - rho_0, rho_0])
        
        # Matriz para guardar o histórico de cores (Eixo Y = Tempo, Eixo X = Jogadores)
        self.historico_cores = np.zeros((rodadas, L))
        
        # Preenche a primeira linha (tempo t=0)
        for i in range(L):
            if self.grid[i] == 1:
                self.historico_cores[0, i] = 0 # Azul
            else:
                self.historico_cores[0, i] = 1 # Vermelho

    def calcular_payoffs(self):
        payoffs = np.zeros(self.L)
        for i in range(self.L):
            cooperadores_vizinhos = 0
            
            # Usando a vizinhança assimétrica
            for j in range(-self.viz_esq, self.viz_dir + 1):
                indice_vizinho = (i + j) % self.L
                cooperadores_vizinhos += self.grid[indice_vizinho]

            if self.grid[i] == 1:
                payoffs[i] = cooperadores_vizinhos
            else:
                payoffs[i] = cooperadores_vizinhos * self.T
                
        return payoffs

    def evoluir(self, t):
        payoffs = self.calcular_payoffs()
        novo_grid = np.copy(self.grid)

        for i in range(self.L):
            maior_payoff = payoffs[i]
            melhor_estrategia = self.grid[i]

            # Inspecionando os vizinhos com base na assimetria
            for j in range(-self.viz_esq, self.viz_dir + 1):
                indice_vizinho = (i + j) % self.L
                if payoffs[indice_vizinho] > maior_payoff:
                    maior_payoff = payoffs[indice_vizinho]
                    melhor_estrategia = self.grid[indice_vizinho]
            
            novo_grid[i] = melhor_estrategia
            
            # Lógica de mapeamento de cores (Azul, Vermelho, Verde, Amarelo)
            if novo_grid[i] == 1 and self.grid[i] == 1:
                cor = 0 
            elif novo_grid[i] == 0 and self.grid[i] == 0:
                cor = 1 
            elif novo_grid[i] == 1 and self.grid[i] == 0:
                cor = 2 
            elif novo_grid[i] == 0 and self.grid[i] == 1:
                cor = 3 
                
            self.historico_cores[t, i] = cor

        self.grid = novo_grid

    def simular(self):
        print(f"Calculando {self.rodadas} rodadas. Aguarde...")
        for t in range(1, self.rodadas):
            self.evoluir(t)
            
    def exibir_grafico(self):
        mapa_cores = ListedColormap(['blue', 'red', 'green', 'yellow'])
        
        plt.figure(figsize=(10, 6))
        plt.imshow(self.historico_cores, cmap=mapa_cores, aspect='auto', interpolation='none')
        
        plt.title(f"Dilema do Prisioneiro 1D (T={self.T}, L={self.L}, z={self.z} Assimétrico)")
        plt.xlabel("Jogador")
        plt.ylabel("Tempo")
        
        if plt.isinteractive():
            plt.show()
        else:
            plt.savefig("dilema_prisioneiro_1D.png")
            print("AVISO: Modo interativo não disponível no ambiente atual.")
            print("Gráfico salvo como 'dilema_prisioneiro_1D.png'")

if __name__ == "__main__":
    jogo = DilemaDoPrisioneiro1D(L=500, rho_0=0.7, T=1.40, z=7, rodadas=200) 
    jogo.simular()
    jogo.exibir_grafico()