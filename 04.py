import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2, expon, norm, binom, poisson, uniform as sp_uniform
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math

# --- Generadores de Números Pseudoaleatorios ---
def cuadrados_medios(seed, n):
    resultados = []
    x = seed
    longitud_seed = len(str(seed))
    if longitud_seed % 2 != 0:
        print(f"Advertencia: La longitud de la semilla ({longitud_seed}) es impar. Se procederá, pero podría no ser ideal para todos los métodos de cuadrados medios.")
    for _ in range(n):
        x_cuadrado_str = str(x * x).zfill(longitud_seed * 2)
        offset = longitud_seed // 2
        x = int(x_cuadrado_str[offset : offset + longitud_seed])
        resultados.append(x / (10**longitud_seed))
    return resultados

def fibonacci(seed1, seed2, n):
    m_fib = 10000
    resultados = []
    x1, x2 = seed1, seed2
    for _ in range(n):
        x_next = (x1 + x2) % m_fib
        resultados.append(x_next / m_fib)
        x1, x2 = x2, x_next
    return resultados

def congruencial_mixto(x0, a, c, m, n):
    resultados = []
    x = x0
    for _ in range(n):
        x = (a * x + c) % m
        resultados.append(x / m)
    return resultados

def congruencial_multiplicativo(x0, a, m, n):
    resultados = []
    x = x0
    for _ in range(n):
        x = (a * x) % m
        resultados.append(x / m)
    return resultados

def metodo_numeros_indice(p, random_numbers):
    acumulada = np.cumsum(p)
    muestras = []
    for r in random_numbers:
        idx = np.searchsorted(acumulada, r, side='right')
        muestras.append(idx)
    return muestras

def bernoulli(p, random_numbers): # Note: This global function is not directly used by distribution tab after changes
    return [1 if r < p else 0 for r in random_numbers]


