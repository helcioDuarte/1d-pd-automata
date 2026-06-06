import argparse
import csv
import json
import os
import time
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class DilemaDoPrisioneiro1D:
    def __init__(self, L=500, rho_0=0.7, T=1.20, z=7, rodadas=200, symmetric=True, viz_esq=None, viz_dir=None, self_interaction=None):
        self.L = L
        self.T = T
        self.z = z
        self.rodadas = rodadas

        # Configuração da vizinhança: podemos aceitar valores explícitos de viz_esq/viz_dir
        # ou derivar a vizinhança a partir de z (simétrica por padrão).
        # viz_esq/viz_dir representam números de vizinhos à esquerda/direita EXCLUINDO o próprio índice.
        if viz_esq is not None and viz_dir is not None:
            left = int(viz_esq)
            right = int(viz_dir)
            if self_interaction is None:
                self.self_interaction = False
            else:
                self.self_interaction = bool(self_interaction)
        else:
            # Derivar a vizinhança a partir de z
            if symmetric:
                if z % 2 == 1:
                    # ímpar: inclui autointeração
                    left = right = (z - 1) // 2
                    self.self_interaction = True
                else:
                    # par: sem autointeração, mesmos vizinhos de cada lado
                    left = right = z // 2
                    self.self_interaction = False
            else:
                # Assimétrico padrão: distribui à esquerda a metade inteira
                left = z // 2
                # direita pega o restante (sem autointeração por padrão)
                right = z - left
                if z % 2 == 1:
                    # quando z ímpar, por coerência, ativamos autointeração e ajustamos
                    right = z - left - 1
                    self.self_interaction = True
                else:
                    self.self_interaction = False

        self.viz_esq = left
        self.viz_dir = right

        # Gerar lista de offsets de vizinhança que soma exatamente z vizinhos
        offsets = []
        # offsets à esquerda: -left ... -1
        if self.viz_esq > 0:
            offsets.extend(range(-self.viz_esq, 0))
        # autointeração se ativada
        if getattr(self, 'self_interaction', False):
            offsets.append(0)
        # offsets à direita: 1 ... right
        if self.viz_dir > 0:
            offsets.extend(range(1, self.viz_dir + 1))

        # Sanidade: garanta que o número de offsets é igual a z
        if len(offsets) != self.z:
            # ajustar automaticamente se houver discrepância
            # preferimos manter a soma alvo z; truncar ou estender do lado direito
            if len(offsets) > self.z:
                offsets = offsets[:self.z]
            else:
                # adicionar deslocamentos à direita crescentes
                extra = self.z - len(offsets)
                last = self.viz_dir
                for k in range(1, extra + 1):
                    offsets.append(last + k)

        self.neighbor_offsets = offsets
        
        # Inicia o grid (1 = Cooperador, 0 = Desertor)
        self.grid = np.random.choice([0, 1], size=L, p=[1 - rho_0, rho_0]).astype(np.int8)

        # Matriz para guardar o histórico de cores (Eixo Y = Tempo, Eixo X = Jogadores)
        self.historico_cores = np.zeros((rodadas, L), dtype=np.int8)

        # Preenche a primeira linha (tempo t=0)
        # 0: cooperador estável (blue), 1: desertor estável (red)
        self.historico_cores[0, :] = np.where(self.grid == 1, 0, 1)

    def calcular_payoffs(self):
        # vetorize: somar rolamentos para obter número de cooperadores na vizinhança
        # cada offset contribui com np.roll(self.grid, -j)
        neighbor_sum = np.zeros(self.L, dtype=np.int32)
        for j in self.neighbor_offsets:
            neighbor_sum += np.roll(self.grid, -j)

        # payoff = neighbor_sum * (T - (T-1)*theta)
        payoffs = neighbor_sum.astype(float) * (self.T - (self.T - 1.0) * self.grid.astype(float))
        return payoffs

    def evoluir(self, t):
        payoffs = self.calcular_payoffs()

        # Construir matriz de payoffs dos vizinhos alinhada por posição i via roll
        K = len(self.neighbor_offsets)
        stacked_payoffs = np.empty((K, self.L), dtype=float)
        stacked_states = np.empty((K, self.L), dtype=np.int8)
        for idx, j in enumerate(self.neighbor_offsets):
            stacked_payoffs[idx, :] = np.roll(payoffs, -j)
            stacked_states[idx, :] = np.roll(self.grid, -j)

        max_payoffs = stacked_payoffs.max(axis=0)
        argmax_idx = stacked_payoffs.argmax(axis=0)

        # Escolher estratégia vencedora onde exista payoff maior que o próprio
        melhor_states = stacked_states[argmax_idx, np.arange(self.L)]
        manter = (max_payoffs <= payoffs)
        novo_grid = np.where(manter, self.grid, melhor_states).astype(np.int8)

        # Mapear cores: 0 coopera e permaneceu(blue), 1 deserta e permaneceu(red),
        # 2 virou cooperador (green), 3 virou desertor (yellow)
        cor = np.full(self.L, 0, dtype=np.int8)
        cor[np.logical_and(novo_grid == 1, self.grid == 1)] = 0
        cor[np.logical_and(novo_grid == 0, self.grid == 0)] = 1
        cor[np.logical_and(novo_grid == 1, self.grid == 0)] = 2
        cor[np.logical_and(novo_grid == 0, self.grid == 1)] = 3

        self.historico_cores[t, :] = cor
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

    def proporcao_cooperadores(self):
        return float(np.mean(self.grid))


