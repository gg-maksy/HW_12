from operation import AdressBook, Record, Name, Phone, Birthday
from notes import Note, NameNote, NoteBook, Text

adress_book = AdressBook()
adress_book.recover_from_file()
note_book = NoteBook()
note_book.recover_from_file()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError:
            return 'Not enough params. Type help.'
    return inner


@input_error
def list_of_params(*args):
    conteiner = args[0].split()

    if not conteiner:
        raise ValueError
    
    return conteiner


def help(*args):
    return """
Show all contacts -- enter /show all
Add a new contact -- enter /add
Get contact -------- enter /phone [Name]
Get Birthday ------- enter /birthday [Name]
Change number ------ enter /change contact [Name] [current number] [new number]
Remove contact ----- enter /remove [Name]
Add a new note ----- enter /notes
Show all notes ----- entet /show notes
For exit ----------- enter .
"""


def hello(*args):
    return 'How can I help you? For more information - enter /help'


@input_error
def add(*args):
    lst = list_of_params(*args)
    if len(lst) >= 2:
            
        name = Name(lst[0])
        numb_of_phone = Phone(int(lst[1]))
        birthday = None
        if len(lst) == 3:
            birthday = Birthday(lst[2])
        new_contact = Record(name, numb_of_phone, birthday)

        if lst[0] in [k for k in adress_book.keys()]:
            
            val = adress_book.get(lst[0])
            if lst[1] in [str(i) for i in val.phones]:
                if len(lst) == 3:
                    val.add_birthday(Birthday(lst[2]))
                    return f'Contact {name} was update'
                return f'This number is alredy yet in contact {name}'
            
            val.add_phone(Phone(int(lst[1])))

            if len(lst) == 3:
                val.add_birthday(Birthday(lst[2]))
            return f'Contact {name} was update'

        if not lst[0] in [k for k in adress_book.keys()]:
            adress_book.add_contact(new_contact)
            return f'Contact {name} was added'
        
    else:
        raise ValueError


def exit(*args):
    adress_book.save_to_file()
    note_book.save_to_file()
    return 'Bye'


def no_command(*args):
    return 'Unknown command. Try again'


def show_all(*args):
    gen_obj = adress_book.paginator(adress_book)
    for i in gen_obj:
        print('*' * 50)
        print(i)
        input('Press any key')
    return "You don't have more contacts"


@input_error
def get_birthday(*args):
    lst = list_of_params(*args)
    val = adress_book.get(lst[0])
    return val.days_to_birthday()


@input_error
def get_number(*args):
    lst = list_of_params(*args)
    list_of_contacts = {}
    
    for k, v in adress_book.items():
        if lst[0] == k:
            return f'{lst[0]}: {str(*v.phones)}'
        
        if str(*v.phones).startswith(lst[0]):
            list_of_contacts.update({k: str(*v.phones)})
        
        if k.startswith(lst[0]):
            list_of_contacts.update({k: str(*v.phones)})

    if list_of_contacts:
        return list_of_contacts
    return f'Not contacts {lst[0]}'


@input_error
def change_contact(*args):
    lst = list_of_params(*args)

    if len(lst) == 3:
        if lst[0] in [k for k in adress_book.keys()]:
            adress_book.get(lst[0]).change_phone(Phone(int(lst[1])), Phone(int(lst[2])))
        return f'Contact {lst[0]} was change'
    
    else:
        raise ValueError


def remove_contact(*args):
    adress_book.pop(args[0])
    return f'Contact {args[0]} was delete'


@input_error
def add_note(*args):
    lst = list_of_params(*args)

    if len(lst) > 1:
        note_book.add_notes(Note(NameNote(lst[0]), Text(' '.join(lst[1:]))))
        # tag = input('Please enter the tag for this note')

        if lst[0] in [k for k in note_book.keys()]:
            note_book.get(lst[0]).add_tag(input('Please enter the tag for this note: ').split(', '))

        return f'Note {lst[0]} was added'
    else:
        raise ValueError


def show_notes(*args):
    gen_obj = note_book.paginator(note_book)
    for i in gen_obj:
        print('*' * 50)
        print(i)
        input('Press any key')
    return "You don't have more notes"

@input_error
def add_tag(*args):
    lst = list_of_params(*args)
    print(lst[0])
    if len(lst) > 1:
        note_book.get(lst[0]).add_tag(lst[1:])
        return f'Note {lst[0]} was update'
    else:
        raise ValueError
    
@input_error
def get_notes(*args):
    lst = list_of_params(*args)
    list_of_notes = {}
    
    for k, v in note_book.items():
        if lst[0] == k:
            return f'{lst[0]}: {v.text}'
        
        if str(v.text).startswith(lst[0]):
            list_of_notes.update({k: v.text})
        
        if k.startswith(lst[0]):
            list_of_notes.update({k: v.text})

    if list_of_notes:
        return list_of_notes
    return f'Not notes that start with {lst[0]}'


def remove_note(*args):
    note_book.pop(args[0])
    return f'Note {args[0]} was delete'

COMMANDS = {help: '/help',
            add: '/add contact',
            exit: '.',
            show_all: '/show all',
            get_number: '/phone',
            get_birthday: '/birthday',
            change_contact: '/change contact',
            remove_contact: '/remove contact',
            add_note: '/add note',
            show_notes: '/show notes',
            add_tag: '/add tag',
            remove_note: '/remove note',
            get_notes: '/note',
            hello: 'hello'}


def command_handler(text: str):

    for command, kword in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, '').strip()
        
    return no_command, None


def main():

    while True:

        user_input = input('>>> ')
        if user_input in ('.', 'good bye', 'close', 'exit'):
            print(exit())
            break

        command, data = command_handler(user_input)
        print(command(data))



if __name__ == '__main__':
    main()

    