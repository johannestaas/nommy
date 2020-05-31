from enum import Enum

from nommy import le_enum, parser


@le_enum(4)
class BikeType(Enum):
    regular = 0
    cruiser = 1
    sports = 2
    all_terrain = 3
    dual_sport = 4
    cafe_racer = 5
    touring = 6
    trike = 7


@le_enum(8)
class Destination(Enum):
    san_francisco = 1
    los_angeles = 2
    oakland = 3


@parser
class BikerGroup:
    dest: Destination
    leader: BikeType
    bike2: BikeType
    bike3: BikeType
    bike4: BikeType


def main():
    group, rest = BikerGroup.parse(b'\x01\x14\x25')
    print(f'group is: {group!r}')


if __name__ == '__main__':
    main()
