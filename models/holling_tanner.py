import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
from models.holling_tanner import HollingTannerModel

def draw_figure(element, figure):
    """Draw a matplotlib figure onto a PySimpleGUI Graph element"""
    plt.close('all')  # Clear previous figures
    canv = FigureCanvasTkAgg(figure, element.TKCanvas)
    canv.draw()
    canv.get_tk_widget().pack(side='top', fill='both', expand=1)
    return canv

def create_combined_figure(solution, t):
    """Create a single figure with both subplots"""
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

def main():
    # Default parameters
    default_params = {
        'r': 1.0, 'K': 10.0, 'a': 1.0, 'h': 0.1,
        'm': 0.5, 'c': 0.5, 'd': 0.1
    }
    
    # Layout
    parameter_col = [
        [sg.Text('Prey Parameters', font='Any 12')],
        [sg.Text('Growth rate (r):'), sg.Input(default_params['r'], key='-R-', size=10)],
        [sg.Text('Carrying capacity (K):'), sg.Input(default_params['K'], key='-K-', size=10)],
        
        [sg.Text('\nPredator Parameters', font='Any 12')],
        [sg.Text('Attack rate (a):'), sg.Input(default_params['a'], key='-A-', size=10)],
        [sg.Text('Handling time (h):'), sg.Input(default_params['h'], key='-H-', size=10)],
        [sg.Text('Mortality rate (m):'), sg.Input(default_params['m'], key='-M-', size=10)],
        [sg.Text('Conversion (c):'), sg.Input(default_params['c'], key='-C-', size=10)],
        [sg.Text('Growth rate (d):'), sg.Input(default_params['d'], key='-D-', size=10)],
        
        [sg.Text('\nInitial Conditions', font='Any 12')],
        [sg.Text('Initial prey (N0):'), sg.Input('5.0', key='-N0-', size=10)],
        [sg.Text('Initial predator (P0):'), sg.Input('2.0', key='-P0-', size=10)],
        
        [sg.Text('\nSimulation Time', font='Any 12')],
        [sg.Text('Max time:'), sg.Input('100', key='-TMAX-', size=10)],
        
        [sg.Button('Run Simulation'), sg.Button('Exit')]
    ]
    
    graph_col = [
        [sg.Graph(
            canvas_size=(800, 400),
            graph_bottom_left=(0, 0),
            graph_top_right=(800, 400),
            key='-GRAPH-',
            pad=0,
            enable_events=True,
            background_color='#F0F0F0'
        )]
    ]
    
    layout = [
        [
            sg.Column(parameter_col, vertical_alignment='top'),
            sg.VSeperator(),
            sg.Column(graph_col, expand_x=True, expand_y=True)
        ]
    ]
    
    window = sg.Window(
        'Holling-Tanner Predator-Prey Model',
        layout,
        resizable=True,
        finalize=True,
        size=(1200, 600)
    )
    
    # Initial empty figure
    fig = plt.figure(figsize=(8, 4))
    fig_agg = draw_figure(window['-GRAPH-'], fig)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
            
        if event == 'Run Simulation':
            try:
                # Get parameters
                params = {k: float(values[f'-{k}-']) for k in ['R', 'K', 'A', 'H', 'M', 'C', 'D']}
                initial_conditions = [float(values['-N0-']), float(values['-P0-'])]
                t_max = float(values['-TMAX-'])
                t = np.linspace(0, t_max, 1000)
                
                # Run simulation
                model = HollingTannerModel(**params)
                solution = model.simulate(initial_conditions, t)
                
                # Update figure
                fig = create_combined_figure(solution, t)
                fig_agg = draw_figure(window['-GRAPH-'], fig)
                
            except Exception as e:
                sg.popup_error(f'Error: {str(e)}')
    
    window.close()

if __name__ == "__main__":
    main()