import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from models.holling_tanner import HollingTannerModel

def create_figure(solution, t):
    """Create matplotlib figure for GUI"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Population vs time
    ax1.plot(t, solution[:, 0], label='Prey (N)')
    ax1.plot(t, solution[:, 1], label='Predator (P)')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Population')
    ax1.set_title('Population Dynamics')
    ax1.legend()
    ax1.grid(True)
    
    # Phase portrait
    ax2.plot(solution[:, 0], solution[:, 1])
    ax2.set_xlabel('Prey Population')
    ax2.set_ylabel('Predator Population')
    ax2.set_title('Phase Portrait')
    ax2.grid(True)
    
    plt.tight_layout()
    return fig

def draw_figure(canvas, figure):
    """Draw matplotlib figure on PySimpleGUI canvas"""
    if hasattr(canvas, 'figure_canvas_agg'):
        canvas.figure_canvas_agg.get_tk_widget().forget()
        plt.close('all')
    
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas.TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def main():
    # Default parameters
    default_params = {
        'r': 1.0,   # Prey growth rate
        'K': 10.0,   # Carrying capacity
        'a': 1.0,    # Attack rate
        'h': 0.1,    # Handling time
        'm': 0.5,    # Predator mortality
        'c': 0.5,    # Conversion efficiency
        'd': 0.1     # Predator growth
    }
    
    # Initial conditions
    initial_conditions = [5.0, 2.0]  # [N0, P0]
    
    # Time parameters
    t_max = 100
    num_points = 1000
    
    # GUI layout
    parameter_col = [
        [sg.Text('Prey Parameters')],
        [sg.Text('Growth rate (r):'), sg.Input(default_params['r'], key='-R-', size=(10, 1))],
        [sg.Text('Carrying capacity (K):'), sg.Input(default_params['K'], key='-K-', size=(10, 1))],
        
        [sg.Text('\nPredator Parameters')],
        [sg.Text('Attack rate (a):'), sg.Input(default_params['a'], key='-A-', size=(10, 1))],
        [sg.Text('Handling time (h):'), sg.Input(default_params['h'], key='-H-', size=(10, 1))],
        [sg.Text('Mortality rate (m):'), sg.Input(default_params['m'], key='-M-', size=(10, 1))],
        [sg.Text('Conversion (c):'), sg.Input(default_params['c'], key='-C-', size=(10, 1))],
        [sg.Text('Growth rate (d):'), sg.Input(default_params['d'], key='-D-', size=(10, 1))],
        
        [sg.Text('\nInitial Conditions')],
        [sg.Text('Initial prey (N0):'), sg.Input(initial_conditions[0], key='-N0-', size=(10, 1))],
        [sg.Text('Initial predator (P0):'), sg.Input(initial_conditions[1], key='-P0-', size=(10, 1))],
        
        [sg.Text('\nSimulation Time')],
        [sg.Text('Max time:'), sg.Input(t_max, key='-TMAX-', size=(10, 1))],
        
        [sg.Button('Run Simulation'), sg.Button('Exit')]
    ]
    
    graph_col = [
        [sg.Text('Simulation Results', size=(40, 1), justification='center')],
        [sg.Canvas(key='-CANVAS-')]
    ]
    
    layout = [
        [
            sg.Column(parameter_col),
            sg.VSeperator(),
            sg.Column(graph_col)
        ]
    ]
    
    window = sg.Window('Holling-Tanner Predator-Prey Model', layout, finalize=True)
    
    # Initialize figure
    fig = plt.figure(figsize=(10, 4))
    figure_canvas_agg = draw_figure(window['-CANVAS-'], fig)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event == 'Run Simulation':
            try:
                # Get parameters from GUI
                params = {
                    'r': float(values['-R-']),
                    'K': float(values['-K-']),
                    'a': float(values['-A-']),
                    'h': float(values['-H-']),
                    'm': float(values['-M-']),
                    'c': float(values['-C-']),
                    'd': float(values['-D-'])
                }
                
                initial_conditions = [
                    float(values['-N0-']),
                    float(values['-P0-'])
                ]
                
                t_max = float(values['-TMAX-'])
                t = np.linspace(0, t_max, num_points)
                
                # Run simulation
                model = HollingTannerModel(**params)
                solution = model.simulate(initial_conditions, t)
                
                # Update plot
                fig = create_figure(solution, t)
                figure_canvas_agg = draw_figure(window['-CANVAS-'], fig)
                
            except ValueError as e:
                sg.popup_error(f"Invalid input: {str(e)}")
    
    window.close()

if __name__ == "__main__":
    main()