def is_square(num):
    x = num // 2
    seen = {x}
    while x * x != num:
        x = (x + (num // x)) // 2
        if x in seen:
            return False
        seen.add(x)
    return True

class Graph:
    def __init__(self):
        self.graph = {}
        self.previous = {}
        self.hamiltonian_path = []

    def add(self, val):
        self.previous = self.copy()
        self.graph[val] = []
        if len(self.graph) == 1:
            return
        for node in self.graph:  # O(|V|)
            if node != val:
                if is_square(node + val):
                    if val not in self.graph[node]:
                        self.graph[node].append(val)
                    if node not in self.graph[val]:
                        self.graph[val].append(node)

        curr_path = self.get_difference(val)
        if val < 26:
            self.hamiltonian_path = self.hamiltonian([], False)
        else:
            if len(curr_path) > 0:
                self.hamiltonian_path = self.hamiltonian(curr_path, True)
            else:
                self.hamiltonian_path = self.hamiltonian([], False)

    def get_difference(self, val):
        if isinstance(self.hamiltonian_path, bool):
            return []
        same = []
        different = []
        found = False
        for node in self.hamiltonian_path:
            if self.previous[node] != self.graph[node] and not found:
                found = True
            if not found:
                same.append(node)
            else:
                different.append(node)
        return same

    def copy(self):
        new = {}
        for k in self.graph:
            new[k] = self.graph[k].copy()
        return new

    def hamiltonian(self, path=[], given_start=False):
        size = len(self.graph)
        sub_graph = self.copy()
        if len(path) > 0:
            for node in list(sub_graph):  # O(|E|)
                if node in path and node != path[-1]:
                    for connection in sub_graph[node]:
                        sub_graph[connection].remove(node)
                    del sub_graph[node]

        def search(routes, start=given_start):
            if len(path) == size:
                return path
            routes = sorted(routes, key=lambda routes: len(sub_graph[routes]))
            if start:
                routes.remove(path[-1])
                routes.insert(0, path[-1])
                path.pop()
            for route in routes:
                if route not in path:
                    path.append(route)
                for vertex in sub_graph[route]:
                    sub_graph[vertex].remove(route)
                if search(sub_graph[route], False):
                    return path
                path.pop()
                for vertex in sub_graph[route]:
                    sub_graph[vertex].append(route)
            return False

        return search([k for k in sub_graph])


def validate(sol):
    return all([(n + sol[e]) ** .5 % 1 == 0 for e, n in enumerate(sol[:-1], 1)])

def square_sums(n):
    pairs = []
    squares = [i * i for i in range(1, n // 2)]
    squares.reverse()
    nums = [i for i in range(1, n + 1)]
    curr = n
    while len(nums) > 0:
        if len(nums) == 1:
            while curr not in nums:
                curr -= 1
            pairs.append(curr)
            nums.remove(curr)
            curr -= 1
            break
        for square in squares:
            if curr in nums:
                if square - curr in nums and curr != square - curr:
                    pairs.append([square - curr, curr])
                    nums.remove(curr)
                    nums.remove(square - curr)
                    curr -= 1
                    break
            else:
                curr -= 1
                break
    path = []
    while len(pairs) > 0:
        for pair in list(pairs):
            if isinstance(pair, int):
                if is_square(pair + path[-1]):
                    path.append(pair)
                    pairs.remove(pair)
                elif is_square(pair + path[0]):
                    path.insert(0, pair)
                    pairs.remove(pair)
            elif len(path) == 0:
                path.append(pair[0])
                path.append(pair[1])
                pairs.remove(pair)
            else:
                if is_square(pair[0] + path[-1]):
                    path.append(pair[0])
                    path.append(pair[1])
                    pairs.remove(pair)
                elif is_square(pair[1] + path[-1]):
                    path.append(pair[1])
                    path.append(pair[0])
                    pairs.remove(pair)
                elif is_square(pair[0] + path[0]):
                    path.insert(0, pair[0])
                    path.insert(0, pair[1])
                    pairs.remove(pair)
                elif is_square(pair[1] + path[0]):
                    path.insert(0, pair[1])
                    path.insert(0, pair[0])
                    pairs.remove(pair)
    print(path)


def main():
#     square_sums(200)
    import sys
    from timeit import default_timer as timer
    sys.setrecursionlimit(1000000)
    graph = Graph()
    start = timer()
    for i in range(1, 50):
        beg = timer()
        graph.add(i)
        end = timer()
        if graph.hamiltonian_path:
            print(f"{i}: {graph.hamiltonian_path}, took {(end - beg) * 1000} milliseconds, result is {validate(graph.hamiltonian_path)}")
        else:
            print(f"{i} has no path, took {(end - beg) * 1000} milliseconds")
    finish = timer()
    print(f"Total time was {(finish - start) * 1000} milliseconds")


if __name__ == "__main__":
    main()

# import sys
# from timeit import default_timer as timer
# import matplotlib.pyplot as plt
# import csv
# sys.setrecursionlimit(1000000)
# nums = []
# times = []
# with open('data1.csv', mode='w') as data_file:
#     data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     data_writer.writerow(['Graph Size', 'Path', 'Verified Path', 'Runtime (milliseconds)'])
#     for n in range(26, 2001):
#         graph = Graph()
#         start = timer()
#         for i in range(1, n):
#             graph.add(i)
#             # print(f"{i}: {graph.hamiltonian_path}")
#             # if graph.hamiltonian_path:
#             #     print(f"Result is {validate(graph.hamiltonian_path)}")
#         end = timer()
#         nums.append(n)
#         times.append((end - start) * 1000)
#
#         data_writer.writerow([i + 1, graph.hamiltonian_path, validate(graph.hamiltonian_path) , (end - start) * 1000])
#         print(f"{n} is {graph.hamiltonian_path} and took {end - start} seconds")
#
#     plt.scatter(nums, times)
#     plt.xlabel("Graph Size")
#     plt.ylabel("Runtime (milliseconds)")
#     plt.show()

# -----------------------------

# import csv
# import matplotlib.pyplot as plt
#
# sizes = []
# times = []
# xdiff = []
# differences = []
# with open('data.csv', mode='r') as data_file:
#     data_reader = csv.reader(data_file, delimiter=',')
#     line = 0
#     for row in data_reader:
#         if line > 0:
#             sizes.append(int(row[0]))
#             times.append(float(row[-1]))
#         line += 1
#
# with open('clean_data.csv', mode='w') as clean_file:
#     clean_writer = csv.writer(clean_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     clean_writer.writerow(['Graph Size', 'Runtime (milliseconds)'])
#     for i in range(len(sizes)):
#         clean_writer.writerow([sizes[i], round(times[i], 6)])
#
# for i in range(len(times)):
#     if i < len(times) - 1:
#         xdiff.append(i + 1)
#         differences.append(times[i + 1] - times[i])
#
# plt.scatter(sizes, times)
# plt.xlabel("Graph Size")
# plt.ylabel("Runtime (milliseconds)")
# plt.show()
