from nommy import Data


def test_chomp_bits_le_unsigned():
    d = Data(b'\x00\x80\x01\x00')
    assert d.chomp_bits(8) == 0x0
    assert d.chomp_bits(8) == 0x80
    assert d.chomp_bits(16) == 0x0001


def test_chomp_bits_le_unsigned_unaligned():
    d = Data(b'\x0f\x80\x01\xf8')
    assert d.chomp_bits(4) == 0x0
    assert d.chomp_bits(4) == 0x0f
    assert d.chomp_bits(1) == 0x1
    assert d.chomp_bits(7) == 0x0
    assert d.chomp_bits(7) == 0x0
    assert d.chomp_bits(1) == 0x1
    assert d.chomp_bits(1) == 0x1
    assert d.chomp_bits(3) == 0b111
    assert d.chomp_bits(2) == 0b10
    assert d.chomp_bits(2) == 0b00
