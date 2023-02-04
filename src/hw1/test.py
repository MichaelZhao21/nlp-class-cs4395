import sys
import csv
import re
import pickle

class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print(f'{self.last}, {self.first} {self.mi}, {self.id}, {self.phone}')

def process_file(file_path):
    persons = {}

    # Open the file and read in the data
    with open(file_path, 'r') as file:
        data = csv.reader(file)

        # Skip the first line (heading)
        next(data)

        for row in data:
            last, first, mi, id, phone = row
            mi = mi.upper() if mi else "X"

            # Modify last name and first name to be in Capital Case
            last = last.capitalize()
            first = first.capitalize()

            # Check if id is in correct format
            id_pattern = re.compile(r"[A-Z]{2}\d{4}")
#            while not id_pattern.match(id):
 #               id = input("Invalid ID format. Please enter a valid ID: ")

            # Check if phone number is in correct format
            phone_pattern = re.compile(r"\d{3}-\d{3}-\d{4}")
  #          while not phone_pattern.match(phone):
   #             phone = input("Invalid phone number format. Please enter a valid phone number: ")

            # Create a Person object and save to dict
            person = Person(last, first, mi, id, phone)
            if id in persons:
                print("Error: Duplicate ID found.")
            else:
                persons[id] = person
    return persons

def main(args):
    # Check if file path is specified
    if len(args) < 2:
        print("Error: Please specify a file path.")
        return

    file_path = args[1]
    persons = process_file(file_path)

    # Save the dictionary as a pickle file
    with open("persons.pickle", "wb") as file:
        pickle.dump(persons, file)

    # Open the pickle file for read, and print each person
    with open("persons.pickle", "rb") as file:
        persons = pickle.load(file)
        for person in persons.values():
            person.display()

if __name__ == '__main__':
    main(sys.argv)

