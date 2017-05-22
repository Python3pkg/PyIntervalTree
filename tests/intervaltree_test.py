'''
PyIntervalTree: A mutable, self-balancing interval tree.

Test module

Copyright 2014, Chaim-Leib Halbert et al.
Most recent fork and modifications by Konstantin Tretyakov

Licensed under LGPL.
'''

def test_issue5():
    # Issue #5, https://github.com/konstantint/PyIntervalTree/issues/5
    from intervaltree import IntervalTree
    t = IntervalTree()
    t.addi(-46.0, 31.0, 'test')
    t.addi(-20.0, 29.0, 'test')
    t.addi(1.0, 9.0, 'test')
    t.addi(-3.0, 6.0, 'test')
    t.removei(1.0, 9.0, 'test')
    t.removei(-20.0, 29.0, 'test')
    t.removei(-46.0, 31.0, 'test')
    assert len(t) == 1
    
def test_emptytree():
    # Issue #3, https://github.com/konstantint/PyIntervalTree/issues/3
    from intervaltree import IntervalTree
    t = IntervalTree()
    assert len(t) == 0
    assert t[1:3] == set([])
    assert t[1] == set([])

def test_all():
    from intervaltree import Interval, IntervalTree
    from pprint import pprint
    from operator import attrgetter
    
    def makeinterval(lst):
        return Interval(
            lst[0], 
            lst[1], 
            "{}-{}".format(*lst)
            )
    
    ivs = list(map(makeinterval, [
        [1,2],
        [4,7],
        [5,9],
        [6,10],
        [8,10],
        [8,15],
        [10,12],
        [12,14],
        [14,15],
        ]))
    t = IntervalTree(ivs)
    t.verify()
    
    def data(s): 
        return set(map(attrgetter('data'), s))
    
    # Query tests
    print('Query tests...')
    assert data(t[4])          == set(['4-7'])
    assert data(t[4:5])        == set(['4-7'])
    assert data(t[4:6])        == set(['4-7', '5-9'])
    assert data(t[9])          == set(['6-10', '8-10', '8-15'])
    assert data(t[15])         == set()
    assert data(t.search(5))   == set(['4-7', '5-9'])
    assert data(t.search(6, 11, strict = True)) == set(['6-10', '8-10'])
    
    print('    passed')
    
    # Membership tests
    print('Membership tests...')
    assert ivs[1] in t
    assert Interval(1,3, '1-3') not in t
    assert t.overlaps(4)
    assert t.overlaps(9)
    assert not t.overlaps(15)
    assert t.overlaps(0,4)
    assert t.overlaps(1,2)
    assert t.overlaps(1,3)
    assert t.overlaps(8,15)
    assert not t.overlaps(15, 16)
    assert not t.overlaps(-1, 0)
    assert not t.overlaps(2,4)
    print('    passed')
    
    # Insertion tests
    print('Insertion tests...')
    t.add( makeinterval([1,2]) )  # adding duplicate should do nothing
    assert data(t[1])        == set(['1-2'])
    
    t[1:2] = '1-2'                # adding duplicate should do nothing
    assert data(t[1])        == set(['1-2'])
    
    t.add(makeinterval([2,4]))
    assert data(t[2])        == set(['2-4'])
    t.verify()
    
    t[13:15] = '13-15'
    assert data(t[14])       == set(['8-15', '13-15', '14-15'])
    t.verify()
    print('    passed')
    
    # Duplication tests
    print('Interval duplication tests...')
    t.add(Interval(14,15,'14-15####'))
    assert data(t[14])        == set(['8-15', '13-15', '14-15', '14-15####'])
    t.verify()
    print('    passed')
    
    # Copying and casting
    print('Tree copying and casting...')
    tcopy = IntervalTree(t)
    tcopy.verify()
    assert t == tcopy
    
    tlist = list(t)
    for iv in tlist:
        assert iv in t
    for iv in t:
        assert iv in tlist
    
    tset = set(t)
    assert tset == list(t.items())
    print('    passed')
    
    # Deletion tests
    print('Deletion tests...')
    try:
        t.remove(
            Interval(1,3, "Doesn't exist")
            )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
    
    try:
        t.remove(
            Interval(500, 1000, "Doesn't exist")
            )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
    
    orig = t.print_structure(True)
    t.discard( Interval(1,3, "Doesn't exist") )
    t.discard( Interval(500, 1000, "Doesn't exist") )
    
    assert data(t[14])        == set(['8-15', '13-15', '14-15', '14-15####'])
    t.remove( Interval(14,15,'14-15####') )
    assert data(t[14])        == set(['8-15', '13-15', '14-15'])
    t.verify()
    
    assert data(t[2])        == set(['2-4'])
    t.discard( makeinterval([2,4]) )
    assert data(t[2])        == set()
    t.verify()
    
    assert t[14]
    t.remove_overlap(14)
    t.verify()
    assert not t[14]
    
    # Emptying the tree
    #t.print_structure()
    for iv in sorted(iter(t)):
        #print('### Removing '+str(iv)+'... ###')
        t.remove(iv)
        #t.print_structure()
        t.verify()
        #print('')
    assert len(t) == 0
    assert t.is_empty()
    assert not t
    
    t = IntervalTree(ivs)
    #t.print_structure()
    t.remove_overlap(1)
    #t.print_structure()
    t.verify()
    
    t.remove_overlap(8)
    #t.print_structure()    
    print('    passed')
    
    t = IntervalTree(ivs)
    pprint(t)
    t.split_overlaps()
    pprint(t)
    #import cPickle as pickle
    #p = pickle.dumps(t)
    #print(p)
    