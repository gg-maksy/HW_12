from collections import UserDict
import json
from json import JSONDecodeError



class FieldNote:
    def __init__(self, value):

        if not isinstance(value, str):
            raise ValueError('Value must be a string')
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self)
    
    def to_json(self):
        return self.__str__()


class Note(FieldNote):

    def __init__(self, name, text, tags=None):
        self.name = name
        self.text = text
        self.tags = [*tags.value] if tags else []

    def add_tag(self, tag):
        if isinstance(tag, list):
            self.tags.extend(tag)
        elif len(tag) == 0:
            self.tags = []
        else:
            self.tags.append(tag)


class NameNote(FieldNote):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not isinstance(value, str):
            raise ValueError('Must be a string')
        if len(value) < 1:
            raise ValueError('Name must be more than 0 characters')
        if len(value) > 15:
            raise ValueError('Name must be less than 15 characters')
        self.__value = value



class Text(FieldNote):
    def __init__(self, value):
        self.value = value


class Tag(FieldNote):
    def __init__(self, value):
            self.value = value

class NoteEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Note):
            return obj.__dict__
    
        return obj.to_json()


class NoteBook(UserDict):

    def add_notes(self, note:Note):
        self.data[note.name.value] = note
        
    # def add_tag(self, tag:Tag):

    #     for i, p in enumerate(self):
    #         if p.value == old_phone.value:
    #             self.phones[i] = new_phone

    #     return f'Change {old_phone} to {new_phone}'

    def paginator(self, iter_obj, page=1):
        start = 0

        while True:
            
            result_keys = list(iter_obj)[start:start + page]
            result = ' '.join([f'{k}: {iter_obj.get(k).text.value}' for k in result_keys])
            if not result:
                break
            yield result
            start += page

    def recover_from_file(self):
        try:
            with open('notes_book.json') as fd:
                data = json.load(fd)
        except (FileNotFoundError, AttributeError, JSONDecodeError, ValueError):
            return {}

        for k, v in data.items():
            if v['tags']:
                self.add_notes(Note(NameNote(v['name']), Text(v['text']), Tag(v['tags'])))
            else:
                self.add_notes(Note(NameNote(v['name']), Text(v['text'])))


    def save_to_file(self):

        with open('notes_book.json', "w") as fd:
            if self.data:
                json.dump(self.data, fd, cls=NoteEncoder, indent=3)