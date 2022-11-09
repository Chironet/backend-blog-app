from datetime import datetime
from config import db, app

class Person(db.Model):
	__tablename__='person'
	person_id = db.Column(db.Integer, primary_key=True)
	lname = db.Column(db.String(32), index=True)
	fname = db.Column(db.String(32))
	# timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime)
	timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
	notes = db.relationship('Note', backref='person', cascade='all, delete, delete-orphan', single_parent=True, order_by='desc(Note.timestamp)')


	def __init__(self, lname, fname):
		self.lname = lname
		self.fname = fname
	
	def to_json(self):
		return {'person_id': self.person_id,
				'lname' : self.lname,
				'fname' : self.fname,
				'timestamp' : str(self.timestamp)}
	


class Note(db.Model):
	__tablename__='note'
	note_id = db.Column(db.Integer, primary_key=True)
	person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
	content = db.Column(db.String(300), nullable=False)
	timestamp = db.Column(db.DateTime(), default=datetime.utcnow)

	def __init__(self, content):
		self.content = content

	def note_to_json(self):
		return {'note_id': self.note_id,
				'person_id' : self.person_id,
				'content' : self.content,
				'timestamp' : str(self.timestamp)}

with app.app_context():
	db.create_all()
	db.session.commit()

