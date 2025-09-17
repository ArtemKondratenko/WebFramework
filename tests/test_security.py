from webframework.security import BasicHTTPAuthCredentials

# parse


# Aladdin:open sesame
def test_parse_basic_http_auth_credentials() -> None:
    line = " Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    basic = BasicHTTPAuthCredentials.parse(line)
    assert basic.login == "Aladdin"
    assert basic.password == "open sesame"
