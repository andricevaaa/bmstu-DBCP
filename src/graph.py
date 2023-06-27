import matplotlib.pyplot as plt

# Sample data
x = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]  # x-coordinates
y1 = [0.009931, 0.011121, 0.014892, 0.018479, 0.021430, 0.025890, 0.037692, 0.044029, 0.048321, 0.051124]  # y-values for the first array
y2 = [0.019872, 0.024128, 0.028439, 0.033996, 0.039122, 0.045900, 0.059679, 0.067951, 0.078347, 0.083025]  # y-values for the second array

# Create the plot
plt.plot(x, y1, label='Первый запрос')
plt.plot(x, y2, label='Второй запрос')

# Add labels and title
plt.ylabel('Время')
plt.xlabel('Число записей')
plt.grid()

# Add a legend
plt.legend()

# Show the plot
plt.show()
