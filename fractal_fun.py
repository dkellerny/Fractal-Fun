import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Function to generate the Mandelbrot set
def mandelbrot(c, max_iter):
    z = np.zeros(c.shape, dtype=complex)
    div_time = np.zeros(c.shape, dtype=int)
    mask = np.full(c.shape, True, dtype=bool)
    
    for i in range(max_iter):
        z[mask] = z[mask] * z[mask] + c[mask]
        mask, old_mask = np.abs(z) < 2, mask
        div_time[mask] = i
    
    return div_time

# Function to generate the Julia set
def julia(c, z, max_iter):
    div_time = np.zeros(z.shape, dtype=int)
    mask = np.full(z.shape, True, dtype=bool)
    
    for i in range(max_iter):
        z[mask] = z[mask] * z[mask] + c
        mask, old_mask = np.abs(z) < 2, mask
        div_time[mask] = i
    
    return div_time

# Function to generate the Burning Ship fractal
def burning_ship(c, max_iter):
    z = np.zeros(c.shape, dtype=complex)
    div_time = np.zeros(c.shape, dtype=int)
    mask = np.full(c.shape, True, dtype=bool)
    
    for i in range(max_iter):
        z_real = np.abs(z.real)
        z_imag = np.abs(z.imag)
        z = z_real + 1j * z_imag
        z[mask] = z[mask] * z[mask] + c[mask]
        mask, old_mask = np.abs(z) < 2, mask
        div_time[mask] = i
    
    return div_time

def generate_fractal(fractal_type):
    width, height = 2000, 2000  # Adjust resolution
    
    # Zoom parameters and setup
    if fractal_type == 'mandelbrot':
        x_min, x_max = -2.0, 1.0
        y_min, y_max = -1.5, 1.5
        max_iter = 1000
        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = mandelbrot(C, max_iter)
        cmap = plt.cm.twilight_shifted

    elif fractal_type == 'julia':
        x_min, x_max = -1.5, 1.5
        y_min, y_max = -1.5, 1.5
        max_iter = 1000
        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)
        C = -0.7 + 0.27015j  # A common parameter for Julia sets
        Z = X + 1j * Y
        Z = julia(C, Z, max_iter)
        cmap = plt.cm.viridis

    elif fractal_type == 'burning_ship':
            # Focus on the "antenna" region
            x_min, x_max = -1.8, -1.7
            y_min, y_max = -0.08, 0.02
            max_iter = 1000
            x = np.linspace(x_min, x_max, width)
            y = np.linspace(y_min, y_max, height)
            X, Y = np.meshgrid(x, y)
            C = X + 1j * Y
            Z = burning_ship(C, max_iter)
            cmap = plt.cm.magma_r  


    else:
        raise ValueError("Unknown fractal type")

    # Normalize 
    Z = np.log(Z + 1)
    
    # Generate the fractal image
    plt.figure(figsize=(10, 10), dpi=100)
    plt.imshow(Z, cmap=cmap, extent=(x_min, x_max, y_min, y_max))
    plt.axis('off')
    file_name = f"{fractal_type}_fractal.png"
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0, dpi=600)
    plt.show()

    img = Image.open(file_name)
    img.show()

if __name__ == "__main__":
    print("Select a fractal to generate:")
    print("1. Mandelbrot")
    print("2. Julia")
    print("3. Burning Ship")
    choice = input("Enter the number of your choice: ")
    
    fractal_map = {
        '1': 'mandelbrot',
        '2': 'julia',
        '3': 'burning_ship'
    }
    
    fractal_type = fractal_map.get(choice)
    print(f"Generating {fractal_type} fractal")
    
    if fractal_type:
        generate_fractal(fractal_type)
    else:
        print("Invalid choice. Please select a valid fractal type.")
