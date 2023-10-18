from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

root = Tk()
root.title('Graph Plotter')
root.geometry("400x600")

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
    num1 = float(S0.get())
    num2 = float(K.get())
    num3 = float(r.get())
    num4 = float(T.get())
    num5 = int(N.get())
    option_t = option_type.get()
    option_s = option_style.get()
    num6 = float(option_sigma.get())

    # Perform mathematical operations on the variables
    dt = num4 / num5
    u = np.exp(num3 * dt + num6 * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(num3 * dt) - d) / (u - d)

    # Create arrays to store stock and option values
    stock_tree = np.zeros((num5 + 1, num5 + 1))
    option_tree = np.zeros((num5 + 1, num5 + 1))

    # Initialize stock and option values
    for i in range(num5 + 1):
        for j in range(i + 1):
            stock_tree[j, i] = num1 * (u ** (i - j)) * (d ** j)

    # Calculate option values at expiration
    if option_s == 'call':
        option_tree[:, num5] = np.maximum(0, stock_tree[:, num5] - num2)
    elif option_s == 'put':
        option_tree[:, num5] = np.maximum(0, num2 - stock_tree[:, num5])

    # Calculate option values backwards in time
    for i in range(num5 - 1, -1, -1):
        for j in range(i + 1):
            if option_t == 'european':
                option_tree[j, i] = np.exp(-num3 * dt) * (
                    p * option_tree[j, i + 1] + (1 - p) * option_tree[j + 1, i + 1])
            elif option_t == 'american':
                if option_s == 'call':
                    option_tree[j, i] = max(
                        stock_tree[j, i] - num2,
                        np.exp(-num3 * dt) * (p *
                                              option_tree[j, i + 1] + (1 - p) * option_tree[j + 1, i + 1])
                    )
                elif option_s == 'put':
                    option_tree[j, i] = max(
                        num2 - stock_tree[j, i],
                        np.exp(-num3 * dt) * (p *
                                              option_tree[j, i + 1] + (1 - p) * option_tree[j + 1, i + 1])
                    )

    # Calculate the option price
    option_price = option_tree[0, 0]
    result_label.config(text=f'Option Price: {option_price:.2f}')

    # Create a plot of the binomial tree
    plt.figure(figsize=(10, 6))
    for i in range(num5 + 1):
        for j in range(i + 1):
            plt.scatter(j, i, c='b', marker='o')
            plt.text(j, i, f'{stock_tree[i, j]:.2f}', ha='center', va='bottom')

    for i in range(num5):
        for j in range(i + 1):
            plt.plot([j, j + 1], [i, i + 1], 'k-')
            plt.plot([j, j], [i, i + 1], 'k-')
            plt.plot([j + 1, j + 1], [i, i + 1], 'k-')

    plt.xlabel('Steps')
    plt.ylabel('Time')
    plt.title('Binomial Tree of Underlying Asset Price')
    plt.grid(True)
    plt.show()


# Label and Entry widgets for user input
Label(root, text="S0:").pack()
Entry(root, textvariable=S0).pack()

Label(root, text="K:").pack()
Entry(root, textvariable=K).pack()

Label(root, text="r:").pack()
Entry(root, textvariable=r).pack()

Label(root, text="T:").pack()
Entry(root, textvariable=T).pack()

Label(root, text="N:").pack()
Entry(root, textvariable=N).pack()

Label(root, text="Option Type (european/american):").pack()
Entry(root, textvariable=option_type).pack()

Label(root, text="Option Style (call/put):").pack()
Entry(root, textvariable=option_style).pack()

Label(root, text="σ:").pack()
Entry(root, textvariable=option_sigma).pack()

# Button to calculate and display the plot
submit_button = Button(root, text='Submit', command=calculate_and_plot)
submit_button.pack()

# Label to display the result
result_label = Label(root, text="")
result_label.pack()

root.mainloop()
