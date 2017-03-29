import numpy, sys, os

for subset in os.listdir(sys.argv[ 1 ]) :
    print subset
    os.system( 'mkdir -p '+sys.argv[ 3 ]+'/'+subset )

    for fname in os.listdir(sys.argv[ 1 ]+'/'+subset):
        f = open(sys.argv[ 1 ]+'/'+subset+'/'+fname,'r')
        lines = f.readlines()
        f.close()
        fids = [v.split(' ')[0] for v in lines]
        f = open(sys.argv[ 2 ]+'/'+subset+'/'+fname,'r')
        lines2 = f.readlines()
        f.close()
        fids_sub = [v.split(' ')[0] for v in lines2]

        # open output file
        f = open(sys.argv[ 3 ]+'/'+subset+'/'+fname,'w')
        
        # # remove fids_sub if not included in fids
        # is_included = [(v in fids) for v in fids_sub]
        # inds = [i for i, x in enumerate(is_included) if x == True]
        # fids_sub = [v for v in fids_sub if (v in fids)]

        # # print subclasses info.
        # for i in inds:
        #     f.write( lines2[ i ] )

        # print samples included in fids_sub
        is_included = [(v in fids_sub) for v in fids]
        inds = [i for i, x in enumerate(is_included) if x == True]
        for i in inds:
            f.write( lines[ i ] )

        # print remaining samples
        inds = [i for i, x in enumerate(is_included) if x == False]
        for i in inds:
            f.write( lines[ i ] )

        f.close()
