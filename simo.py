from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

root = Tk()
root.title('Graph Plotter')
root.geometry("400x300")

# Define variables as StringVar to store user inputs
S0 = StringVar()
K = StringVar()
r = StringVar()
T = StringVar()
N = StringVar()
option_type = StringVar()
option_style = StringVar()
option_sigma = StringVar()

# Function to perform calculations and display the plot


def calculate_and_plot():
    # Get user inputs from StringVar and convert to float
    S0 = float(S0.get())
    K = float(K.get())
    r = float(r.get())
    T = float(T.get())
    N = int(N.get())
    option_type = option_type.get()
    option_style = option_style.get()
    option_sigma = option_sigma.get()

    # Perform mathematical operations on the variables

    dt = T / N
    u = np.exp(r * dt + option_sigma * np.sqrt(dt))
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


# Label and Entry widgets for user input
Label(root, text="S0:").pack()
Entry(root, textvariable=S0).pack()

Label(root, text="K").pack()
Entry(root, textvariable=K).pack()

Label(root, text="r").pack()
Entry(root, textvariable=r).pack()

Label(root, text="T").pack()
Entry(root, textvariable=T).pack()

Label(root, text="N").pack()
Entry(root, textvariable=N).pack()

Label(root, text="option_type").pack()
Entry(root, textvariable=option_type).pack()

Label(root, text="option_style").pack()
Entry(root, textvariable=option_style).pack()

Label(root, text="option_sigma").pack()
Entry(root, textvariable=option_sigma).pack()

# Button to calculate and display the plot
Button(root, text='Submit', command=calculate_and_plot).pack()

root.mainloop()
