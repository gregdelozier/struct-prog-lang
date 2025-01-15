def eval(s):
    for c in s:
        assert c in "-0123456789."
    n = 0
    if s[0] == '-':
        sign = -1
        s = s[1:]
    else:
        sign = 1
    multi = 1.0
    fractional = False
    assert len(s) > 0
    assert s != '.'
    while len(s) > 0:
        assert s[0] != '-'
        if s[0] == ".":
            assert fractional == False
            fractional = True
        else:
            if not fractional:
                n = n * 10 + ord(s[0]) - ord("0")
            else:
                multi = multi / 10
                n = n + (ord(s[0]) - ord("0")) * multi
        s = s[1:]        
    return n * sign

def test_eval():
    """ test eval """
    print("testing eval()")
    assert eval("0") == 0, "Expect 0 to be 0"
    assert eval("1") == 1
    assert eval("99") == 99
    assert eval("1099") == 1099
    assert eval("0001") == 1
    assert eval("-99") == -99
    assert eval("1.") == 1
    assert eval("1.23") == 1.23
    assert eval("-1.23") == -1.23
    try:
        eval("1..2")
        assert False, "No error for 1..2"
    except Exception as e:
        print("got an error for 1..2")
    try:
        eval(" 1")
        assert False, "No error for [ 1]"
    except Exception as e:
        print("got an error for [ 1]")
    try:
        eval("--1")
        assert False, "No error for [--1]"
    except Exception as e:
        print("got an error for [--1]")

if __name__ == "__main__":
    test_eval()
    print("done.")