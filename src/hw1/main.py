import sys
import re

# Compile regex patterns
ID_PATTERN = re.compile('\w\w\d\d')
PHONE_PATTERN = re.compile('\d{3}-\d{3}-\d{4}')


class Person:
    '''
    Stores the information for a single Person
    '''
    last: str
    first: str
    mi: str
    id: str
    phone: str

    def __init__(self, last: str, first: str, mi: str, id: str, phone: str):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        '''
        Displays the person object
        '''
        print('Employee id: ', self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone, '\n')


def get_datafile_path() -> str:
    '''
    Reads in the datafile path from the command line arguments
    and returns an error if not found
    '''
    # Check to make sure datafile path is defined
    if len(sys.argv) < 2:
        print('Error: no datafile path defined in the command line arguments')
        sys.exit(1)

    return sys.argv[1]


def process_name(name: str) -> str:
    '''
    Captializes the name
    '''
    return name.title()


def process_middle(mi: str) -> str:
    '''
    Captializes the initial and replaces with X if not present
    ''' 
    return mi.upper() if mi else 'X'


def process_id(id: str) -> str:
    '''
    Make sure ID is correct and reprompt if not
    '''
    while not ID_PATTERN.match(id):
        print('ID invalid: ', id)
        print('ID is two letters followed by 4 digits')
        id = input('Please enter a valid id: ')

    return id


def process_phone(phone: str) -> str:
    '''
    Make sure ID is correct and reprompt if not
    '''
    while not PHONE_PATTERN.match(phone):
        print('Phone # invalid: ', phone)
        print('Enter phone number in form 123-456-7890')
        phone = input('Enter phone number: ')

    return phone


def process_input_file(file_path: str) -> list[Person]:
    '''
    Process the input file by reading in the CSV and
    processing each line, splitting by the commas
    '''
    # Instatiate an dict to return
    output = {}

    # Open the file
    with open(file_path) as file:
        # Use boolean variable to ignore the first line (header)
        first_row = True

        # Iterate through each line in the file
        for line in file:
            # Ignore the first line
            if first_row:
                first_row = False
                continue
            
            print(line)

            # Split each other line by commas
            split = line.split(',')
            last = process_name(split[0])
            first = process_name(split[1])
            mi = process_middle(split[2])
            id = process_id(split[3])
            phone = process_phone(split[4])

            # Check to make sure no duplicate ID
            if id in output:
                print("Error: Duplicated ID", id, "found")

            # Add to output dict
            output.update({ id: Person(last, first, mi, id, phone) })

    # Return the filled person array
    return output


def main():
    '''
    Main routine
    '''
    # Get the datafile path
    datafile_path = get_datafile_path()

    # Read the datafile and return an array of Person objects
    people = process_input_file(datafile_path)

    print(people)
    for p in people:
        p.display()

if __name__ == '__main__':
    main()
