from flask import make_response, abort
from config import db
from models import Person, Note#, NoteSchema


def read_all():

    notes = Note.query.order_by(db.desc(Note.timestamp)).all()

    return [note.to_json() for note in notes]


def read_one(person_id, note_id):

    note = (Note.query.join(Person, Person.person_id == Note.person_id).filter(Person.person_id == person_id).filter(Note.note_id == note_id).one_or_none())

    if note is not None:
        return note.to_json()

    else:
        abort(404, f"Note not found for Id: {note_id}")


def create(person_id, note):

    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is None:
        abort(404, f"Person not found for Id: {person_id}")

    new_note = Note(content=note['content'])

    person.notes.append(new_note)
    db.session.commit()

    data = new_note.note_to_json()

    return data, 201


def update(person_id, note_id, note):

    update_note = (Note.query.filter(Person.person_id == person_id).filter(Note.note_id == note_id).one_or_none())

    if update_note is not None:

        update_note.content = note['content']


        # update.person_id = update_note.person_id
        # update.note_id = update_note.note_id

        db.session.commit()

        data = update_note.note_to_json()

        return data, 200

    else:
        abort(404, f"Note not found for Id: {note_id}")


def delete(person_id, note_id):

    note = (Note.query.filter(Person.person_id == person_id).filter(Note.note_id == note_id).one_or_none())

    if note is not None:
        db.session.delete(note)
        db.session.commit()
        return make_response(
            "Note {note_id} deleted".format(note_id=note_id), 200
        )

    else:
        abort(404, f"Note not found for Id: {note_id}")