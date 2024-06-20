from typing import Any
from MooToo.construct import Construct, ConstructType
from MooToo.ship import Ship, ShipType, select_ship_type_by_name
from MooToo.constants import Building

MAX_QUEUE = 6


#################################################################################################
class BuildQueue:
    def __init__(self):
        self._index = -1
        self._queue: list[Construct] = []

    #############################################################################################
    def __repr__(self):
        return f"<BuildQueue {len(self._queue)}: {', '.join([str(_) for _ in self._queue])}>"

    #############################################################################################
    def __bool__(self):
        return len(self._queue) != 0

    #############################################################################################
    def __len__(self):
        return len(self._queue)

    #############################################################################################
    def __iter__(self):
        self._index = -1
        return self

    #############################################################################################
    def __next__(self):
        self._index += 1
        try:
            return self._queue[self._index]
        except IndexError as e:
            raise StopIteration from e

    #############################################################################################
    def __getitem__(self, item):
        return self._queue[item]

    #############################################################################################
    def __contains__(self, item):
        if isinstance(item, Building):
            return bool([_ for _ in self._queue if _.tag == item])
        if isinstance(item, Construct):
            return bool([_ for _ in self._queue if _ == item])
        return False

    #############################################################################################
    @property
    def cost(self) -> int:
        return self._queue[0].cost

    #############################################################################################
    def pop(self, index=0) -> Construct:
        return self._queue.pop(index)

    #############################################################################################
    def is_building(self, building: Building) -> bool:
        if not self._queue:
            return False
        return self._queue[0].category == ConstructType.BUILDING and self._queue[0].tag == building

    #############################################################################################
    def toggle(self, construct: Any) -> None:
        if isinstance(construct, Building):
            con = Construct(ConstructType.BUILDING, building_tag=construct)
        elif isinstance(construct, Construct):
            con = construct
        elif isinstance(construct, Ship):
            con = Construct(ConstructType.SHIP, ship=construct)
        elif isinstance(construct, ShipType):
            ship = select_ship_type_by_name(construct.name)
            con = Construct(ConstructType.SHIP, ship=ship)
        else:
            raise NotImplementedError(f"build_queue.toggle({construct=}) Unknown type {type(construct)}")

        if con.category == ConstructType.BUILDING and con in self._queue:
            self._queue.remove(con)
        else:
            self.add(con)

    #############################################################################################
    def add(self, obj: Building | Ship | Construct) -> None:
        if len(self._queue) >= MAX_QUEUE:
            return
        if isinstance(obj, Building):
            con = Construct(ConstructType.BUILDING, building_tag=obj)
        elif isinstance(obj, Ship):
            con = Construct(ConstructType.SHIP, ship=obj)
        elif isinstance(obj, Construct):
            con = obj
        else:
            raise NotImplementedError(f"build_queue.add({obj=}) Unknown type {type(obj)}")
        self._queue.append(con)
