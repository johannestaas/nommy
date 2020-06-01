from enum import Enum

from nommy import le_enum, parser, string, le_u8, repeating


@le_enum(2)
class Type(Enum):
    null = 0
    foo = 1
    bar = 2
    baz = 3


@le_enum(6)
class OtherType(Enum):
    null2 = 0
    foo2 = 1
    bar2 = 2
    baz2 = 3


@parser
class Header:
    magic: string(8)
    some_type: Type
    other_type: OtherType
    person_ct: le_u8


@parser
class Person:
    first_name: string(None)
    last_name: string(None)


@parser
class PersonRecord:
    header: Header
    people: repeating(Person, 'header.person_ct')


def test_nested_header_body():
    # \x42 is type "foo" and "bar2"
    data, rest = PersonRecord.parse(b'UNITTEST\x42\x02joe\0blow\0toe\0schmo\0')
    assert data.header.magic == 'UNITTEST'
    assert data.header.some_type == Type.foo
    assert data.header.other_type == OtherType.bar2
    assert data.header.person_ct == 2
    assert data.people[0].first_name == 'joe'
    assert data.people[0].last_name == 'blow'
    assert data.people[1].first_name == 'toe'
    assert data.people[1].last_name == 'schmo'


@parser
class Group:
    person_ct: le_u8
    people: repeating(Person, 'person_ct')


@parser
class GroupRoot:
    group_ct: le_u8
    groups: repeating(Group, 'group_ct')


def test_nested_repeating():
    data, rest = GroupRoot.parse(
        b'\x02\x03foo\0bar\0fizz\0buzz\0nolast\0\0\x01hello\0world\0rest'
    )
    assert rest == b'rest'
    assert data.group_ct == 2
    assert data.groups[0].person_ct == 3
    assert data.groups[0].people[0] == Person(first_name='foo', last_name='bar')
    assert data.groups[0].people[1] == Person(first_name='fizz', last_name='buzz')
    assert data.groups[0].people[2] == Person(first_name='nolast', last_name='')
    assert data.groups[1].person_ct == 1
    assert data.groups[1].people[0] == Person(first_name='hello', last_name='world')


@parser
class GroupHeader:
    other: le_u8
    group_ct: le_u8


@parser
class GroupHeaderCtr:
    another: le_u8
    header: GroupHeader


@parser
class GroupNoCount:
    groups: repeating(Group, 'header_ctr.header.group_ct')


@parser
class GroupNoCountCtr:
    group_no_count: GroupNoCount
    last_byte: le_u8


@parser
class GroupRootCtr:
    header_ctr: GroupHeaderCtr
    group_no_count_ctr: GroupNoCountCtr


def test_nested_containers():
    data, rest = GroupRootCtr.parse(
        # 2 group count, with some other random bytes
        b'\x11\x22\x02'
        # Group 1
        b'\x03joe\0blow\0toe\0scmoe\0foo\0bar\0'
        # Group 2
        b'\x04a\0\0b\0\0c\0d\0eee\0fff\0'
        # last_byte
        b'\xff'
        # rest
        b' the rest'
    )
    assert rest == b' the rest'
    assert data.header_ctr.another == 0x11
    assert data.header_ctr.header.other == 0x22
    assert data.header_ctr.header.group_ct == 2
    group = data.group_no_count_ctr.group_no_count.groups[0]
    assert group.person_ct == 3
    assert group.people[0] == Person(first_name='joe', last_name='blow')
    assert group.people[1] == Person(first_name='toe', last_name='scmoe')
    assert group.people[2] == Person(first_name='foo', last_name='bar')
    group = data.group_no_count_ctr.group_no_count.groups[1]
    assert group.person_ct == 4
    assert group.people[0] == Person(first_name='a', last_name='')
    assert group.people[1] == Person(first_name='b', last_name='')
    assert group.people[2] == Person(first_name='c', last_name='d')
    assert group.people[3] == Person(first_name='eee', last_name='fff')
    assert data.group_no_count_ctr.last_byte == 0xff
