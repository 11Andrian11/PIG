import random

# Base Class
class Computer:
    def __init__(self, cpu, ram, storage):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

    def set_parameters(self, cpu=None, ram=None, storage=None):
        if cpu:
            self.cpu = cpu
        if ram:
            self.ram = ram
        if storage:
            self.storage = storage

    def get_info(self):
        return f"CPU: {self.cpu}, RAM: {self.ram}GB, Storage: {self.storage}GB"

# Inherited Classes
class GamingComputer(Computer):
    def __init__(self, cpu, ram, storage, gpu):
        super().__init__(cpu, ram, storage)
        self.gpu = gpu

    def get_info(self):
        return f"[Gaming PC] {super().get_info()}, GPU: {self.gpu}"

class WorkstationComputer(Computer):
    def __init__(self, cpu, ram, storage, software):
        super().__init__(cpu, ram, storage)
        self.software = software

    def get_info(self):
        return f"[Workstation] {super().get_info()}, Software: {self.software}"

class ServerComputer(Computer):
    def __init__(self, cpu, ram, storage, network_speed):
        super().__init__(cpu, ram, storage)
        self.network_speed = network_speed

    def get_info(self):
        return f"[Server] {super().get_info()}, Network Speed: {self.network_speed}Gbps"


# Generate sample objects
computers = []

# 10 Gaming PCs
for i in range(10):
    computers.append(GamingComputer(
        cpu=f"Intel i7-{9000+i}",
        ram=random.choice([16, 32]),
        storage=random.choice([512, 1024]),
        gpu=f"NVIDIA RTX {random.choice([3060, 3070, 3080])}"
    ))

# 10 Workstations
for i in range(10):
    computers.append(WorkstationComputer(
        cpu=f"AMD Ryzen {i+5} 5600X",
        ram=random.choice([32, 64]),
        storage=random.choice([1024, 2048]),
        software=random.choice(["AutoCAD", "MATLAB", "SolidWorks"])
    ))

# 10 Servers
for i in range(10):
    computers.append(ServerComputer(
        cpu=f"Xeon E5-{2600+i}",
        ram=random.choice([64, 128]),
        storage=random.choice([2048, 4096]),
        network_speed=random.choice([1, 10, 25, 40])
    ))


# Simple text-based interface
def menu():
    while True:
        print("\n==== Computer Management ====")
        print("1. Show all computers")
        print("2. Modify a computer's parameters")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            for idx, comp in enumerate(computers):
                print(f"{idx}. {comp.get_info()}")

        elif choice == "2":
            idx = int(input("Enter computer index (0-29): "))
            if 0 <= idx < len(computers):
                cpu = input("Enter new CPU (or press Enter to skip): ")
                ram = input("Enter new RAM (or press Enter to skip): ")
                storage = input("Enter new Storage (or press Enter to skip): ")

                ram = int(ram) if ram else None
                storage = int(storage) if storage else None

                computers[idx].set_parameters(
                    cpu=cpu if cpu else None,
                    ram=ram,
                    storage=storage
                )
                print("Updated:", computers[idx].get_info())
            else:
                print("Invalid index!")

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid option, try again.")


# Run program
if __name__ == "__main__":
    menu()
