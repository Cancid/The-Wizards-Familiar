from threading import Timer

timeout = 10
t = Timer(timeout, print, ['Sorry, times up'])
t.start()
prompt = "You have %d seconds to choose the correct answer...\n" % timeout
answer = input(prompt)
while answer not in 'y':
    print('Incorrect!')
    break
else:
    t.cancel()
    print('You did it!')
