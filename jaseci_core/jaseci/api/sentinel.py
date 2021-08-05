"""
Sentinel api functions as a mixin
"""
from jaseci.utils.id_list import id_list
from jaseci.actor.sentinel import sentinel
from jaseci.utils.utils import b64decode_str
import uuid


class sentinel_api():
    """
    Sentinel APIs
    """

    def __init__(self):
        self.active_snt_id = None
        self.sentinel_ids = id_list(self)

    def api_sentinel_register(self, name: str, code: str = '',
                              encoded: bool = False, set_active: bool = True):
        """
        Create blank or code loaded sentinel and return object
        """
        snt = self.sentinel_ids.get_obj_by_name(name, silent=True)
        if(not snt):
            snt = sentinel(h=self._h, name=name, code='# Jac Code')
            self.sentinel_ids.add_obj(snt)
            self.api_graph_create(set_active=True)
        if(code):
            if (encoded):
                code = b64decode_str(code)
            if (snt.code != code or not snt.is_active):
                snt.code = code
                snt.register_code()
        if(set_active):
            self.active_snt_id = snt.jid
        self.extract_snt_aliases(snt)
        return snt.serialize()

    def api_sentinel_get(self, snt: sentinel = None,
                         format: str = 'default', detailed: bool = False):
        """
        Get a sentinel rendered with specific format
        Valid Formats: {default, code, }
        """
        if(format == 'code'):
            return [snt.code]
        else:
            return snt.serialize(detailed=detailed)

    def api_sentinel_list(self, detailed: bool = False):
        """
        Provide complete list of all sentinel objects
        """
        snts = []
        for i in self.sentinel_ids.obj_list():
            snts.append(i.serialize(detailed=detailed))
        return snts

    def api_sentinel_active_set(self, snt: sentinel):
        """
        Sets the default sentinel master should use
        """
        self.active_snt_id = snt.jid
        return [f'Sentinel {snt.id} set as default']

    def api_sentinel_active_get(self, detailed: bool = False):
        """
        Returns the default sentinel master is using
        """
        if(self.active_snt_id):
            default = self._h.get_obj(uuid.UUID(self.active_snt_id))
            return default.serialize(detailed=detailed)
        else:
            return ['No default sentinel is selected!']

    def api_sentinel_delete(self, snt: sentinel):
        """
        Permanently delete sentinel with given id
        """
        self.remove_snt_aliases(snt)
        self.sentinel_ids.destroy_obj(snt)
        return [f'Sentinel {snt.id} successfully deleted']

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sentinel_ids.obj_list():
            i.destroy()
        super().destroy()
