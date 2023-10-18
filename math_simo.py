import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb


def option_price(S0, K, r, T, N, option_type='european', option_style='call', sigma=0.2):
    dt = T / N
    u = np.exp(r * dt + sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Créez un arbre de prix de l'actif sous-jacent
    stock_tree = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(i + 1):
            stock_tree[j, i] = S0 * (u * (i - j)) * (d * j)

    # Initialisez l'arbre des options
    option_tree = np.zeros((N + 1, N + 1))

    # Calculez la valeur de l'option à l'échéance
    if option_style == 'call':
        option_tree[:, N] = np.maximum(0, stock_tree[:, N] - K)
    elif option_style == 'put':
        option_tree[:, N] = np.maximum(0, K - stock_tree[:, N])

    # Travaillez à rebours pour estimer le prix de l'option
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            if option_type == 'european':
                option_tree[j, i] = np.exp(-r * dt) * (
                    p * option_tree[j, i + 1] + (1 - p) * option_tree[j + 1, i + 1])
            elif option_type == 'american':
                if option_style == 'call':
                    option_tree[j, i] = max(
                        stock_tree[j, i] - K,
                        np.exp(-r * dt) * (p *
                                           option_tree[j, i + 1] + (1 - p) * option_tree[j + 1, i + 1])
                    )
                elif option_style == 'put':
                    option_tree[j, i] = max(
                        K - stock_tree[j, i],
                        np.exp(-r * dt) * (p *
                                           option_tree[j, i + 1] + (1 - p) * option_tree[j + 1, i + 1])
                    )

    return option_tree[0, 0], stock_tree


# Demandez à l'utilisateur de saisir les paramètres
S0 = float(input('Prix de l\'actif sous-jacent (S0) : '))
K = float(input('Prix d\'exercice (K) : '))
r = float(input('Taux d\'intérêt (r) : '))
T = float(input('Durée (T) : '))
N = int(input('Nombre d\'intervalles de temps (N) : '))
sigma = float(input('Volatilité (σ) : '))

option_type = input('Type d\'option (european/american) : ').lower()
option_style = input('Type d\'option (call/put) : ').lower()

option_price, stock_tree = option_price(
    S0, K, r, T, N, option_type, option_style, sigma)

if option_type == 'european':
    print(f'Prix de l\'option européenne : {option_price:.2f}')
elif option_type == 'american':
    print(f'Prix de l\'option américaine : {option_price:.2f}')

# Créer un graphique de l'arbre binomial
plt.figure(figsize=(10, 6))

# Afficher l'arbre
# Afficher l'arbre
for i in range(N + 1):
    for j in range(i + 1):
        plt.scatter(j, i, c='b', marker='o')
        plt.text(j, i, f'{stock_tree[i,j]:.2f}', ha='center', va='bottom')

# Lier les nœuds de l'arbre
for i in range(N):
    for j in range(i + 1):
        plt.plot([j, j + 1], [i, i + 1], 'k-')
        plt.plot([j, j], [i, i + 1], 'k-')
        plt.plot([j + 1, j + 1], [i, i + 1], 'k-')

plt.xlabel('Étapes')
plt.ylabel('Temps')
plt.title('Arbre binomial du prix de l\'actif sous-jacent')
plt.grid(True)
plt.show()
