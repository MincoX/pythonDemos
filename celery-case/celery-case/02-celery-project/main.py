import tasks

if __name__ == '__main__':
    res = tasks.add.delay(5, 20)
    print(res.id)