def run_single(L, rho_0, T, z, rodadas, symmetric, viz_esq, viz_dir, self_interaction, seed=None):
    if seed is not None:
        np.random.seed(int(seed))
    jogo = DilemaDoPrisioneiro1D(L=L, rho_0=rho_0, T=T, z=z, rodadas=rodadas,
                                 symmetric=symmetric, viz_esq=viz_esq, viz_dir=viz_dir, self_interaction=self_interaction)
    jogo.simular()
    rho_final = jogo.proporcao_cooperadores()
    return rho_final, jogo


def _worker_run_single(args):
    # helper for multiprocessing mapping
    L, rho_0, T, z, rodadas, symmetric, viz_esq, viz_dir, self_interaction, seed = args
    rho_final, _ = run_single(L, rho_0, T, z, rodadas, symmetric, viz_esq, viz_dir, self_interaction, seed=seed)
    return rho_final


def run_ensemble(L, rho_0, T, z, rodadas, symmetric, viz_esq, viz_dir, self_interaction, runs=100, seed=None, out_prefix=None, workers=1):
    base_seed = int(seed) if seed is not None else None
    seeds = [None] * runs if base_seed is None else [base_seed + i for i in range(runs)]

    args_list = [(L, rho_0, T, z, rodadas, symmetric, viz_esq, viz_dir, self_interaction, s) for s in seeds]

    results = []
    if workers is None or workers <= 1:
        for args in args_list:
            results.append(_worker_run_single(args))
    else:
        with multiprocessing.Pool(processes=workers) as pool:
            results = pool.map(_worker_run_single, args_list)

    arr = np.array(results)
    mean = float(arr.mean())
    std = float(arr.std())

    if out_prefix:
        dirn = os.path.dirname(out_prefix)
        if dirn:
            os.makedirs(dirn, exist_ok=True)
        csv_path = f"{out_prefix}_T{T:.3f}_ensemble.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["run", "rho_final"]) 
            for idx, val in enumerate(results):
                writer.writerow([idx, val])
        print(f"Ensemble salvo em {csv_path}")

    return mean, std, results


def scan_T(Tmin, Tmax, dT, L, rho_0, z, rodadas, symmetric, viz_esq, viz_dir, self_interaction, runs_per_T, seed=None, out_dir="out", workers=1):
    os.makedirs(out_dir, exist_ok=True)
    Ts = []
    means = []
    stds = []
    t = Tmin
    while t <= Tmax + 1e-12:
        print(f"Rodando T={t:.3f}")
        mean, std, _ = run_ensemble(L, rho_0, t, z, rodadas, symmetric, viz_esq, viz_dir, self_interaction, runs=runs_per_T, seed=seed, workers=workers)
        Ts.append(t)
        means.append(mean)
        stds.append(std)
        t = round(t + dT, 12)

    # salvar CSV
    csv_path = os.path.join(out_dir, "rho_infty_vs_T.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["T", "rho_mean", "rho_std"])
        for Ti, m, s in zip(Ts, means, stds):
            writer.writerow([f"{Ti:.6f}", f"{m:.6f}", f"{s:.6f}"])
    print(f"Scan salvo em {csv_path}")

    # plot
    plt.figure()
    plt.errorbar(Ts, means, yerr=stds, fmt='-o')
    plt.xlabel('T')
    plt.ylabel('rho_infty')
    plt.title('Asymptotic proportion of cooperators vs T')
    plot_path = os.path.join(out_dir, "rho_infty_vs_T.png")
    plt.savefig(plot_path)
    print(f"Plot salvo em {plot_path}")
    return csv_path, plot_path

def _main():
    parser = argparse.ArgumentParser(description='1D Spatial Prisoner\'s Dilemma simulator')
    parser.add_argument('--L', type=int, default=500)
    parser.add_argument('--rho0', type=float, default=0.7)
    parser.add_argument('--T', type=float, help='single T value')
    parser.add_argument('--Tmin', type=float, default=1.0)
    parser.add_argument('--Tmax', type=float, default=2.0)
    parser.add_argument('--dT', type=float, default=0.1)
    parser.add_argument('--z', type=int, default=7)
    parser.add_argument('--rodadas', type=int, default=200)
    parser.add_argument('--symmetric', action='store_true')
    parser.add_argument('--viz_esq', type=int, default=None)
    parser.add_argument('--viz_dir', type=int, default=None)
    parser.add_argument('--self_interaction', action='store_true')
    parser.add_argument('--ensembles', type=int, default=1)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--out', type=str, default='out')
    args = parser.parse_args()

    if args.T is not None:
        mean, std, _ = run_ensemble(args.L, args.rho0, args.T, args.z, args.rodadas, args.symmetric, args.viz_esq, args.viz_dir, args.self_interaction, runs=args.ensembles, seed=args.seed, out_prefix=os.path.join(args.out, 'ensemble'), workers=args.workers)
        print(f"T={args.T} -> mean={mean:.6f}, std={std:.6f}")
    else:
        scan_T(args.Tmin, args.Tmax, args.dT, args.L, args.rho0, args.z, args.rodadas, args.symmetric, args.viz_esq, args.viz_dir, args.self_interaction, runs_per_T=args.ensembles, seed=args.seed, out_dir=args.out, workers=args.workers)


if __name__ == "__main__":
    _main()