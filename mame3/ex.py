class aa():

    a = 'a'
    b = 'b'
    boo = False
    d = 'd'
    if a == b: boo = True

    ls = []
    ls.append('aaa')
    ls.append('bbb')
    ls.append('ccc')

    for i in range(0, 3):
        print(i)
        print(ls[i])


    def newCar(width, height):

        def inNewCar():
            print('inNewCar>>'+d)

        c = width * height
        # global d
        global d
        d = '555'

        inNewCar()
        return c

    def pd():
        print('pd>>>'+d)

    print(newCar(2,3))
    print(boo)
    pd()
    print(d)
