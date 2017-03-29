import numpy, sys, os

####################
# read class info. #
####################

#f = open('classes.txt')
f = open(sys.argv[1])
classes = f.readlines()
f.close()
classes = [f[:-1] for f in classes]
clsnum = len(classes)
if len(sys.argv) > 6:
    clsnum = int(sys.argv[ 6 ])

#####################
# read sample info. #
#####################

f = open(sys.argv[3]+'.csv')
lines = f.readlines()
lines = lines[1:] # ignore header
f.close()
mid  = [l.split(',')[0] for l in lines]
cid  = [l.split(',')[1] for l in lines]
scid = [l.split(',')[2][:-1] for l in lines]
mid = numpy.array(mid)

###############
# read scores #
###############

dirname = sys.argv[2]

pred_classes_ = []
scores_ = []
for clsid in range(len(classes)):
    # read scores
    f = open( dirname+'/'+sys.argv[3]+'_'+sys.argv[4]+'_'+str( clsid )+'.txt' )
    lines = f.readlines()
    f.close()
    pc = numpy.zeros( len(lines), dtype=numpy.int );
    ss = numpy.zeros( (len(lines), clsnum) );
    idx = 0
    for l in lines:
        s = [float(val) for val in l.split(' ')[:-1]]
        pc[ idx ] = numpy.argmax( s )
        ss[ idx ] = s #numpy.max( s )
        idx += 1
    pred_classes_.append( pc )
    scores_.append( ss )

##################
# reorder scores #
##################

pred_classes = numpy.zeros( len(mid), dtype=numpy.int );
scores = numpy.zeros( (len(mid), clsnum) );
for clsid in range(len(classes)):
    inds = [i for i, x in enumerate(cid) if x == classes[ clsid ] ]
    pred_classes[ inds ] = pred_classes_[ clsid ]
    scores[ inds ] = scores_[ clsid ]

#################
# write ranking #
#################

savedir = sys.argv[ 5 ] + '/'+sys.argv[3]+'_'+sys.argv[4]+'/'
os.system( 'mkdir -p '+savedir )

for m in range(len(mid)):
    f = open( savedir+mid[ m ], 'w' )
    scores_each = scores[ :, pred_classes[ m ] ].copy()
    scores_each[ m ] = float('inf')
    if 0:
        inds = numpy.argsort( scores_each )[ ::-1 ]
        inds = inds[:1000]
        for i in inds:
            f.write( mid[ i ]+' '+str(1./scores_each[ i ])+'\n' )
    else:
        # pick up samples in the same class
        inds = [i for i, x in enumerate(pred_classes) if x == pred_classes[ m ] ]
        scores_each_ = scores_each[ inds ]
        mid_ = mid[ inds ]
        inds = numpy.argsort( scores_each_ )[ ::-1 ]
        if len(inds) > 1000:
            inds = inds[:1000]
        for i in inds:
            f.write( mid_[ i ]+' '+str(1./scores_each_[ i ])+'\n' )
    f.close()
