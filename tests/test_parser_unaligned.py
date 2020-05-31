from nommy import parser, le_u


@parser
class LESimple:
    u8_1: le_u(8)
    # 1 byte
    u4_1: le_u(4)
    u4_2: le_u(4)
    # 2 byte
    u3_1: le_u(3)
    u1_1: le_u(1)
    u3_2: le_u(3)
    u1_2: le_u(1)
    # 3 byte
    u5_1: le_u(5)
    u3_3: le_u(3)
    # 4 byte
    u16_1: le_u(16)
    # 6 byte


def test_lesimple_ff():
    data, rest = LESimple.parse(b'\xff' * 8)
    assert data == LESimple(
        u8_1=0xff,
        u4_1=0x0f,
        u4_2=0x0f,
        u3_1=0x07,
        u1_1=0x01,
        u3_2=0x07,
        u1_2=0x01,
        u5_1=0x1f,
        u3_3=0x07,
        u16_1=0xffff,
    )
    assert rest == b'\xff\xff'
