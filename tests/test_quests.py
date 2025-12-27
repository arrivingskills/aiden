from aiden.quests import Quest, QuestLog


def test_questlog_basic_flow():
    q1 = Quest("q1", "Do thing 1")
    called = {"ok": False}

    def on_complete():
        called["ok"] = True

    q2 = Quest("q2", "Do thing 2", on_complete=on_complete)
    log = QuestLog()
    log.add(q1)
    log.add(q2)

    assert not log.all_complete()
    assert log.current().name == "q1"

    # complete first quest (no on_complete)
    log.complete_current()
    assert q1.is_complete is True
    assert log.current_index == 1

    # complete second quest and ensure callback runs
    log.complete_current()
    assert q2.is_complete is True
    assert called["ok"] is True

    # all complete now
    assert log.all_complete() is True


def test_objective_text_shows_status():
    q = Quest("qx", "Find the key")
    log = QuestLog()
    log.add(q)
    t = log.objective_text()
    assert "Find the key" in t
    assert "(done)" not in t
    q.is_complete = True
    assert "(done)" in log.objective_text()
