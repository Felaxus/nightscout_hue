from twisted.internet import task, reactor


def main():
    print('lmao')


if __name__ == '__main__':
    task.LoopingCall(main).start(2)
    reactor.run()