class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Multifuncional Mejorado")
        self.root.geometry("1100x750")

        self.current_random_numbers = []
        self.current_distribution_numbers = np.array([]) 
        self.current_custom_discrete_samples = np.array([]) 

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", tabposition='n')
        # ... (rest of style configurations remain the same) ...
        style.configure("TNotebook.Tab", padding=[10, 5], font=('Helvetica', 10, 'bold'))
        style.configure("TFrame", background='#f0f0f0')
        style.configure("TLabel", background='#f0f0f0', font=('Helvetica', 10))
        style.configure("TButton", padding=6, font=('Helvetica', 10, 'bold'), background='#e0e0e0')
        style.map("TButton", background=[('active', '#c0c0c0')])
        style.configure("TEntry", padding=5, font=('Helvetica', 10))
        style.configure("Results.TText", font=('Courier New', 10), background='white', wrap='word', relief='sunken', borderwidth=1)


        self.notebook = ttk.Notebook(root)

        self.create_generator_tab()
        self.create_distribution_tab()
        self.create_custom_discrete_tab()
        self.create_montecarlo_tab()
        self.create_queues_tab()

        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

    def create_input_frame(self, parent, label_text, default_value=""):
        # ... (remains the same) ...
        frame = ttk.Frame(parent, padding=(0,0,0,5))
        label = ttk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT, padx=(0,5))
        entry_var = tk.StringVar(value=default_value)
        entry = ttk.Entry(frame, textvariable=entry_var, width=10)
        entry.pack(side=tk.LEFT)
        return entry_var, entry, frame

    def create_generator_tab(self):
        # ... (remains largely the same, ensures self.current_random_numbers is populated) ...
        tab_main_generators = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_main_generators, text="Generadores RNG")

        gen_frame = ttk.LabelFrame(tab_main_generators, text="Configuración del Generador", padding="10")
        gen_frame.pack(pady=10, padx=10, fill="x")

        self.selected_generator = tk.StringVar(value="Congruencial Mixto")
        generators = ["Congruencial Mixto", "Congruencial Multiplicativo", "Cuadrados Medios", "Fibonacci"]
        gen_cb = ttk.Combobox(gen_frame, textvariable=self.selected_generator, values=generators, state="readonly", width=25)
        gen_cb.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        gen_cb.bind("<<ComboboxSelected>>", self.update_generator_params_visibility)

        self.n_entry_var = tk.StringVar(value="100") # Default 100 for RNG tab
        n_label = ttk.Label(gen_frame, text="Cantidad (n):")
        n_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.n_entry = ttk.Entry(gen_frame, textvariable=self.n_entry_var, width=10)
        self.n_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.params_frames = {}

        frame_cm = ttk.Frame(gen_frame)
        self.seed_cm_var, _, _ = self.create_input_frame(frame_cm, "Semilla (X0):", "12345")
        self.a_cm_var, _, _ = self.create_input_frame(frame_cm, "Constante (a):", "1664525")
        self.c_cm_var, _, _ = self.create_input_frame(frame_cm, "Incremento (c):", "1013904223")
        self.m_cm_var, _, _ = self.create_input_frame(frame_cm, "Módulo (m):", "4294967296")
        for i, child_frame in enumerate(frame_cm.winfo_children()): child_frame.grid(row=i, column=0, sticky="w", padx=5, pady=2)
        self.params_frames["Congruencial Mixto"] = frame_cm
        
        frame_cmu = ttk.Frame(gen_frame)
        self.seed_cmu_var, _, _ = self.create_input_frame(frame_cmu, "Semilla (X0):", "12345")
        self.a_cmu_var, _, _ = self.create_input_frame(frame_cmu, "Constante (a):", "1664525")
        self.m_cmu_var, _, _ = self.create_input_frame(frame_cmu, "Módulo (m):", "4294967296")
        for i, child_frame in enumerate(frame_cmu.winfo_children()): child_frame.grid(row=i, column=0, sticky="w", padx=5, pady=2)
        self.params_frames["Congruencial Multiplicativo"] = frame_cmu

        frame_sq = ttk.Frame(gen_frame)
        self.seed_sq_var, _, _ = self.create_input_frame(frame_sq, "Semilla (X0):", "1234")
        for i, child_frame in enumerate(frame_sq.winfo_children()): child_frame.grid(row=i, column=0, sticky="w", padx=5, pady=2)
        self.params_frames["Cuadrados Medios"] = frame_sq
        
        frame_fib = ttk.Frame(gen_frame)
        self.seed1_fib_var, _, _ = self.create_input_frame(frame_fib, "Semilla 1 (X0):", "1234")
        self.seed2_fib_var, _, _ = self.create_input_frame(frame_fib, "Semilla 2 (X1):", "5678")
        for i, child_frame in enumerate(frame_fib.winfo_children()): child_frame.grid(row=i, column=0, sticky="w", padx=5, pady=2)
        self.params_frames["Fibonacci"] = frame_fib

        for i, frame_name in enumerate(self.params_frames):
            self.params_frames[frame_name].grid(row=2 + i//2, column=i%2, sticky="nsew", padx=10, pady=5)

        self.update_generator_params_visibility()

        generate_button = ttk.Button(gen_frame, text="Generar Números", command=self.run_selected_generator)
        generate_button.grid(row=max(3, 2 + (len(self.params_frames)+1)//2), column=0, columnspan=2, pady=10)

        results_tests_frame = ttk.Frame(tab_main_generators)
        results_tests_frame.pack(pady=10, padx=10, fill="both", expand=True)

        results_frame = ttk.LabelFrame(results_tests_frame, text="Resultados Generados", padding="10")
        results_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0,5))
        
        self.results_text_area = tk.Text(results_frame, height=15, width=40, wrap=tk.WORD, relief='sunken', borderwidth=1, font=('Courier New', 10))
        self.results_text_area.pack(pady=5, padx=5, fill="both", expand=True)
        results_scrollbar = ttk.Scrollbar(self.results_text_area, command=self.results_text_area.yview)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text_area.config(yscrollcommand=results_scrollbar.set)

        tests_frame = ttk.LabelFrame(results_tests_frame, text="Pruebas de Aleatoriedad", padding="10")
        tests_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=(5,0))

        chi_frame = ttk.Frame(tests_frame)
        chi_frame.pack(fill="x", pady=5)
        self.k_chi_var, self.k_chi_entry, k_chi_frame_inner = self.create_input_frame(chi_frame, "Intervalos (k) Chi²:", "10")
        k_chi_frame_inner.pack(fill="x")
        chi_button = ttk.Button(chi_frame, text="Prueba Chi-Cuadrado", command=self.run_chi_cuadrado_test)
        chi_button.pack(pady=5, fill="x")

        ks_button = ttk.Button(tests_frame, text="Prueba Kolmogorov-Smirnov", command=self.run_kolmogorov_smirnov_test)
        ks_button.pack(pady=10, fill="x")
        
        self.test_results_area = tk.Text(tests_frame, height=10, width=50, wrap=tk.WORD, relief='sunken', borderwidth=1, font=('Courier New', 10))
        self.test_results_area.pack(pady=5, padx=5, fill="both", expand=True)
        test_results_scrollbar = ttk.Scrollbar(self.test_results_area, command=self.test_results_area.yview)
        test_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.test_results_area.config(yscrollcommand=test_results_scrollbar.set)

        plot_button = ttk.Button(results_frame, text="Mostrar Gráfico de Dispersión", command=self.plot_generated_numbers)
        plot_button.pack(pady=10)

    def update_generator_params_visibility(self, event=None):
        # ... (remains the same) ...
        selected = self.selected_generator.get()
        for name, frame in self.params_frames.items():
            if name == selected:
                frame.grid() 
            else:
                frame.grid_remove() 

    def run_selected_generator(self):
        # ... (remains the same) ...
        generator_name = self.selected_generator.get()
        try:
            n = int(self.n_entry_var.get())
            if n <= 0:
                messagebox.showerror("Error", "La cantidad (n) debe ser un entero positivo.")
                return
            if generator_name == "Congruencial Mixto":
                x0 = int(self.seed_cm_var.get())
                a = int(self.a_cm_var.get())
                c = int(self.c_cm_var.get())
                m = int(self.m_cm_var.get())
                if not (0 <= x0 < m and 0 <= a < m and 0 <= c < m and m > 0):
                     messagebox.showerror("Error", "Parámetros inválidos para CM. Deben ser >= 0 y < m (excepto m > 0).")
                     return
                self.current_random_numbers = congruencial_mixto(x0, a, c, m, n)
            elif generator_name == "Congruencial Multiplicativo":
                x0 = int(self.seed_cmu_var.get())
                a = int(self.a_cmu_var.get())
                m = int(self.m_cmu_var.get())
                if not (0 < x0 < m and 0 < a < m and m > 0):
                     messagebox.showerror("Error", "Parámetros inválidos para CMu. Deben ser > 0 y < m (excepto m > 0).")
                     return
                self.current_random_numbers = congruencial_multiplicativo(x0, a, m, n)
            elif generator_name == "Cuadrados Medios":
                x0 = int(self.seed_sq_var.get())
                if len(str(x0)) < 3 or len(str(x0)) > 6: 
                     messagebox.showerror("Error", "La semilla para Cuadrados Medios debe tener entre 3 y 6 dígitos.")
                     return
                self.current_random_numbers = cuadrados_medios(x0, n)
            elif generator_name == "Fibonacci":
                x0 = int(self.seed1_fib_var.get())
                x1 = int(self.seed2_fib_var.get())
                self.current_random_numbers = fibonacci(x0, x1, n)
            self.display_results(self.current_random_numbers, self.results_text_area)
            self.test_results_area.delete('1.0', tk.END)
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos para los parámetros.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    def display_results(self, numbers, text_widget):
        # ... (remains the same) ...
        text_widget.delete('1.0', tk.END)
        if not numbers: 
            text_widget.insert(tk.END, "No se generaron números.")
            return
        text_widget.insert(tk.END, f"Primeros {min(len(numbers), 100)} números generados (de {len(numbers)}):\n")
        for i, num in enumerate(numbers[:100]):
            text_widget.insert(tk.END, f"{num:.4f}\n")
        if len(numbers) > 100:
            text_widget.insert(tk.END, "...\n")
        
        if hasattr(self, 'current_random_numbers') and self.current_random_numbers:
            stats_text = f"\n--- Estadísticas Básicas ---\n"
            stats_text += f"Cantidad: {len(self.current_random_numbers)}\n"
            stats_text += f"Mínimo: {np.min(self.current_random_numbers):.4f}\n"
            stats_text += f"Máximo: {np.max(self.current_random_numbers):.4f}\n"
            stats_text += f"Media: {np.mean(self.current_random_numbers):.4f}\n"
            stats_text += f"Varianza: {np.var(self.current_random_numbers):.4f}\n"
            text_widget.insert(tk.END, stats_text)

    def plot_generated_numbers(self):
        # ... (remains the same) ...
        if not self.current_random_numbers: 
            messagebox.showinfo("Información", "Primero genere números para mostrar el gráfico.")
            return
        fig, ax = plt.subplots()
        ax.scatter(range(len(self.current_random_numbers)), self.current_random_numbers, alpha=0.6, s=10)
        ax.set_title('Gráfico de Dispersión de Números Generados')
        ax.set_xlabel('Índice')
        ax.set_ylabel('Valor Aleatorio')
        ax.grid(True)
        self.show_plot(fig, "Gráfico de Dispersión")

    def run_chi_cuadrado_test(self):
        # ... (remains the same) ...
        if not self.current_random_numbers: 
            messagebox.showerror("Error", "Primero genere números aleatorios.")
            return
        try:
            k = int(self.k_chi_var.get())
            if k <= 0:
                messagebox.showerror("Error", "El número de intervalos (k) debe ser positivo.")
                return

            N = len(self.current_random_numbers)
            observed_freq, bins = np.histogram(self.current_random_numbers, bins=k, range=(0,1))
            expected_freq_per_bin = N / k
            
            valid_bins = expected_freq_per_bin > 0
            observed_freq_valid = observed_freq[valid_bins]
            expected_freq_per_bin_valid = np.full_like(observed_freq_valid, expected_freq_per_bin, dtype=float)

            if expected_freq_per_bin == 0: 
                messagebox.showerror("Error", "La frecuencia esperada por intervalo es cero. Verifique N y k.")
                return

            chi_cuadrado_calculado = np.sum((observed_freq_valid - expected_freq_per_bin_valid)**2 / expected_freq_per_bin_valid)
            
            df = k - 1 
            if df <= 0: 
                 messagebox.showerror("Error", "Grados de libertad deben ser > 0. Aumente k.")
                 return

            p_valor = 1 - chi2.cdf(chi_cuadrado_calculado, df)
            alpha_tipico = 0.05
            chi_critico = chi2.ppf(1 - alpha_tipico, df)

            result_text = f"--- Prueba Chi-Cuadrado (Uniformidad) ---\n"
            result_text += f"Intervalos (k): {k}\n"
            result_text += f"Frecuencia Esperada (Ei) por intervalo: {expected_freq_per_bin:.2f}\n"
            result_text += f"Frecuencias Observadas (Oi): {observed_freq}\n"
            result_text += f"Estadístico Chi-Cuadrado (χ² calculado): {chi_cuadrado_calculado:.4f}\n"
            result_text += f"Grados de Libertad (gl): {df}\n"
            result_text += f"Valor p: {p_valor:.4f}\n"
            result_text += f"Chi-Cuadrado Crítico (α=0.05): {chi_critico:.4f}\n\n"

            if p_valor >= alpha_tipico:
                result_text += f"Conclusión: No se rechaza H0 (p-valor >= {alpha_tipico}).\n"
                result_text += "Los números parecen seguir una distribución uniforme.\n"
            else:
                result_text += f"Conclusión: Se rechaza H0 (p-valor < {alpha_tipico}).\n"
                result_text += "Los números NO parecen seguir una distribución uniforme.\n"
            
            self.test_results_area.delete('1.0', tk.END)
            self.test_results_area.insert(tk.END, result_text)

        except ValueError:
            messagebox.showerror("Error de Entrada", "Ingrese un valor numérico válido para k.")
        except Exception as e:
            messagebox.showerror("Error en Prueba", f"Ocurrió un error: {e}")

    def run_kolmogorov_smirnov_test(self):
        # ... (remains the same) ...
        if not self.current_random_numbers: 
            messagebox.showerror("Error", "Primero genere números aleatorios.")
            return
        try:
            N = len(self.current_random_numbers)
            if N == 0:
                messagebox.showerror("Error", "No hay números para probar.")
                return

            from scipy.stats import kstest 
            ks_statistic, p_valor = kstest(self.current_random_numbers, 'uniform') 
            
            alpha_ks = 0.05
            result_text = f"--- Prueba Kolmogorov-Smirnov (Uniformidad) ---\n"
            result_text += f"Cantidad de números (N): {N}\n"
            result_text += f"Estadístico D (kstest): {ks_statistic:.4f}\n" 
            result_text += f"Valor p (kstest): {p_valor:.4f}\n\n" 

            if p_valor >= alpha_ks:
                result_text += f"Conclusión: No se rechaza H0 (p-valor >= {alpha_ks}).\n"
                result_text += "Los números parecen seguir una distribución uniforme.\n"
            else:
                result_text += f"Conclusión: Se rechaza H0 (p-valor < {alpha_ks}).\n"
                result_text += "Los números NO parecen seguir una distribución uniforme.\n"
            
            self.test_results_area.delete('1.0', tk.END)
            self.test_results_area.insert(tk.END, result_text)
        except Exception as e:
            messagebox.showerror("Error en Prueba K-S", f"Ocurrió un error: {e}")

    # --- MODIFICATIONS for Distribution Tab ---
    def create_distribution_tab(self):
        # ... (UI structure remains similar, button text might change if needed) ...
        tab_dist = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_dist, text="Distribuciones de Probabilidad")

        dist_config_frame = ttk.LabelFrame(tab_dist, text="Generar Variables Aleatorias (Usando RNG de Tab 1)", padding="10")
        dist_config_frame.pack(pady=10, padx=10, fill="x")

        self.selected_distribution_var = tk.StringVar(value="Exponencial")
        distributions = ["Exponencial", "Normal", "Binomial", "Poisson", "Uniforme (continua)", "Bernoulli"]
        dist_cb = ttk.Combobox(dist_config_frame, textvariable=self.selected_distribution_var, values=distributions, state="readonly", width=25)
        dist_cb.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        dist_cb.bind("<<ComboboxSelected>>", self.update_dist_params_visibility)

        self.n_dist_var, self.n_dist_entry, n_dist_frame = self.create_input_frame(dist_config_frame, "Cantidad (n - de Tab 1):", "100")
        n_dist_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.dist_params_frames = {}
        self.dist_param_labels = {}
        self.dist_param_entries_var = {}

        frame_exp = ttk.Frame(dist_config_frame)
        self.dist_param_labels["Exponencial"] = [ttk.Label(frame_exp, text="Escala (β):")]
        self.dist_param_entries_var["Exponencial"] = [tk.StringVar(value="1.0")]
        exp_entry1 = ttk.Entry(frame_exp, textvariable=self.dist_param_entries_var["Exponencial"][0], width=10)
        self.dist_param_labels["Exponencial"][0].grid(row=0, column=0, padx=5, pady=2, sticky="w")
        exp_entry1.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.dist_params_frames["Exponencial"] = frame_exp

        frame_norm = ttk.Frame(dist_config_frame)
        self.dist_param_labels["Normal"] = [ttk.Label(frame_norm, text="Media (μ):"), ttk.Label(frame_norm, text="Desv. Estándar (σ):")]
        self.dist_param_entries_var["Normal"] = [tk.StringVar(value="0.0"), tk.StringVar(value="1.0")]
        norm_entry1 = ttk.Entry(frame_norm, textvariable=self.dist_param_entries_var["Normal"][0], width=10)
        norm_entry2 = ttk.Entry(frame_norm, textvariable=self.dist_param_entries_var["Normal"][1], width=10)
        self.dist_param_labels["Normal"][0].grid(row=0, column=0, padx=5, pady=2, sticky="w")
        norm_entry1.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.dist_param_labels["Normal"][1].grid(row=1, column=0, padx=5, pady=2, sticky="w")
        norm_entry2.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.dist_params_frames["Normal"] = frame_norm

        frame_binom = ttk.Frame(dist_config_frame)
        self.dist_param_labels["Binomial"] = [ttk.Label(frame_binom, text="Ensayos (n_b):"), ttk.Label(frame_binom, text="Probabilidad (p):")]
        self.dist_param_entries_var["Binomial"] = [tk.StringVar(value="10"), tk.StringVar(value="0.5")]
        binom_entry1 = ttk.Entry(frame_binom, textvariable=self.dist_param_entries_var["Binomial"][0], width=10)
        binom_entry2 = ttk.Entry(frame_binom, textvariable=self.dist_param_entries_var["Binomial"][1], width=10)
        self.dist_param_labels["Binomial"][0].grid(row=0, column=0, padx=5, pady=2, sticky="w")
        binom_entry1.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.dist_param_labels["Binomial"][1].grid(row=1, column=0, padx=5, pady=2, sticky="w")
        binom_entry2.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.dist_params_frames["Binomial"] = frame_binom
        
        frame_poisson = ttk.Frame(dist_config_frame)
        self.dist_param_labels["Poisson"] = [ttk.Label(frame_poisson, text="Tasa (λ o μ):")]
        self.dist_param_entries_var["Poisson"] = [tk.StringVar(value="3.0")]
        poisson_entry1 = ttk.Entry(frame_poisson, textvariable=self.dist_param_entries_var["Poisson"][0], width=10)
        self.dist_param_labels["Poisson"][0].grid(row=0, column=0, padx=5, pady=2, sticky="w")
        poisson_entry1.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.dist_params_frames["Poisson"] = frame_poisson

        frame_unif = ttk.Frame(dist_config_frame)
        self.dist_param_labels["Uniforme (continua)"] = [ttk.Label(frame_unif, text="Mínimo (a):"), ttk.Label(frame_unif, text="Máximo (b):")]
        self.dist_param_entries_var["Uniforme (continua)"] = [tk.StringVar(value="0.0"), tk.StringVar(value="1.0")]
        unif_entry1 = ttk.Entry(frame_unif, textvariable=self.dist_param_entries_var["Uniforme (continua)"][0], width=10)
        unif_entry2 = ttk.Entry(frame_unif, textvariable=self.dist_param_entries_var["Uniforme (continua)"][1], width=10)
        self.dist_param_labels["Uniforme (continua)"][0].grid(row=0, column=0, padx=5, pady=2, sticky="w")
        unif_entry1.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.dist_param_labels["Uniforme (continua)"][1].grid(row=1, column=0, padx=5, pady=2, sticky="w")
        unif_entry2.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.dist_params_frames["Uniforme (continua)"] = frame_unif
        
        frame_bern = ttk.Frame(dist_config_frame)
        self.dist_param_labels["Bernoulli"] = [ttk.Label(frame_bern, text="Probabilidad (p):")]
        self.dist_param_entries_var["Bernoulli"] = [tk.StringVar(value="0.5")]
        bern_entry1 = ttk.Entry(frame_bern, textvariable=self.dist_param_entries_var["Bernoulli"][0], width=10)
        self.dist_param_labels["Bernoulli"][0].grid(row=0, column=0, padx=5, pady=2, sticky="w")
        bern_entry1.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.dist_params_frames["Bernoulli"] = frame_bern

        for name, frame in self.dist_params_frames.items():
            frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.update_dist_params_visibility()

        generate_dist_button = ttk.Button(dist_config_frame, text="Generar y Probar Distribución (desde Tab 1)", command=self.generar_y_probar_distribucion)
        generate_dist_button.grid(row=3, column=0, columnspan=2, pady=10)

        dist_results_frame = ttk.LabelFrame(tab_dist, text="Resultados y Prueba de Ajuste", padding="10")
        dist_results_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.dist_results_text_area = tk.Text(dist_results_frame, height=15, width=50, wrap=tk.WORD, relief='sunken', borderwidth=1, font=('Courier New', 10))
        self.dist_results_text_area.pack(pady=5, padx=5, fill="both", expand=True)
        dist_results_scrollbar = ttk.Scrollbar(self.dist_results_text_area, command=self.dist_results_text_area.yview)
        dist_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dist_results_text_area.config(yscrollcommand=dist_results_scrollbar.set)

        plot_dist_button = ttk.Button(dist_results_frame, text="Mostrar Histograma/Gráfico de Barras", command=self.plot_distribution_histogram) 
        plot_dist_button.pack(pady=10, side=tk.BOTTOM)


    def update_dist_params_visibility(self, event=None):
        # ... (remains the same) ...
        selected = self.selected_distribution_var.get()
        for name, frame in self.dist_params_frames.items():
            if name == selected:
                frame.grid()
            else:
                frame.grid_remove()

    def generar_y_probar_distribucion(self):
        try:
            n_dist_str = self.n_dist_var.get()
            dist_name = self.selected_distribution_var.get()
            params_values_str = [var.get() for var in self.dist_param_entries_var[dist_name]]

            if not self.current_random_numbers:
                messagebox.showerror("Error", "Primero genere números en la pestaña 'Generadores RNG'.")
                self.current_distribution_numbers = np.array([])
                self.display_results_dist(self.current_distribution_numbers, dist_name, [])
                return
            
            try:
                n_dist = int(n_dist_str)
                if n_dist <= 0:
                    messagebox.showerror("Error", "La cantidad (n) debe ser un entero positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error de Entrada", "Cantidad (n) inválida.")
                return

            available_rng_count = len(self.current_random_numbers)
            actual_n_to_use = n_dist

            if n_dist > available_rng_count:
                messagebox.showwarning("Advertencia",
                                       f"La cantidad solicitada ({n_dist}) excede los números RNG disponibles ({available_rng_count}).\n"
                                       f"Se usarán los primeros {available_rng_count} números RNG.")
                actual_n_to_use = available_rng_count
            
            if actual_n_to_use == 0:
                messagebox.showinfo("Información", "No hay números RNG para usar (0 especificado o 0 disponible).")
                self.current_distribution_numbers = np.array([])
                self.display_results_dist(self.current_distribution_numbers, dist_name, [])
                return

            uniform_samples = np.array(self.current_random_numbers[:actual_n_to_use])
            # Ensure samples are in (0, 1) for some ppf functions if they are strict,
            # or handle 0 and 1 if ppf might fail (e.g. log(0)).
            # Scipy ppf functions generally handle u in [0,1] appropriately.
            # For log transformations, we need to be careful if u=0 or u=1.
            # For expon.ppf(u) = -scale * log(1-u), if u=1, log(0) is -inf. Max to avoid this.
            uniform_samples_for_ppf = np.clip(uniform_samples, 1e-9, 1.0 - 1e-9) # Clip to avoid exact 0 or 1 for robustness


            params_values = [float(p_str) for p_str in params_values_str]
            generated_variates = []

            if dist_name == "Exponencial":
                beta = params_values[0]
                if beta <= 0: messagebox.showerror("Error", "Parámetro beta (escala) debe ser > 0."); return
                # X = -beta * np.log(1 - uniform_samples_for_ppf) # Manual inverse transform
                generated_variates = expon.ppf(uniform_samples_for_ppf, scale=beta)
            elif dist_name == "Normal":
                mu, sigma = params_values[0], params_values[1]
                if sigma <= 0: messagebox.showerror("Error", "Desviación estándar (sigma) debe ser > 0."); return
                generated_variates = norm.ppf(uniform_samples_for_ppf, loc=mu, scale=sigma)
            elif dist_name == "Binomial": 
                n_binom, p_binom = int(params_values[0]), params_values[1]
                if not (0 <= p_binom <= 1 and n_binom > 0 and isinstance(n_binom, int)): messagebox.showerror("Error", "Parámetros Binomial: 0<=p<=1, n_ensayos (entero) >0."); return
                generated_variates = binom.ppf(uniform_samples_for_ppf, n=n_binom, p=p_binom)
            elif dist_name == "Poisson":
                lam = params_values[0]
                if lam <= 0: messagebox.showerror("Error", "Parámetro lambda (tasa) debe ser > 0."); return
                generated_variates = poisson.ppf(uniform_samples_for_ppf, mu=lam)
            elif dist_name == "Uniforme (continua)":
                low, high = params_values[0], params_values[1]
                if low >= high: messagebox.showerror("Error", "Para Uniforme, mínimo (a) debe ser menor que máximo (b)."); return
                # X = low + (high - low) * uniform_samples # Manual
                generated_variates = sp_uniform.ppf(uniform_samples_for_ppf, loc=low, scale=(high - low))
            elif dist_name == "Bernoulli":
                p_bern = params_values[0]
                if not (0 <= p_bern <= 1): messagebox.showerror("Error", "Parámetro Bernoulli (p) debe estar entre 0 y 1."); return
                # generated_variates = (uniform_samples < p_bern).astype(int) # Manual
                generated_variates = binom.ppf(uniform_samples_for_ppf, n=1, p=p_bern)
            else:
                messagebox.showerror("Error", "Distribución no implementada para generación desde Tab 1.")
                return

            self.current_distribution_numbers = np.array(generated_variates)
            self.display_results_dist(self.current_distribution_numbers, dist_name, params_values)
            self.realizar_prueba_chi_cuadrado_distribucion(dist_name, params_values)
            self.dist_results_text_area.insert('1.0', f"Usando los primeros {actual_n_to_use} números de la pestaña 'Generadores RNG'.\n---\n")


        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos para los parámetros y cantidad.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error en la generación de distribución: {e}")
            import traceback
            traceback.print_exc()


    def display_results_dist(self, numbers, dist_name, params_values):
        # ... (remains the same) ...
        self.dist_results_text_area.delete('1.0', tk.END)
        if not isinstance(numbers, np.ndarray):
            numbers = np.array(numbers)

        if not numbers.size: 
            self.dist_results_text_area.insert(tk.END, "No se generaron números.")
            # Display defined params even if no numbers
            if params_values:
                param_str = ", ".join(map(str, params_values))
                self.dist_results_text_area.insert(tk.END, f"\nDistribución seleccionada: {dist_name}\nParámetros definidos: {param_str}\n")
            return
        
        param_str = ", ".join(map(str, params_values))
        self.dist_results_text_area.insert(tk.END, f"Distribución: {dist_name}\nParámetros: {param_str}\n") 
        self.dist_results_text_area.insert(tk.END, f"Primeros {min(len(numbers), 20)} números generados (de {len(numbers)}):\n")
        for i, num in enumerate(numbers[:20]):
            if isinstance(num, float):
                self.dist_results_text_area.insert(tk.END, f"{num:.4f}\n")
            else: 
                self.dist_results_text_area.insert(tk.END, f"{num}\n")

        if len(numbers) > 20:
            self.dist_results_text_area.insert(tk.END, "...\n")
        
        stats_text = f"\n--- Estadísticas Básicas de los Datos Generados ---\n"
        stats_text += f"Cantidad: {len(numbers)}\n"
        stats_text += f"Mínimo: {np.min(numbers):.4f}\n"
        stats_text += f"Máximo: {np.max(numbers):.4f}\n"
        stats_text += f"Media: {np.mean(numbers):.4f}\n" 
        stats_text += f"Varianza: {np.var(numbers):.4f}\n" 
        self.dist_results_text_area.insert(tk.END, stats_text)


    def realizar_prueba_chi_cuadrado_distribucion(self, dist_name, params_values):
        # ... (remains the same) ...
        if not self.current_distribution_numbers.any():
            return
        
        N = len(self.current_distribution_numbers)
        k_sugerido = int(self.k_chi_var.get()) if self.k_chi_var.get().isdigit() and int(self.k_chi_var.get()) > 0 else max(5, int(N**0.4)) 

        m_params_estimados = 0 
        
        if dist_name == "Bernoulli":
            p_param = params_values[0]
            observed_1 = np.sum(self.current_distribution_numbers == 1)
            observed_0 = N - observed_1
            observed_freq = np.array([observed_0, observed_1])
            
            expected_1 = N * p_param
            expected_0 = N * (1 - p_param)
            expected_freq = np.array([expected_0, expected_1])
            
            k_actual = 2 
            m_params_estimados = 0 
            df = k_actual - 1 - m_params_estimados
            
            if np.any(expected_freq < 1e-9): 
                 self.dist_results_text_area.insert(tk.END, "\nAdvertencia: Frecuencia esperada es cero para una categoría. Chi² no aplicable.\n")
                 return
            if np.any(expected_freq < 5):
                self.dist_results_text_area.insert(tk.END, "\nAdvertencia: Alguna frecuencia esperada es < 5. La prueba Chi² puede ser menos precisa.\n")

        elif dist_name in ["Binomial", "Poisson"]: 
            unique_vals = np.unique(self.current_distribution_numbers)
            
            if len(unique_vals) <= k_sugerido + 5 : 
                observed_freq = np.array([np.sum(self.current_distribution_numbers == val) for val in unique_vals])
                k_actual = len(unique_vals)
                
                expected_freq = np.zeros(k_actual)
                if dist_name == "Binomial":
                    n_b, p_b = int(params_values[0]), params_values[1]
                    scipy_dist = binom(n=n_b, p=p_b)
                    for i, val in enumerate(unique_vals):
                        expected_freq[i] = N * scipy_dist.pmf(val)
                elif dist_name == "Poisson":
                    lam = params_values[0]
                    scipy_dist = poisson(mu=lam)
                    for i, val in enumerate(unique_vals):
                        expected_freq[i] = N * scipy_dist.pmf(val)
                m_params_estimados = 0 
                df = k_actual - 1 - m_params_estimados

            else: 
                min_val = np.min(self.current_distribution_numbers)
                max_val = np.max(self.current_distribution_numbers)
                bin_edges = np.linspace(min_val - 0.5, max_val + 0.5, k_sugerido + 1)
                observed_freq, _ = np.histogram(self.current_distribution_numbers, bins=bin_edges)
                k_actual = k_sugerido 
                
                expected_freq = np.zeros(k_actual)
                if dist_name == "Binomial":
                    n_b, p_b = int(params_values[0]), params_values[1]
                    scipy_dist = binom(n=n_b, p=p_b)
                elif dist_name == "Poisson":
                    lam = params_values[0]
                    scipy_dist = poisson(mu=lam)

                for i in range(k_actual):
                    p_intervalo = scipy_dist.cdf(bin_edges[i+1] - 0.5) - scipy_dist.cdf(bin_edges[i] -0.5) 
                    if i == 0 : p_intervalo = scipy_dist.cdf(bin_edges[i+1] -0.5)
                    expected_freq[i] = N * p_intervalo
                m_params_estimados = 0
                df = k_actual - 1 - m_params_estimados
            
            if np.any(expected_freq < 5):
                 self.dist_results_text_area.insert(tk.END, "\nAdvertencia: Algunas frecuencias esperadas son < 5. La prueba Chi² puede ser menos precisa.\nConsidere agrupar intervalos, aumentar N, o verificar la elección de k.\n")

        else: 
            min_val = np.min(self.current_distribution_numbers)
            max_val = np.max(self.current_distribution_numbers)
            observed_freq, bin_edges = np.histogram(self.current_distribution_numbers, bins=k_sugerido, range=(min_val,max_val))
            k_actual = k_sugerido
            
            expected_freq = np.zeros(k_actual)
            scipy_dist = None
            if dist_name == "Exponencial":
                beta = params_values[0]
                scipy_dist = expon(scale=beta)
            elif dist_name == "Normal":
                mu, sigma = params_values[0], params_values[1]
                scipy_dist = norm(loc=mu, scale=sigma)
            elif dist_name == "Uniforme (continua)":
                low, high = params_values[0], params_values[1]
                scipy_dist = sp_uniform(loc=low, scale=(high - low)) 

            if scipy_dist:
                for i in range(k_actual):
                    p_intervalo = scipy_dist.cdf(bin_edges[i+1]) - scipy_dist.cdf(bin_edges[i])
                    expected_freq[i] = N * p_intervalo
            
            if np.any(expected_freq < 5):
                self.dist_results_text_area.insert(tk.END, "\nAdvertencia: Algunas frecuencias esperadas son < 5. La prueba Chi² puede ser menos precisa.\nConsidere agrupar intervalos o aumentar N.\n")
            
            m_params_estimados = 0 
            df = k_actual - 1 - m_params_estimados

        valid_indices = expected_freq > 1e-9 
        observed_freq_adj = observed_freq[valid_indices]
        expected_freq_adj = expected_freq[valid_indices]

        if len(expected_freq_adj) == 0 or np.sum(expected_freq_adj) == 0 or len(observed_freq_adj) != len(expected_freq_adj):
            self.dist_results_text_area.insert(tk.END, "\nError: Frecuencias inválidas para la prueba Chi². No se puede realizar.\n")
            return
        
        df_final = len(expected_freq_adj) - 1 - m_params_estimados 
        if df_final <= 0:
            self.dist_results_text_area.insert(tk.END, f"\nError: Grados de libertad ({df_final}) no son positivos después de ajustar bins. Revise k, parámetros o datos.\n")
            return

        chi_cuadrado_calculado = np.sum((observed_freq_adj - expected_freq_adj) ** 2 / expected_freq_adj)
        p_valor = 1 - chi2.cdf(chi_cuadrado_calculado, df_final)
        alpha_tipico = 0.05

        result_text = f"\n--- Prueba Chi-Cuadrado de Ajuste ({dist_name}) ---\n"
        result_text += f"Categorías/Intervalos (k usados): {len(expected_freq_adj)}\n"
        result_text += f"Frec. Observadas (Oi): {observed_freq_adj.astype(int)}\n"
        result_text += f"Frec. Esperadas (Ei): {[float(f'{x:.2f}') for x in expected_freq_adj]}\n"
        result_text += f"Estadístico Chi-Cuadrado (χ² calculado): {chi_cuadrado_calculado:.4f}\n"
        result_text += f"Grados de Libertad (gl): {df_final}\n"
        result_text += f"Valor p: {p_valor:.4f}\n\n"

        if p_valor >= alpha_tipico:
            result_text += f"Conclusión: No se rechaza H0 (p-valor >= {alpha_tipico}).\n"
            result_text += f"Los datos parecen ajustarse a una distribución {dist_name} con los parámetros dados.\n"
        else:
            result_text += f"Conclusión: Se rechaza H0 (p-valor < {alpha_tipico}).\n"
            result_text += f"Los datos NO parecen ajustarse a una distribución {dist_name} con los parámetros dados.\n"

        self.dist_results_text_area.insert(tk.END, result_text)


    def plot_distribution_histogram(self):
        # ... (remains the same) ...
        if not self.current_distribution_numbers.any(): 
            messagebox.showinfo("Información", "Primero genere números de la distribución.")
            return

        fig, ax = plt.subplots()
        dist_name = self.selected_distribution_var.get()
        data_to_plot = self.current_distribution_numbers
        
        params_values = [float(var.get()) for var in self.dist_param_entries_var[dist_name]]

        if dist_name == "Bernoulli":
            p_bern = params_values[0]
            observed_counts = np.bincount(data_to_plot.astype(int), minlength=2) 
            ax.bar([0, 1], observed_counts / len(data_to_plot), width=0.4, alpha=0.7, label='Frec. Observada', edgecolor='black')
            x_discrete = np.array([0, 1])
            pmf_values = binom.pmf(x_discrete, n=1, p=p_bern)
            ax.stem(x_discrete, pmf_values, linefmt='r-', markerfmt='ro', basefmt=" ", label=f'Bernoulli Teórica (PMF) p={p_bern}')
            ax.set_xticks([0, 1])
            ax.set_ylabel('Probabilidad / Frecuencia Relativa')
        
        elif dist_name in ["Binomial", "Poisson"]: 
            min_val = int(np.min(data_to_plot))
            max_val = int(np.max(data_to_plot))
            bins = np.arange(min_val, max_val + 2) - 0.5 
            ax.hist(data_to_plot, bins=bins, density=True, alpha=0.7, label='Datos Generados', edgecolor='black')
            
            x_discrete = np.arange(min_val, max_val + 1)
            pmf_values = None
            if dist_name == "Binomial":
                 n_b, p_b = int(params_values[0]), params_values[1]
                 pmf_values = binom.pmf(x_discrete, n=n_b, p=p_b)
                 ax.plot(x_discrete, pmf_values, 'ro-', label=f'{dist_name} Teórica (PMF)')
            elif dist_name == "Poisson":
                 lam = params_values[0]
                 pmf_values = poisson.pmf(x_discrete, mu=lam)
                 ax.plot(x_discrete, pmf_values, 'ro-', label=f'{dist_name} Teórica (PMF)')
            ax.set_ylabel('Densidad / Probabilidad')

        else: 
            bins = 'auto' 
            ax.hist(data_to_plot, bins=bins, density=True, alpha=0.7, label='Datos Generados', edgecolor='black')
            
            x_plot = np.linspace(np.min(data_to_plot), np.max(data_to_plot), 200)
            pdf_values = None
            try:
                if dist_name == "Exponencial":
                    pdf_values = expon.pdf(x_plot, scale=params_values[0])
                elif dist_name == "Normal":
                    pdf_values = norm.pdf(x_plot, loc=params_values[0], scale=params_values[1])
                elif dist_name == "Uniforme (continua)":
                     pdf_values = sp_uniform.pdf(x_plot, loc=params_values[0], scale=(params_values[1]-params_values[0]))
                
                if pdf_values is not None:
                     ax.plot(x_plot, pdf_values, 'r-', lw=2, label=f'{dist_name} Teórica (PDF)')
            except Exception as e:
                print(f"No se pudo graficar PDF teórica para {dist_name}: {e}")
            ax.set_ylabel('Densidad')

        ax.set_title(f'Histograma/Gráfico de Barras de Distribución {dist_name}')
        ax.set_xlabel('Valor')
        ax.legend()
        ax.grid(True)
        self.show_plot(fig, f"Gráfico {dist_name}")


    def create_custom_discrete_tab(self):
        # ... (This tab's functionality to use Tab 1 RNG is already established from previous turn,
        # including default values for the newspaper exercise and the sequence plot button) ...
        tab_custom = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_custom, text="Variables Discretas Personalizadas")

        frame_input = ttk.LabelFrame(tab_custom, text="Defina la Variable Aleatoria Discreta", padding="10")
        frame_input.pack(padx=10, pady=10, fill="x")

        default_demand_values = "20,21,22,23,24,25,26,27,28,29,30"
        default_demand_probs = "0.05,0.05,0.10,0.10,0.10,0.15,0.15,0.10,0.10,0.05,0.05"

        ttk.Label(frame_input, text="Valores (Demandas, separados por coma):").grid(row=0,column=0, sticky="w", pady=(0,2))
        self.values_var = tk.StringVar(value=default_demand_values) 
        values_entry = ttk.Entry(frame_input, textvariable=self.values_var, width=50)
        values_entry.grid(row=0,column=1, sticky="we", padx=5, pady=(0,2)) 

        ttk.Label(frame_input, text="Probabilidades (separadas por coma):").grid(row=1,column=0, sticky="w", pady=(0,2))
        self.probs_var = tk.StringVar(value=default_demand_probs) 
        probs_entry = ttk.Entry(frame_input, textvariable=self.probs_var, width=50)
        probs_entry.grid(row=1,column=1, sticky="we", padx=5, pady=(0,2)) 

        self.n_demandas_var = tk.StringVar(value="60") 
        ttk.Label(frame_input, text="Cantidad de demandas (usar de RNG):").grid(row=2,column=0, sticky="w", pady=(5,2))
        n_demandas_entry = ttk.Entry(frame_input, textvariable=self.n_demandas_var, width=10)
        n_demandas_entry.grid(row=2,column=1, sticky="w", padx=5, pady=(5,2)) 

        frame_input.columnconfigure(1, weight=1) 

        generate_button = ttk.Button(frame_input, text="Generar Muestra Usando Números de RNG Tab", command=self.generar_muestra_artificial)
        generate_button.grid(row=3, column=0, columnspan=2, pady=10) 

        results_frame = ttk.LabelFrame(tab_custom, text="Muestra Generada y Estadísticas", padding="10")
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.custom_samples_text_area = tk.Text(results_frame, height=15, width=70, wrap=tk.WORD, relief='sunken', borderwidth=1, font=('Courier New', 10))
        self.custom_samples_text_area.pack(pady=5, padx=5, fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self.custom_samples_text_area, command=self.custom_samples_text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.custom_samples_text_area.config(yscrollcommand=scrollbar.set)

        plot_freq_button = ttk.Button(results_frame, text="Mostrar Gráfico de Frecuencias", command=self.plot_custom_sample_frequencies)
        plot_freq_button.pack(pady=(10,2), side=tk.TOP, fill=tk.X) 

        plot_sequence_button = ttk.Button(results_frame, text="Graficar Ventas Diarias (Secuencia)", command=self.plot_daily_sales_sequence)
        plot_sequence_button.pack(pady=(2,5), side=tk.TOP, fill=tk.X)

    def generar_muestra_artificial(self):
        # ... (This method is already correctly using Tab 1 RNG and metodo_numeros_indice) ...
        try:
            values_str = self.values_var.get()
            probs_str = self.probs_var.get()
            n_demandas_str = self.n_demandas_var.get() 

            values = [float(v.strip()) for v in values_str.split(',')]
            probs = [float(p.strip()) for p in probs_str.split(',')]

            if len(values) != len(probs):
                messagebox.showerror("Error", "El número de valores y probabilidades debe coincidir.")
                return
            
            if not all(p >= 0 for p in probs):
                messagebox.showerror("Error", "Todas las probabilidades deben ser no negativas.")
                return

            sum_probs = sum(probs)
            if not math.isclose(sum_probs, 1.0, rel_tol=1e-6): 
                messagebox.showerror("Error", f"La suma de las probabilidades debe ser 1.0. Actualmente es {sum_probs:.6f}")
                return

            if not self.current_random_numbers: 
                messagebox.showerror("Error", "Primero genere números en la pestaña 'Generadores RNG'.\nEstos números se usarán para generar la muestra discreta personalizada.")
                self.current_custom_discrete_samples = np.array([]) 
                self.display_custom_samples(self.current_custom_discrete_samples, values, probs) 
                return
            
            try:
                n_demandas = int(n_demandas_str)
                if n_demandas <= 0:
                    messagebox.showerror("Error", "La cantidad de demandas debe ser un entero positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error de Entrada", "Ingrese un valor numérico válido para la cantidad de demandas.")
                return

            available_rng_count = len(self.current_random_numbers)
            actual_n_to_use = n_demandas

            if n_demandas > available_rng_count:
                messagebox.showwarning("Advertencia",
                                       f"La cantidad de demandas solicitada ({n_demandas}) excede los números aleatorios disponibles ({available_rng_count}).\n"
                                       f"Se usarán los primeros {available_rng_count} números disponibles de la pestaña RNG.")
                actual_n_to_use = available_rng_count
            
            uniform_samples_to_use = self.current_random_numbers[:actual_n_to_use]
            
            indices_samples = metodo_numeros_indice(probs, uniform_samples_to_use)
            self.current_custom_discrete_samples = np.array([values[i] for i in indices_samples])
            
            self.display_custom_samples(self.current_custom_discrete_samples, values, probs)
            self.custom_samples_text_area.insert('1.0', f"Usando los primeros {len(uniform_samples_to_use)} números (U[0,1)) de la pestaña 'Generadores RNG' para simular {len(uniform_samples_to_use)} demandas.\n---\n")

        except ValueError: 
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos (separados por comas) para valores, probabilidades y cantidad de demandas.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    def display_custom_samples(self, samples, values, probs): 
        # ... (remains the same) ...
        self.custom_samples_text_area.delete('1.0', tk.END)
        if not isinstance(samples, np.ndarray): 
            samples = np.array(samples)

        if not samples.any() : 
            if not self.current_random_numbers:
                 self.custom_samples_text_area.insert(tk.END, "No hay números generados desde la pestaña 'Generadores RNG' para usar.\n")
            else: 
                 self.custom_samples_text_area.insert(tk.END, "No se generó ninguna muestra (verifique la cantidad de demandas y los parámetros).\n")
            self.custom_samples_text_area.insert(tk.END, f"Valores posibles definidos: {values}\n")
            self.custom_samples_text_area.insert(tk.END, f"Probabilidades teóricas definidas: {[float(f'{p:.5f}') for p in probs]}\n")
            return 

        self.custom_samples_text_area.insert(tk.END, f"Muestra artificial de tamaño {len(samples)} generada.\n") 
        self.custom_samples_text_area.insert(tk.END, f"Valores posibles: {values}\n")
        self.custom_samples_text_area.insert(tk.END, f"Probabilidades teóricas: {[float(f'{p:.5f}') for p in probs]}\n\n")

        self.custom_samples_text_area.insert(tk.END, "Primeros 100 valores de la muestra:\n") 
        for v in samples[:100]: 
            self.custom_samples_text_area.insert(tk.END, f"{v}\n")
        if len(samples) > 100:
            self.custom_samples_text_area.insert(tk.END, "...\n")
        
        frec_obs_dict = {val: count for val, count in zip(*np.unique(samples, return_counts=True))}
        
        self.custom_samples_text_area.insert(tk.END, "\nFrecuencias Observadas vs Esperadas:\n")
        for i, val_defined in enumerate(values):
            obs_count = frec_obs_dict.get(val_defined, 0)
            exp_count = probs[i] * len(samples)
            self.custom_samples_text_area.insert(tk.END, f"Valor {val_defined}: Observada = {obs_count}, Esperada = {exp_count:.2f}\n")


    def plot_custom_sample_frequencies(self):
        # ... (remains the same, title/labels updated in previous response) ...
        if not isinstance(self.current_custom_discrete_samples, np.ndarray) or not self.current_custom_discrete_samples.any():
            messagebox.showinfo("Información", "Primero genere una muestra artificial usando los números de la pestaña RNG.")
            return
        
        samples = self.current_custom_discrete_samples 
        
        try:
            defined_values_str = self.values_var.get().split(',')
            defined_values = [float(v.strip()) for v in defined_values_str]
            
            defined_probs_str = self.probs_var.get().split(',')
            defined_probs = [float(p.strip()) for p in defined_probs_str]

            if len(defined_values) != len(defined_probs):
                messagebox.showerror("Error", "Los valores y probabilidades definidos no coinciden en cantidad.")
                return
            if not math.isclose(sum(defined_probs), 1.0, rel_tol=1e-5):
                messagebox.showerror("Error", "Las probabilidades definidas no suman 1.")
                return
        except ValueError:
            messagebox.showerror("Error", "Valores o probabilidades definidos inválidos.")
            return

        observed_counts_map = {val: count for val, count in zip(*np.unique(samples, return_counts=True))}
        observed_freq_for_defined_values = [observed_counts_map.get(val, 0) for val in defined_values]

        total_samples = len(samples)
        expected_freq_for_defined_values = [p * total_samples for p in defined_probs]
        
        fig, ax = plt.subplots(figsize=(10,6)) 
        
        x_positions = np.arange(len(defined_values)) 
        bar_width = 0.35

        rects1 = ax.bar(x_positions - bar_width/2, observed_freq_for_defined_values, bar_width, label="Frec. Observada", color='skyblue')
        rects2 = ax.bar(x_positions + bar_width/2, expected_freq_for_defined_values, bar_width, label="Frec. Esperada", color='lightcoral')

        ax.set_xlabel("Valores Definidos de Demanda")
        ax.set_ylabel("Frecuencia Absoluta")
        ax.set_title("Frecuencias Observadas vs Esperadas de la Demanda de Periódicos")
        ax.set_xticks(x_positions)
        ax.set_xticklabels([str(int(v)) for v in defined_values], rotation=45, ha="right") 
        ax.legend()
        ax.grid(axis='y', linestyle='--')

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.0f}', 
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8)
        autolabel(rects1)
        autolabel(rects2)

        plt.tight_layout() 
        self.show_plot(fig, "Frecuencias de Demanda de Periódicos")

    def plot_daily_sales_sequence(self):
        # ... (remains the same from previous response) ...
        if not isinstance(self.current_custom_discrete_samples, np.ndarray) or not self.current_custom_discrete_samples.any():
            messagebox.showinfo("Información", "Primero genere una muestra de demandas usando los números de la pestaña RNG.")
            return

        samples = self.current_custom_discrete_samples
        days = np.arange(1, len(samples) + 1) 

        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(days, samples, marker='o', linestyle='-', color='dodgerblue', markersize=5)

        ax.set_xlabel("Día Consecutivo")
        ax.set_ylabel("Demanda Diaria de Periódicos (Venta)")
        ax.set_title(f"Secuencia de {len(samples)} Demandas Diarias de Periódicos")
        ax.grid(True, linestyle='--', alpha=0.7)
        
        try:
            defined_values_str = self.values_var.get().split(',')
            defined_values = [float(v.strip()) for v in defined_values_str]
            min_demand = min(defined_values) if defined_values else np.min(samples)
            max_demand = max(defined_values) if defined_values else np.max(samples)
            ax.set_ylim(min_demand - 2, max_demand + 2) 
        except: 
            ax.set_ylim(np.min(samples) - 2 , np.max(samples) + 2)

        if len(samples) <= 60 : 
             ax.set_xticks(days)
        else: 
             ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=min(len(samples), 20)))

        plt.tight_layout()
        self.show_plot(fig, "Secuencia de Ventas Diarias de Periódicos")


    def create_montecarlo_tab(self):
        # ... (remains the same, does not use Tab 1 RNGs by this request) ...
        tab_mc = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_mc, text="Simulación Montecarlo")

        mc_config_frame = ttk.LabelFrame(tab_mc, text="Configuración de Simulación Montecarlo", padding="10")
        mc_config_frame.pack(pady=10, padx=10, fill="x")

        self.selected_montecarlo_var = tk.StringVar(value="Estimación de Pi")
        mc_simulations = ["Estimación de Pi", "Integración Numérica (Función Simple)"]
        mc_cb = ttk.Combobox(mc_config_frame, textvariable=self.selected_montecarlo_var, values=mc_simulations, state="readonly", width=30)
        mc_cb.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        mc_cb.bind("<<ComboboxSelected>>", self.update_montecarlo_params_visibility)

        self.n_mc_var, self.n_mc_entry, n_mc_frame = self.create_input_frame(mc_config_frame, "Número de Iteraciones (N):", "10000")
        n_mc_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        self.mc_params_frames = {}

        frame_pi = ttk.Frame(mc_config_frame) 
        self.mc_params_frames["Estimación de Pi"] = frame_pi

        frame_integral = ttk.Frame(mc_config_frame)
        func_label = ttk.Label(frame_integral, text="Función a integrar (ej: x**2): f(x)=")
        func_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.func_str_var = tk.StringVar(value="x**2")
        self.func_entry = ttk.Entry(frame_integral, textvariable=self.func_str_var, width=15)
        self.func_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        lim_a_label = ttk.Label(frame_integral, text="Límite inferior (a):")
        lim_a_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.lim_a_var = tk.StringVar(value="0")
        self.lim_a_entry = ttk.Entry(frame_integral, textvariable=self.lim_a_var, width=8)
        self.lim_a_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        lim_b_label = ttk.Label(frame_integral, text="Límite superior (b):")
        lim_b_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.lim_b_var = tk.StringVar(value="1")
        self.lim_b_entry = ttk.Entry(frame_integral, textvariable=self.lim_b_var, width=8)
        self.lim_b_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        self.mc_params_frames["Integración Numérica (Función Simple)"] = frame_integral

        current_row_for_params = 2 
        for name, frame in self.mc_params_frames.items():
            frame.grid(row=current_row_for_params, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.update_montecarlo_params_visibility() 

        run_mc_button = ttk.Button(mc_config_frame, text="Ejecutar Simulación Montecarlo", command=self.run_montecarlo_simulation)
        run_mc_button.grid(row=current_row_for_params + 1, column=0, columnspan=2, pady=10)

        mc_results_frame = ttk.LabelFrame(tab_mc, text="Resultados de la Simulación", padding="10")
        mc_results_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.mc_results_text_area = tk.Text(mc_results_frame, height=15, width=70, wrap=tk.WORD, relief='sunken', borderwidth=1, font=('Courier New', 10))
        self.mc_results_text_area.pack(pady=5, padx=5, fill="both", expand=True)
        mc_results_scrollbar = ttk.Scrollbar(self.mc_results_text_area, command=self.mc_results_text_area.yview)
        mc_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mc_results_text_area.config(yscrollcommand=mc_results_scrollbar.set)

    def update_montecarlo_params_visibility(self, event=None):
        # ... (remains the same) ...
        selected = self.selected_montecarlo_var.get()
        for name, frame in self.mc_params_frames.items():
            if name == selected:
                frame.grid() 
            else:
                frame.grid_remove() 

    def run_montecarlo_simulation(self):
        # ... (remains the same) ...
        sim_type = self.selected_montecarlo_var.get()
        self.mc_results_text_area.delete('1.0', tk.END)
        try:
            N = int(self.n_mc_var.get())
            if N <=0 :
                messagebox.showerror("Error", "El número de iteraciones N debe ser positivo.")
                return

            if sim_type == "Estimación de Pi":
                self.simular_montecarlo_pi(N)
            elif sim_type == "Integración Numérica (Función Simple)":
                func_str = self.func_str_var.get()
                a = float(self.lim_a_var.get())
                b = float(self.lim_b_var.get())
                if a >= b:
                    messagebox.showerror("Error", "El límite inferior (a) debe ser menor que el límite superior (b).")
                    return
                self.simular_montecarlo_integral(func_str, a, b, N)
        except ValueError: 
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos para N y los límites de integración.")
        except Exception as e:
            messagebox.showerror("Error en Simulación Montecarlo", f"Ocurrió un error: {e}")


    def simular_montecarlo_pi(self, N):
        # ... (remains the same) ...
        puntos_dentro_circulo = 0
        max_points_to_plot = 5000 
        plot_subset = N > max_points_to_plot
        
        points_x_in, points_y_in = [], []
        points_x_out, points_y_out = [], []

        for i in range(N):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            if x**2 + y**2 <= 1:
                puntos_dentro_circulo += 1
                if not plot_subset or i < max_points_to_plot :
                    points_x_in.append(x)
                    points_y_in.append(y)
            else:
                if not plot_subset or i < max_points_to_plot:
                    points_x_out.append(x)
                    points_y_out.append(y)
        
        pi_estimado = 4 * (puntos_dentro_circulo / N) 
        
        self.mc_results_text_area.insert(tk.END, f"--- Estimación de Pi por Montecarlo ---\n")
        self.mc_results_text_area.insert(tk.END, f"Iteraciones (N): {N}\n")
        self.mc_results_text_area.insert(tk.END, f"Puntos dentro del círculo: {puntos_dentro_circulo}\n")
        self.mc_results_text_area.insert(tk.END, f"Estimación de Pi: {pi_estimado:.6f}\n")
        self.mc_results_text_area.insert(tk.END, f"Valor real de Pi (math.pi): {math.pi:.6f}\n") 
        self.mc_results_text_area.insert(tk.END, f"Error absoluto: {abs(pi_estimado - math.pi):.6f}\n")
        if plot_subset:
             self.mc_results_text_area.insert(tk.END, f"\nNota: Graficando un subconjunto de {max_points_to_plot} puntos.\n")

        fig, ax = plt.subplots(figsize=(6,6))
        ax.scatter(points_x_in, points_y_in, color='blue', s=1, label=f'Dentro ({len(points_x_in)})')
        ax.scatter(points_x_out, points_y_out, color='red', s=1, label=f'Fuera ({len(points_x_out)})')
        
        circle = plt.Circle((0, 0), 1, color='gray', fill=False, linestyle='--', linewidth=1.5) 
        ax.add_artist(circle)
        
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect('equal', adjustable='box')
        title_str = f'Estimación de Pi (N={N}) - Pi ≈ {pi_estimado:.4f}'
        if plot_subset: title_str += f' (mostrando {max_points_to_plot} puntos)'
        ax.set_title(title_str)
        ax.legend(markerscale=5) 
        ax.grid(False) 
        self.show_plot(fig, "Estimación de Pi con Montecarlo")

    def simular_montecarlo_integral(self, func_str, a, b, N):
        # ... (remains the same) ...
        safe_dict = {"math": math, "np": np, "x": None} 
        
        def func_to_integrate(x_val):
            safe_dict["x"] = x_val
            try:
                return eval(func_str, {"__builtins__": {}}, safe_dict)
            except Exception as e:
                raise ValueError(f"Error al evaluar la función f(x)={func_str}: {e}")

        try:
            func_to_integrate((a + b) / 2) 
        except ValueError as e: 
            messagebox.showerror("Error de Función", str(e))
            return
        except Exception as e_generic: 
            messagebox.showerror("Error de Función", f"Error inesperado al probar la función '{func_str}': {e_generic}")
            return

        sum_fx = 0
        random_x_values = np.random.uniform(a, b, N) 
        
        function_values = []
        for x_rand in random_x_values:
            try:
                fx_val = func_to_integrate(x_rand)
                if not isinstance(fx_val, (int, float)): 
                    messagebox.showerror("Error de Función", f"La función f(x)={func_str} no devolvió un número para x={x_rand:.3f} (devolvió {type(fx_val)}).")
                    return
                function_values.append(fx_val)
            except ValueError as e: 
                 messagebox.showerror("Error de Función", str(e))
                 return

        sum_fx = sum(function_values)
        integral_estimada = (b - a) * (sum_fx / N)

        self.mc_results_text_area.insert(tk.END, f"--- Integración Numérica por Montecarlo ---\n")
        self.mc_results_text_area.insert(tk.END, f"Función f(x): {func_str}\n")
        self.mc_results_text_area.insert(tk.END, f"Límites: [{a}, {b}]\n")
        self.mc_results_text_area.insert(tk.END, f"Iteraciones (N): {N}\n")
        self.mc_results_text_area.insert(tk.END, f"Estimación de la Integral: {integral_estimada:.6f}\n")

        try:
            from scipy.integrate import quad
            integral_exacta, error_exacto = quad(func_to_integrate, a, b)
            self.mc_results_text_area.insert(tk.END, f"Integral (scipy.quad): {integral_exacta:.6f} (error estimado: {error_exacto:.2e})\n")
            self.mc_results_text_area.insert(tk.END, f"Error absoluto Montecarlo vs scipy.quad: {abs(integral_estimada - integral_exacta):.6f}\n")
        except ImportError:
             self.mc_results_text_area.insert(tk.END, "Scipy no está instalado, no se puede calcular la integral exacta para comparación.\n")
        except Exception as e_quad:
            self.mc_results_text_area.insert(tk.END, f"No se pudo calcular la integral con scipy.quad: {e_quad}\n")

        fig, ax = plt.subplots()
        plot_x = np.linspace(a, b, 400) 
        
        try:
            plot_y = np.array([func_to_integrate(val) for val in plot_x])
        except ValueError as e:
            messagebox.showerror("Error de Función para Gráfico", f"No se pudo evaluar la función para graficar: {e}")
            return 

        ax.plot(plot_x, plot_y, 'r-', lw=2, label=f'f(x) = {func_str}')
        ax.fill_between(plot_x, 0, plot_y, where=plot_y >= 0, interpolate=True, color='skyblue', alpha=0.5, label='Área Positiva')
        ax.fill_between(plot_x, 0, plot_y, where=plot_y < 0, interpolate=True, color='salmon', alpha=0.5, label='Área Negativa')

        ax.set_title(f'Integración Montecarlo de f(x)={func_str} en [{a},{b}]')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        ax.grid(True, linestyle=':')
        ax.axhline(0, color='black', lw=0.75) 
        self.show_plot(fig, f"Integración de {func_str}")


    # --- MODIFICATIONS for Queues Tab ---
    def create_queues_tab(self):
        tab_q = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_q, text="Simulación de Colas")

        q_config_frame = ttk.LabelFrame(tab_q, text="Configuración del Sistema de Colas (M/M/s - Usando RNG de Tab 1)", padding="10")
        # ... (rest of UI setup as before) ...
        q_config_frame.pack(pady=10, padx=10, fill="x")
        q_config_frame.columnconfigure(1, weight=1) 
        row_idx = 0
        self.lambda_q_var, _, frame_l = self.create_input_frame(q_config_frame, "Tasa de Llegadas (λ clientes/unidad de tiempo):", "5")
        frame_l.grid(row=row_idx, column=0, columnspan=2, sticky="ew", padx=5, pady=3); row_idx+=1
        self.mu_q_var, _, frame_m = self.create_input_frame(q_config_frame, "Tasa de Servicio (μ clientes/unidad de tiempo por servidor):", "3")
        frame_m.grid(row=row_idx, column=0, columnspan=2, sticky="ew", padx=5, pady=3); row_idx+=1
        self.s_q_var, _, frame_s = self.create_input_frame(q_config_frame, "Número de Servidores (s):", "2")
        frame_s.grid(row=row_idx, column=0, columnspan=2, sticky="ew", padx=5, pady=3); row_idx+=1
        self.sim_time_q_var, _, frame_t = self.create_input_frame(q_config_frame, "Tiempo Total de Simulación:", "100")
        frame_t.grid(row=row_idx, column=0, columnspan=2, sticky="ew", padx=5, pady=3); row_idx+=1
        run_q_button = ttk.Button(q_config_frame, text="Ejecutar Simulación de Colas (desde Tab 1)", command=self.run_queue_simulation_gui)
        run_q_button.grid(row=row_idx, column=0, columnspan=2, pady=10, padx=5)

        q_results_frame = ttk.LabelFrame(tab_q, text="Resultados de la Simulación de Colas", padding="10")
        q_results_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.q_results_text_area = tk.Text(q_results_frame, height=20, width=80, wrap=tk.WORD, relief='sunken', borderwidth=1, font=('Courier New', 10))
        self.q_results_text_area.pack(pady=5, padx=5, fill="both", expand=True)
        q_results_scrollbar = ttk.Scrollbar(self.q_results_text_area, command=self.q_results_text_area.yview)
        q_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.q_results_text_area.config(yscrollcommand=q_results_scrollbar.set)


    def run_queue_simulation_gui(self):
        self.q_results_text_area.delete('1.0', tk.END)
        try:
            lambda_val = float(self.lambda_q_var.get())
            mu_val = float(self.mu_q_var.get())
            s_val = int(self.s_q_var.get())
            sim_time_val = float(self.sim_time_q_var.get())

            if not (lambda_val > 0 and mu_val > 0 and s_val > 0 and sim_time_val > 0):
                messagebox.showerror("Error", "Todos los parámetros de la simulación de colas deben ser positivos.")
                return
            if not isinstance(s_val, int): 
                 messagebox.showerror("Error", "El número de servidores (s) debe ser un entero positivo.")
                 return

            if not self.current_random_numbers:
                messagebox.showerror("Error", "Primero genere números en la pestaña 'Generadores RNG' para usar en la simulación de colas.")
                return
            
            # Pass a copy of the random numbers to the simulator
            rng_for_sim = list(self.current_random_numbers) # Make a copy

            rho_sistema_input = lambda_val / (s_val * mu_val) 
            self.q_results_text_area.insert(tk.END, f"--- Simulación de Colas M/M/{s_val} (Usando RNG de Tab 1) ---\n")
            self.q_results_text_area.insert(tk.END, f"Parámetros: λ={lambda_val:.3f}, μ={mu_val:.3f} (por servidor), s={s_val}, Tiempo Sim={sim_time_val:.2f}\n")
            self.q_results_text_area.insert(tk.END, f"Números RNG disponibles de Tab 1: {len(rng_for_sim)}\n")
            self.q_results_text_area.insert(tk.END, f"Factor de Utilización del Sistema (λ/(s*μ)): {rho_sistema_input:.4f}\n\n")

            if rho_sistema_input >= 1:
                 self.q_results_text_area.insert(tk.END, f"ADVERTENCIA: El factor de utilización ρ_sistema = {rho_sistema_input:.3f} es >= 1.\n"
                                                       "El sistema es inestable y la cola teóricamente crecerá indefinidamente.\n\n")

            simulator = QueueSimulator(lambda_val, mu_val, s_val, rng_for_sim) # Pass RNG list
            results = simulator.run_simulation(sim_time_val)
            
            self.q_results_text_area.insert(tk.END, f"Resultados de la Simulación (hasta T={results.get('simulation_end_time', sim_time_val):.2f}):\n")
            if "simulation_status" in results:
                self.q_results_text_area.insert(tk.END, f"  Estado: {results['simulation_status']}\n")

            self.q_results_text_area.insert(tk.END, f"  Clientes totales llegados: {results['total_arrivals']}\n")
            # ... (rest of results display as before) ...
            self.q_results_text_area.insert(tk.END, f"  Clientes totales servidos: {results['total_served']}\n")
            self.q_results_text_area.insert(tk.END, f"  Clientes remanentes en cola al final: {results.get('final_queue_length', 'N/A')}\n") # Use .get for safety
            self.q_results_text_area.insert(tk.END, f"  Tiempo promedio de espera en cola (Wq_sim): {results['avg_wait_time']:.4f}\n")
            self.q_results_text_area.insert(tk.END, f"  Tiempo promedio en el sistema (Ws_sim): {results['avg_system_time']:.4f}\n")
            self.q_results_text_area.insert(tk.END, f"  Número promedio de clientes en cola (Lq_sim): {results['avg_queue_length']:.4f}\n")
            self.q_results_text_area.insert(tk.END, f"  Número promedio de clientes en el sistema (Ls_sim): {results['avg_system_length']:.4f}\n")
            self.q_results_text_area.insert(tk.END, f"  Utilización promedio de servidores (ρ_sim): {results['avg_server_utilization']:.4f}\n")
            if results.get('max_queue_length') is not None:
                self.q_results_text_area.insert(tk.END, f"  Máxima longitud de cola observada: {results['max_queue_length']}\n")
            if results.get('max_system_length') is not None:
                self.q_results_text_area.insert(tk.END, f"  Máximo número de clientes en sistema: {results['max_system_length']}\n")


            # Theoretical calculations (remain the same)
            self.q_results_text_area.insert(tk.END, "\n--- Fórmulas Teóricas M/M/s (Estado Estacionario) ---\n")
            rho_teorico_servidor = lambda_val / (s_val * mu_val) 
            if rho_teorico_servidor < 1:
                try:
                    sum_term_p0 = sum([(lambda_val / mu_val)**k / math.factorial(k) for k in range(s_val)])
                    term2_p0_num = (lambda_val / mu_val)**s_val
                    term2_p0_den = math.factorial(s_val) * (1 - rho_teorico_servidor)
                    if term2_p0_den == 0: P0 = float('inf') if term2_p0_num > 0 else 0
                    else: term2_p0 = term2_p0_num / term2_p0_den
                    if math.isinf(sum_term_p0) or math.isinf(term2_p0): P0 = 0 
                    else: P0 = 1 / (sum_term_p0 + term2_p0)
                    Lq_teorico = (P0 * ((lambda_val / mu_val)**s_val) * rho_teorico_servidor) / (math.factorial(s_val) * (1 - rho_teorico_servidor)**2)
                    Ls_teorico = Lq_teorico + (lambda_val / mu_val) 
                    Wq_teorico = Lq_teorico / lambda_val
                    Ws_teorico = Wq_teorico + (1 / mu_val) 
                    self.q_results_text_area.insert(tk.END, f"  P0 (Prob. sistema vacío): {P0:.4e}\n")
                    self.q_results_text_area.insert(tk.END, f"  Lq (teórico): {Lq_teorico:.4f}\n")
                    self.q_results_text_area.insert(tk.END, f"  Ls (teórico): {Ls_teorico:.4f}\n")
                    self.q_results_text_area.insert(tk.END, f"  Wq (teórico): {Wq_teorico:.4f}\n")
                    self.q_results_text_area.insert(tk.END, f"  Ws (teórico): {Ws_teorico:.4f}\n")
                    self.q_results_text_area.insert(tk.END, f"  ρ_servidor (utilización teórica por servidor): {rho_teorico_servidor:.4f}\n")
                except OverflowError:
                     self.q_results_text_area.insert(tk.END, "  Error de desbordamiento al calcular valores teóricos.\n")
                except ValueError as ve: 
                     self.q_results_text_area.insert(tk.END, f"  Error matemático al calcular valores teóricos: {ve}\n")
            else: 
                self.q_results_text_area.insert(tk.END, "  El sistema es teóricamente INESTABLE (ρ_servidor >= 1).\n")
                self.q_results_text_area.insert(tk.END, f"  ρ_servidor (utilización teórica por servidor): {rho_teorico_servidor:.4f}\n")

            # Plotting (remains the same, uses data from results dict)
            times = results.get('event_times', [])
            queue_lengths = results.get('queue_length_over_time', [])
            system_lengths = results.get('system_length_over_time', [])
            servers_busy_count = results.get('servers_busy_over_time', [])

            if times and queue_lengths and system_lengths and servers_busy_count and len(times) > 1:
                fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True) 
                axes[0].step(times, queue_lengths, where='post', label='Clientes en Cola', color='dodgerblue')
                # ... (rest of plotting logic) ...
                axes[0].set_title('Evolución de la Longitud de la Cola')
                axes[0].set_ylabel('Nº Clientes en Cola')
                axes[0].legend(loc='upper left')
                axes[0].grid(True, linestyle=':', alpha=0.7)

                axes[1].step(times, system_lengths, where='post', label='Clientes en Sistema', color='forestgreen')
                axes[1].set_title('Evolución del Nº de Clientes en el Sistema')
                axes[1].set_ylabel('Nº Clientes en Sistema')
                axes[1].legend(loc='upper left')
                axes[1].grid(True, linestyle=':', alpha=0.7)

                axes[2].step(times, servers_busy_count, where='post', label='Servidores Ocupados', color='mediumorchid')
                axes[2].set_title('Evolución del Nº de Servidores Ocupados')
                axes[2].set_xlabel(f'Tiempo (hasta T={results.get("simulation_end_time", sim_time_val):.2f})')
                axes[2].set_ylabel('Nº Servidores Ocupados')
                axes[2].set_yticks(range(s_val + 1)) 
                axes[2].legend(loc='upper left')
                axes[2].grid(True, linestyle=':', alpha=0.7)
                
                plt.tight_layout(pad=2.0) 
                self.show_plot(fig, "Comportamiento Temporal del Sistema de Colas")

            elif not results.get("simulation_status", "").startswith("Completada"):
                pass # Don't show "no data to plot" if already reported premature termination status
            else:
                 self.q_results_text_area.insert(tk.END, "\nNo hay suficientes datos de eventos para graficar.\n")

        except ValueError: 
            messagebox.showerror("Error de Entrada", "Por favor, introduce valores numéricos válidos para los parámetros de la cola.")
        except Exception as e:
            messagebox.showerror("Error en Simulación de Colas", f"Ocurrió un error inesperado: {e}")
            import traceback
            traceback.print_exc() 

    def show_plot(self, fig, title="Gráfico"):
        # ... (remains the same) ...
        for win in self.root.winfo_children():
            if isinstance(win, tk.Toplevel) and win.title() == title:
                win.destroy()
                break 
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("800x600") 
        top.resizable(True, True)
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar_frame = ttk.Frame(top)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update() 
        canvas.draw() 


