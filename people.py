from flask import make_response, abort
from config import db
from models import Person, Note#, PersonSchema
import requests

def read_all():
	people = Person.query.order_by(Person.lname).all()
	return [person.to_json() for person in people]


def read_one(person_id):
	person = Person.query.filter(Person.person_id == person_id).outerjoin(Note).one_or_none()

	if person is not None:
		return person.to_json()

	else:
		abort(404, 'Person not fount for Id:{person_id}'.format(person_id=person_id))


def create(person):
	
	fname=person.get('fname')
	lname=person.get('lname')

	existing_person = Person.query.filter(Person.fname == fname).filter(Person.lname == lname).one_or_none()

	if existing_person is None:
		new_person = Person(lname=person['lname'],
							fname=person['fname'])

		db.session.add(new_person)
		db.session.commit()

		data = new_person.to_json()

		return data, 201

	else:
		abort(409, 'Person {fname} {lname} already exists'.format(fname=fname, lname=lname))



def update(person_id, person):
    update_person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if update_person is not None:

        update_person.lname = person['lname']
        update_person.fname = person['fname']
        
        db.session.commit()

        data = update_person.to_json()

        return data, 200

    else:
        abort(404, f"Person not found for Id: {person_id}")




def delete(person_id):

	person = Person.query.filter(Person.person_id == person_id).one_or_none()

	if person is not None:
		db.session.delete(person)
		db.session.commit()
		return make_response("Person {person_id} deleted".format(person_id=person_id), 200)

	else:
		abort(404, "Person not found for Id: {person_id}".format(person_id=person_id))