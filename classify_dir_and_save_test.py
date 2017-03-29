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
if len(sys.argv) > 5:
    clsnum = int(sys.argv[ 5 ])

#####################
# read sample info. #
#####################

f = open('TXT/test_normal.txt')
lines = f.readlines()
f.close()
mid  = [l.split('/')[-1].split('_')[0] for l in lines]
mid = mid[::20]
mid = numpy.array(mid)

###############
# read scores #
###############

dirname = sys.argv[2]

pred_classes = numpy.zeros( len(mid), dtype=numpy.int );
scores = numpy.zeros( (len(mid), clsnum) );
# read scores
f = open( dirname+'/test_'+sys.argv[3]+'.txt' )
lines = f.readlines()
f.close()
idx = 0
for l in lines:
    s = [float(val) for val in l.split(' ')[:-1]]
    pred_classes[ idx ] = numpy.argmax( s )
    scores[ idx ] = s #numpy.max( s )
    idx += 1

#################
# write ranking #
#################

savedir = sys.argv[ 4 ] + '/test_'+sys.argv[3]+'/'
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
