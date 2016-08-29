#coding=UTF-8
class Region(object):
	def __init__(self, region_id=None, region_name=None):
		# The unique ID of the Region.
		self.id = region_id
		# The local name of the Region.
		self.name = region_name