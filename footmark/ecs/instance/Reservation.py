class Reservation(object):
	def __init__():
		# The unique ID of the Reservation.
		self.id = ''

		# The unique ID of the owner of the Reservation.
		self.owner_id = ''

		# A list of Group objects representing the security groups associated with launched instances.
		self.groups = []

		# A list of Instance objects launched in this Reservation.
		self.instances = []


	def endElement(name, value, connection):
		pass
	
	def startElement(name, attrs, connection):
		pass

	def stop_all(dry_run=False):
		pass