import shelve

# Opening up remindme db
remind_db = shelve.open("reminder_db", writeback=True)


def loader():
    remind_db["new_reminders"] = []
    remind_db["reminders"] = []
    remind_db.close()

def viewer():

    for key, item in remind_db.items():
        print(key, item)

    remind_db.close()


def remover():

    del remind_db["reminders"][0:1]

    remind_db.close()


def test_one():

    R = remind_db["reminders"][0]

    remind_db.close()
    return R

def test_two(obj):

    remind_db = shelve.open("reminder_db", writeback=True)

    print(obj == remind_db["reminders"][0])

    # remind_db["reminders"].remove(obj)

    remind_db.close()


if __name__ == "__main__":

    viewer()