class QueueSimulator:
    def __init__(self, lambda_rate, mu_rate_per_server, num_servers, random_numbers_list):
        self.lambda_rate = lambda_rate  
        self.mu_rate_per_server = mu_rate_per_server  
        self.num_servers = num_servers  
        
        self.rng_stream = iter(random_numbers_list) # Use an iterator for the provided RNG list
        self.rng_provided_count = len(random_numbers_list)
        self.rng_consumed_count = 0

        self.clock = 0.0
        # Initial event scheduling requires first random number(s)
        try:
            self.next_arrival_time = self._generate_interarrival_time_internal() 
        except ValueError: # Not enough RNGs even for the first event
            self.next_arrival_time = float('inf') # Prevent simulation from starting
            self.initial_rng_error = True
        else:
            self.initial_rng_error = False


        self.server_status = [0] * num_servers # 0 for free, customer_id if busy
        self.service_completion_times = [float('inf')] * num_servers 
        self.queue = []  # Stores customer_ids

        self.total_arrivals = 0
        self.total_served = 0
        self.total_wait_time = 0.0  
        self.total_system_time = 0.0 
        
        self.area_queue_length = 0.0 
        self.area_system_length = 0.0 
        self.area_server_busy_time = [0.0] * num_servers 

        self.event_times = [0.0] 
        self.queue_length_over_time = [0] 
        self.system_length_over_time = [0] 
        self.servers_busy_over_time = [0] 
        self.last_event_time = 0.0 

        self.max_queue_length_obs = 0
        self.max_system_length_obs = 0
        self.customer_data = {} # To track arrival times for system time calculation

    def _get_next_rng(self):
        try:
            u = next(self.rng_stream)
            self.rng_consumed_count += 1
            # Clip to avoid issues with log(0) or log(1) if ppf doesn't handle it.
            # For log(1-u), u=1 -> log(0). For log(u), u=0 -> log(0)
            return np.clip(u, 1e-9, 1.0 - 1e-9) 
        except StopIteration:
            raise ValueError(f"Se agotaron los números aleatorios de Tab 1. Usados: {self.rng_consumed_count}/{self.rng_provided_count}")

    def _generate_interarrival_time_internal(self):
        u = self._get_next_rng()
        return -math.log(1.0 - u) / self.lambda_rate # Using 1-u for exp a_rate F(x) = 1 - e^(-ax)

    def _generate_service_time_internal(self):
        u = self._get_next_rng()
        return -math.log(1.0 - u) / self.mu_rate_per_server
    
    def find_free_server(self): # Remains the same
        for i in range(self.num_servers):
            if self.server_status[i] == 0: # 0 means free
                return i
        return -1

    def update_stats_areas(self): # Remains the same
        time_since_last_event = self.clock - self.last_event_time
        if time_since_last_event > 0: 
            self.area_queue_length += len(self.queue) * time_since_last_event
            num_in_service = sum(1 for status in self.server_status if status != 0)
            self.area_system_length += (len(self.queue) + num_in_service) * time_since_last_event
            for i in range(self.num_servers):
                if self.server_status[i] != 0: 
                    self.area_server_busy_time[i] += time_since_last_event
        self.last_event_time = self.clock 

    def record_event_state(self): # Remains the same
        self.event_times.append(self.clock)
        self.queue_length_over_time.append(len(self.queue))
        current_system_length = len(self.queue) + sum(1 for status in self.server_status if status != 0)
        self.system_length_over_time.append(current_system_length)
        self.servers_busy_over_time.append(sum(1 for status in self.server_status if status != 0))
        self.max_queue_length_obs = max(self.max_queue_length_obs, len(self.queue))
        self.max_system_length_obs = max(self.max_system_length_obs, current_system_length)

    def run_simulation(self, simulation_time):
        simulation_status_msg = f"Completada. {self.rng_consumed_count} de {self.rng_provided_count} números RNG usados."
        
        if self.initial_rng_error:
            simulation_status_msg = f"No hay suficientes números RNG de Tab 1 ni para el primer evento. Usados: {self.rng_consumed_count}/{self.rng_provided_count}"
            # Return empty/default stats
            final_results = {
                "total_arrivals": 0, "total_served": 0, "avg_wait_time": 0, "avg_system_time": 0,
                "avg_queue_length": 0, "avg_system_length": 0, "avg_server_utilization": 0,
                "event_times": [0], "queue_length_over_time": [0], "system_length_over_time": [0],
                "servers_busy_over_time": [0], "max_queue_length": 0, "max_system_length": 0,
                "simulation_status": simulation_status_msg, "simulation_end_time": 0,
                "final_queue_length": 0
            }
            return final_results

        try:
            while self.clock < simulation_time:
                next_service_completion_event_time = min(self.service_completion_times) if any(s != float('inf') for s in self.service_completion_times) else float('inf')

                if self.next_arrival_time <= next_service_completion_event_time and self.next_arrival_time < simulation_time:
                    self.update_stats_areas()
                    self.clock = self.next_arrival_time
                    self.total_arrivals += 1
                    customer_id = self.total_arrivals 
                    
                    self.customer_data[customer_id] = {"arrival_time": self.clock, "service_start_time": -1, "service_time": -1}

                    server_idx = self.find_free_server()
                    if server_idx != -1:
                        self.server_status[server_idx] = customer_id 
                        service_time = self._generate_service_time_internal()
                        self.service_completion_times[server_idx] = self.clock + service_time
                        self.customer_data[customer_id]["service_start_time"] = self.clock
                        self.customer_data[customer_id]["service_time"] = service_time
                    else:
                        self.queue.append(customer_id)
                    
                    self.next_arrival_time = self.clock + self._generate_interarrival_time_internal()

                elif next_service_completion_event_time < simulation_time:
                    self.update_stats_areas()
                    self.clock = next_service_completion_event_time
                    server_finished_idx = self.service_completion_times.index(next_service_completion_event_time)
                    
                    departing_customer_id = self.server_status[server_finished_idx]
                    if departing_customer_id != 0: # A customer was being served
                        self.total_served += 1
                        cust_info = self.customer_data[departing_customer_id]
                        wait_time = cust_info["service_start_time"] - cust_info["arrival_time"]
                        # self.total_wait_time += wait_time # Wait time is added when service STARTS
                        self.total_system_time += (self.clock - cust_info["arrival_time"])
                    
                    if self.queue:
                        next_customer_id = self.queue.pop(0)
                        self.server_status[server_finished_idx] = next_customer_id
                        
                        cust_info = self.customer_data[next_customer_id]
                        wait_time_for_new = self.clock - cust_info["arrival_time"]
                        self.total_wait_time += wait_time_for_new # Accumulate wait time now
                        cust_info["service_start_time"] = self.clock

                        service_time = self._generate_service_time_internal()
                        cust_info["service_time"] = service_time
                        self.service_completion_times[server_finished_idx] = self.clock + service_time
                    else:
                        self.server_status[server_finished_idx] = 0 
                        self.service_completion_times[server_finished_idx] = float('inf')
                else:
                    self.update_stats_areas()
                    self.clock = simulation_time
                    break
                self.record_event_state()
        
        except ValueError as e: # Catches RNG depletion from _get_next_rng
            simulation_status_msg = str(e) + f" Simulación detenida a t={self.clock:.2f}."
            print(simulation_status_msg) # Log to console
            # No more events can be processed. Finalize areas with current clock.
            self.update_stats_areas() # update areas till the point of failure
        
        # Finalize stats based on the actual end time (could be < simulation_time if RNGs depleted)
        actual_simulation_end_time = self.clock
        if self.last_event_time < actual_simulation_end_time : # Ensure last segment is counted
             self.clock = actual_simulation_end_time # Set clock for final update_stats_areas call if not already
             self.update_stats_areas()
        if not self.event_times or self.event_times[-1] < actual_simulation_end_time:
             self.record_event_state() # Record final state if needed

        avg_wait_time = self.total_wait_time / self.total_served if self.total_served > 0 else 0
        avg_system_time = self.total_system_time / self.total_served if self.total_served > 0 else 0
        avg_queue_length = self.area_queue_length / actual_simulation_end_time if actual_simulation_end_time > 0 else 0
        avg_system_length = self.area_system_length / actual_simulation_end_time if actual_simulation_end_time > 0 else 0
        total_busy_time_all_servers = sum(self.area_server_busy_time)
        avg_server_utilization = total_busy_time_all_servers / (self.num_servers * actual_simulation_end_time) if actual_simulation_end_time > 0 and self.num_servers > 0 else 0
        simulation_status_msg += f" RNG consumidos: {self.rng_consumed_count}/{self.rng_provided_count}."


        final_results = {
            "total_arrivals": self.total_arrivals, "total_served": self.total_served,
            "avg_wait_time": avg_wait_time, "avg_system_time": avg_system_time,
            "avg_queue_length": avg_queue_length, "avg_system_length": avg_system_length,
            "avg_server_utilization": avg_server_utilization,
            "event_times": self.event_times, "queue_length_over_time": self.queue_length_over_time,
            "system_length_over_time": self.system_length_over_time,
            "servers_busy_over_time": self.servers_busy_over_time,
            "max_queue_length": self.max_queue_length_obs if self.total_arrivals > 0 else 0,
            "max_system_length": self.max_system_length_obs if self.total_arrivals > 0 else 0,
            "simulation_status": simulation_status_msg,
            "simulation_end_time": actual_simulation_end_time,
            "final_queue_length": len(self.queue)
        }
        return final_results

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()