
"""
Represents an ECS Instance
"""

from footmark.ecs.ecsobject import *

class Instance(TaggedECSObject):
    """
    Represents an instance.
    """

    def __init__(self, connection=None):
        super(Instance, self).__init__(connection)
        # self.connection = connection


    def __repr__(self):
        return 'Instance:%s' % self.id

    @property
    def id(self):
        return self.instance_id

    @property
    def state(self):
        return self.status

    @property
    def vpc_id(self):
        if self.vpc_attributes:
            return self.vpc_id

    @property
    def vswitch_id(self):
        return self.v_switch_id

    @property
    def private_ip(self):
        return self.private_ip_address['IpAddress']

    @property
    def eip(self):
        if self.eip_attributes:
            return self.eip_attributes_attributes.eip_address



    def _update(self, updated):
        self.__dict__.update(updated.__dict__)

    def update(self, validate=False):
        """
        Update the instance's state information by making a call to fetch
        the current instance attributes from the service.

        :type validate: bool
        :param validate: By default, if ECS returns no data about the
                         instance the update method returns quietly.  If
                         the validate param is True, however, it will
                         raise a ValueError exception if no data is
                         returned from ECS.
        """
        rs = self.connection.get_all_instances([self.id])
        if len(rs) > 0:
            for r in rs:
                if r.id == self.id:
                    self._update(r)
        elif validate:
            raise ValueError('%s is not a valid Instance ID' % self.id)
        return self.state

    def terminate(self):
        """
        Terminate the instance
        """
        rs = self.connection.terminate_instances([self.id])
        if len(rs) > 0:
            self._update(rs[0])

    def stop(self, force=False):
        """
        Stop the instance

        :type force: bool
        :param force: Forces the instance to stop

        :rtype: list
        :return: A list of the instances stopped
        """
        rs = self.connection.stop_instances([self.id], force)
        # if len(rs) > 0:
        #     self._update(rs[0])

    def start(self):
        """
        Start the instance.
        """
        rs = self.connection.start_instances([self.id])
        # if len(rs) > 0:
        #     self._update(rs[0])

    def reboot(self, force=False):
        return self.connection.reboot_instances([self.id], force)
