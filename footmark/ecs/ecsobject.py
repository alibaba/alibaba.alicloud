
class ECSObject(object):

    def __init__(self, connection=None):
        self.connection = connection
        if self.connection and hasattr(self.connection, 'region'):
            self.region = connection.region
        else:
            self.region = None

class TaggedECSObject(ECSObject):
    """
    Any EC2 resource that can be tagged should be represented
    by a Python object that subclasses this class.  This class
    has the mechanism in place to handle the tagSet element in
    the Describe* responses.  If tags are found, it will create
    a TagSet object and allow it to parse and collect the tags
    into a dict that is stored in the "tags" attribute of the
    object.
    """

    def __init__(self, connection=None):
        super(TaggedEC2Object, self).__init__(connection)
