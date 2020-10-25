import json
from rth.core.errors import MissingJSONTag, WrongJSONTag, MissingJSONInfo
from rth.core.dispatcher import Dispatcher
from rth.virtual_building.network_creator import NetworkCreator


class JSONAdapter:
    def __init__(self, file_path):
        self.file_path = file_path

    def __call__(self, *args, **kwargs):
        return self.evaluate()

    def evaluate(self):
        with open(self.file_path, 'r') as file:
            decoded = json.load(file)

        found_networks, found_routers, found_links, links_or_connections = False, False, False, 'Links'
        for part in decoded:
            if part == 'Networks':
                found_networks = True
            elif part == 'Routers':
                found_routers = True
            elif part == 'Links' or part == 'Connections':
                links_or_connections = 'Links' if part == 'Links' else 'Connections'
                found_links = True
            else:
                raise WrongJSONTag(part)

        if not found_routers:
            raise MissingJSONTag('Routers')
        if not found_networks:
            raise MissingJSONTag('Networks')
        if not found_links:
            raise MissingJSONTag('Links')

        # we init the instance
        inst = NetworkCreator()

        # we create the dictionary of all subnetworks
        subnetworks = {}
        for name in decoded['Networks']:
            net = decoded['Networks'][name]

            if "cidr" in net:
                # we found a CIDR, so we split it and return the network
                subnetworks[name] = net['cidr']
            elif "ip" in net and "mask" in net:
                # we found an IP and a mask
                ip, mask = net['ip'], net['mask']
                subnetworks[name] = f"{ip}/{mask}"
            else:
                # missing a cidr tag or a couple IP/mask
                raise MissingJSONInfo('Networks', str(name), "CIDR or IP/mask couple")

        # then we create the dictionary of all routers
        routers = {}
        for name in decoded['Routers']:
            router = decoded['Routers'][name]

            if router and "internet" in router:
                routers[name] = True
            else:
                routers[name] = None

        # finally, we link all things between them
        list_ = decoded['Links'] if links_or_connections == 'Links' else decoded['Connections']

        # Now we pass the instance onto the dispatcher
        dispatch = Dispatcher()
        dispatch.execute(subnetworks=subnetworks, routers=routers, links=list_)

        return dispatch