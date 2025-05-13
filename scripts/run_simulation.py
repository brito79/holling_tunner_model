import numpy as np
from matplotlib import pyplot as plt
from models.holling_tanner import HollingTannerModel

def main():
    # Default parameters
    params = {
        'r': 1.0,   # Prey growth rate
        'K': 10.0,   # Carrying capacity
        'a': 1.0,    # Attack rate
        'h': 0.1,    # Handling time
        'm': 0.5,    # Predator mortality
        'c': 0.5,    # Conversion efficiency
        'd': 0.1     # Predator growth
    }
    
    # Simulation parameters
    initial_conditions = [5.0, 2.0]  # Initial prey and predator populations
    t_max = 100                      # Simulation time
    num_points = 1000                # Number of time points
    
    # Get user input for parameters
    print("Enter model parameters (press Enter for defaults):")
    for param, default in params.items():
        user_input = input(f"{param} (default={default}): ")
        if user_input:
            params[param] = float(user_input)
    
    # Get initial conditions
    user_N0 = input(f"Initial prey population (default={initial_conditions[0]}): ")
    if user_N0:
        initial_conditions[0] = float(user_N0)
    
    user_P0 = input(f"Initial predator population (default={initial_conditions[1]}): ")
    if user_P0:
        initial_conditions[1] = float(user_P0)
    
    # Create and run model
    model = HollingTannerModel(**params)
    t = np.linspace(0, t_max, num_points)
    solution = model.simulate(initial_conditions, t)
    
    # Plot results
    model.plot_solution(solution, t)
    
    # Save data option
    save = input("Save data to CSV? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename (default=simulation_data.csv): ") or "simulation_data.csv"
        data = np.column_stack((t, solution[:, 0], solution[:, 1]))
        np.savetxt(filename, data, delimiter=',', 
                  header='time,prey,predator', comments='')
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()