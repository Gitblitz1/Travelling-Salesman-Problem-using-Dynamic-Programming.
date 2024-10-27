import tkinter as tk
import itertools
import math
import random

class TSP:
    def __init__(self, cities):
        self.cities = cities
        self.num_cities = len(cities)
        self.distance_matrix = self.calculate_distances()
        self.best_route = None
        self.min_distance = float('inf')

    def calculate_distances(self):
        distance_matrix = [[0] * self.num_cities for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    distance_matrix[i][j] = self.distance(self.cities[i], self.cities[j])
        return distance_matrix

    @staticmethod
    def distance(city1, city2):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

    def solve(self):
        for route in itertools.permutations(range(self.num_cities)):
            distance = self.calculate_route_distance(route)
            if distance < self.min_distance:
                self.min_distance = distance
                self.best_route = route

    def calculate_route_distance(self, route):
        distance = 0
        for i in range(len(route)):
            distance += self.distance_matrix[route[i]][route[(i + 1) % len(route)]]
        return distance

class TSPVisualizer:
    def __init__(self, master, cities, city_names):
        self.master = master
        self.master.title("Traveling Salesman Problem Solver")
        self.canvas = tk.Canvas(master, width=600, height=600, bg='white')
        self.canvas.pack()
        
        self.cities = cities
        self.city_names = city_names
        self.tsp = TSP(cities)
        self.tsp.solve()
        self.step = 0
        self.animate()

    def animate(self):
        if self.step < len(self.tsp.best_route):
            self.update_canvas(self.tsp.best_route[self.step])
            self.step += 1
            self.master.after(1000, self.animate)
        else:
            self.draw_best_route()

    def update_canvas(self, index):
        self.canvas.delete("all")
        for i, city in enumerate(self.cities):
            x, y = city
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='blue')
            self.canvas.create_text(x, y - 10, text=self.city_names[i])

        if self.step > 0:
            prev_index = self.tsp.best_route[self.step - 1]
            self.canvas.create_line(self.cities[prev_index][0], self.cities[prev_index][1],
                                    self.cities[index][0], self.cities[index][1], fill='red', width=2)

            # Display distance between cities
            distance = self.tsp.distance_matrix[prev_index][index]
            mid_x = (self.cities[prev_index][0] + self.cities[index][0]) / 2
            mid_y = (self.cities[prev_index][1] + self.cities[index][1]) / 2
            self.canvas.create_text(mid_x, mid_y, text=f"{distance:.2f}", fill='black')

        # Show the current step
        self.canvas.create_text(300, 580, text=f"Visiting: {self.city_names[index]} (Step {self.step + 1})", font=("Arial", 12))

    def draw_best_route(self):
        self.canvas.delete("all")
        for i, city in enumerate(self.cities):
            x, y = city
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='blue')
            self.canvas.create_text(x, y - 10, text=self.city_names[i])

        for i in range(len(self.tsp.best_route)):
            start_city = self.tsp.best_route[i]
            end_city = self.tsp.best_route[(i + 1) % len(self.tsp.best_route)]
            self.canvas.create_line(self.cities[start_city][0], self.cities[start_city][1],
                                    self.cities[end_city][0], self.cities[end_city][1], fill='green', width=2)

            # Display distances on best route
            distance = self.tsp.distance_matrix[start_city][end_city]
            mid_x = (self.cities[start_city][0] + self.cities[end_city][0]) / 2
            mid_y = (self.cities[start_city][1] + self.cities[end_city][1]) / 2
            self.canvas.create_text(mid_x, mid_y, text=f"{distance:.2f}", fill='black')

        self.canvas.create_text(300, 550, text=f"Best Distance: {self.tsp.min_distance:.2f}", font=("Arial", 12))

def main():
    # Predefined city coordinates
    cities = [(random.randint(50, 550), random.randint(50, 550)) for _ in range(10)]
    
    # City names
    city_names = ["Delhi", "Noida", "Lucknow", "Mumbai", "Ahmedabad", "Kolkata", "Chennai", "Bangalore", "Hyderabad", "Pune"]
    
    root = tk.Tk()
    visualizer = TSPVisualizer(root, cities, city_names)
    root.mainloop()

if __name__ == "__main__":
    main()
