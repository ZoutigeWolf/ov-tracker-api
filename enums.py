from enum import IntEnum


class WheelchairAccesibility(IntEnum):
    NoInformation = 0
    AtLeastOne = 1
    NotPossible = 2


class BikeAccesibility(IntEnum):
    NoInformation = 0
    AtLeastOne = 1
    NotPossible = 2


class ExceptionType(IntEnum):
    Added = 1
    Removed = 2


class RouteType(IntEnum):
    Tram = 0
    Subway = 1
    Rail = 2
    Bus = 3
    Ferry = 4
    CableTram = 5
    Aerial = 6
    Funicular = 7
    TrolleyBus = 11
    Monorail = 12


class WheelchairBoarding(IntEnum):
    NoInformation = 0
    SomeVehicles = 1
    NotPossible = 2


class LocationType(IntEnum):
    StopPlatform = 0
    Station = 1
    EntranceExit = 2
    GenericNode = 3
    BoardingArea = 4


class PickupType(IntEnum):
    Scheduled = 0
    NoPickup = 1
    PhoneAgency = 2
    CoordinateWithDriver = 3


class DropOffType(IntEnum):
    Scheduled = 0
    NoDropOff = 1
    PhoneAgency = 2
    CoordinateWithDriver = 3


class Timepoint(IntEnum):
    Approximate = 0
    Exact = 1


class TransferType(IntEnum):
    Recommended = 0
    Timed = 1
    Minimum = 2
    NotPossible = 3
    InSeat = 4
    ReBoard = 5


class VehicleStatus(IntEnum):
    IncomingAt = 0
    StoppedAt = 1
    InTransitTo = 2


class ScheduleRelationship(IntEnum):
    Scheduled = 0
    Added = 1
    Unscheduled = 2
    Canceled = 3
    Duplicated = 4
    Deleted = 5
