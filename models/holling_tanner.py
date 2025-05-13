import numpy as np
from scipy.integrate import odeint

class HollingTannerModel:
    """
    Holling-Tanner Type II predator-prey model
    
    Parameters:
    -----------
    r : float
        Prey growth rate
    K : float
        Prey carrying capacity
    a : float
        Attack rate of predator
    h : float
        Handling time of predator
    m : float
        Predator mortality rate
    c : float
        Conversion efficiency
    d : float
        Predator growth rate (depends on prey ratio)
    """
    
    def __init__(self, r=1.0, K=10.0, a=1.0, h=0.1, m=0.5, c=0.5, d=0.1):
        self.r = r      # Prey growth rate
        self.K = K      # Prey carrying capacity
        self.a = a      # Attack rate
        self.h = h      # Handling time
        self.m = m      # Predator mortality rate
        self.c = c      # Conversion efficiency
        self.d = d      # Predator growth rate
        
    def differential_equations(self, y, t):
        """Define the system of differential equations"""
        N, P = y  # N = prey, P = predator
        
        # Type II functional response
        functional_response = (self.a * N) / (1 + self.a * self.h * N)
        
        # Prey equation
        dNdt = self.r * N * (1 - N/self.K) - functional_response * P
        
        # Predator equation (ratio-dependent)
        dPdt = self.c * functional_response * P - self.m * P + self.d * P * (1 - P/(N + 1e-10))
        
        return [dNdt, dPdt]
    
    def simulate(self, initial_conditions, t):
        """
        Run the simulation
        
        Parameters:
        -----------
        initial_conditions : list
            [N0, P0] initial prey and predator populations
        t : array-like
            Time points at which to solve the system
            
        Returns:
        --------
        solution : array
            Array with shape (len(t), 2) containing prey and predator populations
        """
        solution = odeint(self.differential_equations, initial_conditions, t)
        return solution
    
    def plot_solution(self, solution, t, title="Holling-Tanner Model"):
        """Plot the simulation results"""
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 5))
        
        # Population vs time
        plt.subplot(1, 2, 1)
        plt.plot(t, solution[:, 0], label='Prey (N)')
        plt.plot(t, solution[:, 1], label='Predator (P)')
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.title('Population Dynamics')
        plt.legend()
        plt.grid(True)
        
        # Phase portrait
        plt.subplot(1, 2, 2)
        plt.plot(solution[:, 0], solution[:, 1])
        plt.xlabel('Prey Population')
        plt.ylabel('Predator Population')
        plt.title('Phase Portrait')
        plt.grid(True)
        
        plt.suptitle(title)
        plt.tight_layout()
        plt.show()