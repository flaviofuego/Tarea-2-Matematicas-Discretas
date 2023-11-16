import networkx as nx
import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

class GrafoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cubrimiento de Grafos")

        self.crear_grafo_conexo()

        self.radio_var = tk.StringVar(value="vertices")

        self.crear_interfaz()

    def crear_grafo_conexo(self):
        while True:
            self.G = nx.erdos_renyi_graph(8, 0.5)
            if nx.is_connected(self.G):
                break

    def crear_interfaz(self):
        ttk.Label(self.root, text="Seleccione el tipo de cubrimiento:").pack(pady=10)

        ttk.Radiobutton(self.root, text="Por Vértices", variable=self.radio_var, value="vertices").pack()
        ttk.Radiobutton(self.root, text="Por Aristas", variable=self.radio_var, value="aristas").pack()

        ttk.Button(self.root, text="Realizar Cubrimiento", command=self.realizar_cubrimiento).pack(pady=10)
        ttk.Button(self.root, text="Generar Nuevo Grafo", command=self.generar_nuevo_grafo).pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.resultado_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.resultado_label.pack()

        self.dibujar_grafo()

    def realizar_cubrimiento(self):
        tipo_cubrimiento = self.radio_var.get()

        if tipo_cubrimiento == "vertices":
            C = self.cubrimiento_por_vertices()
        elif tipo_cubrimiento == "aristas":
            C = self.cubrimiento_por_aristas()

        self.resultado_label.config(text=f"Conjunto C: {C}")

    def generar_nuevo_grafo(self):
        plt.clf()  # Limpiar la figura de Matplotlib
        self.crear_grafo_conexo()
        self.resultado_label.config(text="")  # Limpiar el resultado
        self.dibujar_grafo()


    def cubrimiento_por_vertices(self):
        C = set()

        while self.G.edges():
            max_vertice = max(self.G.degree, key=lambda x: x[1])
            C.add(max_vertice[0])
            self.G.remove_node(max_vertice[0])

        return C

    def cubrimiento_por_aristas(self):
        C = set()

        while self.G.edges():
            arista = random.choice(list(self.G.edges()))
            u, v = arista

            # Agregar la arista al conjunto solución C
            C.add(arista)

            # Marcar los vértices u y v como no disponibles
            self.G.nodes[u]["disponible"] = False
            self.G.nodes[v]["disponible"] = False

            # Marcar la arista seleccionada como cubierta
            self.G[u][v]["cubierta"] = True

            # Marcar el resto de aristas incidentes como eliminadas
            for vecino in self.G.neighbors(u):
                self.G[u][vecino]["eliminada"] = True
            for vecino in self.G.neighbors(v):
                self.G[v][vecino]["eliminada"] = True

            # Eliminar las aristas marcadas como eliminadas
            aristas_a_eliminar = [(x, y) for x, y, data in self.G.edges(data=True) if data.get("eliminada")]
            self.G.remove_edges_from(aristas_a_eliminar)

        return C

    def dibujar_grafo(self):
        self.canvas.delete("all")

        plt.clf()  # Limpiar la figura de Matplotlib

        pos = nx.spring_layout(self.G)
        nx.draw_networkx_nodes(self.G, pos, node_size=700)
        nx.draw_networkx_edges(self.G, pos)
        nx.draw_networkx_labels(self.G, pos)

        plt.axis("off")
        plt.show(block=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoApp(root)
    root.mainloop()
