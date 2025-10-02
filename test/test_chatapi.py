from chatapi.core import Client, Room, Message
# Many of these unit tests are from ChatExchange


def test_get_current_user_ids():
    all([isinstance(user_id, int) for user_id in Room(1).get_current_user_ids()])


def test_get_message():
    # test a message
    msg = Client().get_message(68274952)
    assert isinstance(msg, Message)
    assert msg.id == 68274952
    assert msg.content == "Makyen/EC2-linux: Executing automatic scheduled reboot"
    assert msg.content_source == msg.content

    # test its parent
    assert isinstance(msg.parent, Message)
    assert msg.parent.id == 15358991
    assert msg.parent.text_content == "@bot forever in my tests"


def test_get_user():
    # test with the Feeds user
    user = Client().get_user(-2)
    assert user.id == -2
    assert user.name == "Feeds"

    # test with the SmokeDetector user
    user = Client("stackoverflow.com").get_user(3735529)
    assert user.id == 3735529
    assert user.name == "SmokeDetector"
