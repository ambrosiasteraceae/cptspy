class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * self.length + 2 * self.width

# Here we declare that the Square class inherits from the Rectangle class
class Square(Rectangle):
    def __init__(self, length):
        super().__init__(length, length)




square = Square(4)
square.area()

print(square.length)

class Cube(Square):
    def surface_area(self):
        face_area = super().area()
        return face_area * 6

    def volume(self):
        face_area = super().area()
        return face_area * self.length
    
import os

def print_folder_structure(root_dir, indent=""):
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isfile(item_path):
            if item_path.endswith(".csv"):
                break
            elif item_path.endswith(".xlsx"):
                break
            elif item_path.endswith(".npz"):
                break
            elif item_path.endswith(".xls"):
                break
            print(f"{indent}- {item}")  # Print file
        elif os.path.isdir(item_path):
            if item_path.endswith(".csv"):
                break
            elif item_path.endswith(".xlsx"):
                break
            elif item_path.endswith(".npz"):
                break
            print(f"{indent}+ {item}/")  # Print directory
            print_folder_structure(item_path, indent + "  ")  # Recursively traverse subdirectories

path = 'C:/Users/dragos/Documents/GitHub/cptspy'

print(print_folder_structure(path))