# Scripts for SHREC2017 Track3 using RotationNet

## Getting Started 

### 1. Prepare [caffe-rotationnet2](https://github.com/kanezaki/caffe-rotationnet2)
    $ git clone https://github.com/kanezaki/caffe-rotationnet2.git  
    $ cd caffe-rotationnet2  
  
Prepare your Makefile.config and compile.  

    $ make; make pycaffe  

### 2. Download initial weights for fine-tuning the models
   Please download the file "ilsvrc\_2012\_train\_iter\_310k" according to [R-CNN repository](https://github.com/rbgirshick/rcnn)  
   This is done by the following command:  

    $ wget http://www.cs.berkeley.edu/~rbg/r-cnn-release1-data.tgz  
    $ tar zxvf r-cnn-release1-data.tgz  

### 3. Render multi-view images
  First, download the 3D model data from [SHREC2017 Track3 competition website](https://shapenet.cs.stanford.edu/shrec17/).  
  Unzip test\_normal.zip, test\_perturbed.zip, train\_normal.zip, train\_perturbed.zip, val\_normal.zip, and val\_perturbed.zip in data/ directory.  
  Then, do the following processes in matlab.  

    $ matlab  
    >> render_SHREC('test_normal');  
    >> render_SHREC('test_perturbed');  
    >> render_SHREC('train_normal');  
    >> render_SHREC('train_perturbed');  
    >> render_SHREC('val_normal');  
    >> render_SHREC('val_perturbed');  

### 4. Train RotationNet models
    $ tar zxvf TXT.tar.gz  
    $ ./caffe-rotationnet2/build/tools/caffe train -solver prototxt/rotationnet_alex_SHREC2017_case2_solver_b900.prototxt -weights ilsvrc_2012_train_iter_310k 2>&1 | tee log_SHREC2017_alex.txt  
    $ ./caffe-rotationnet2/build/tools/caffe train -solver prototxt/rotationnet_alex_SHREC2017_case2_solver_b900_perturbed.prototxt -weights ilsvrc_2012_train_iter_310k 2>&1 | tee log_SHREC2017_alex_perturbed.txt  
    $ ./caffe-rotationnet2/build/tools/caffe train -solver prototxt/rotationnet_alex_SHREC2017_SUB_case2_solver_b900_ratio.prototxt -weights ilsvrc_2012_train_iter_310k 2>&1 | tee log_SHREC2017_SUB_alex_ratio.txt  
    $ ./caffe-rotationnet2/build/tools/caffe train -solver prototxt/rotationnet_alex_SHREC2017_SUB_case2_solver_b900_ratio_perturbed.prototxt -weights ilsvrc_2012_train_iter_310k 2>&1 | tee log_SHREC2017_SUB_alex_ratio_perturbed.txt  

  You probably have to set base\_lr = 0.0005 for the first few iterations (~1000) and then increase it to base\_lr = 0.001.  
  Or, you can also download pretrained models here.  

    $ cd models/  
    $ wget https://www.dropbox.com/s/civfcz97xh5oy7l/rotationnet_alex_SHREC2017_case2_b900_iter_68000.caffemodel  
    $ wget https://www.dropbox.com/s/yqev08sn1yl4xib/rotationnet_alex_SHREC2017_case2_b900_perturbed_iter_75000.caffemodel  
    $ wget https://www.dropbox.com/s/7c77rczf231uf7q/rotationnet_alex_SHREC2017_SUB_case2_b900_ratio_iter_78000.caffemodel  
    $ wget https://www.dropbox.com/s/lgtvfgj9l7ck5mu/rotationnet_alex_SHREC2017_SUB_case2_b900_ratio_perturbed_iter_78000.caffemodel  

### 5. Save scores
    $ bash save_scores_alex.sh train normal  
    $ bash save_scores_alex.sh train perturbed  
    $ bash save_scores_alex.sh val normal  
    $ bash save_scores_alex.sh val perturbed  
    $ bash save_scores_alex.sh test normal  
    $ bash save_scores_alex.sh test perturbed  
    $ bash save_scores_alex_ratio_subclass.sh train normal  
    $ bash save_scores_alex_ratio_subclass.sh train perturbed  
    $ bash save_scores_alex_ratio_subclass.sh val normal  
    $ bash save_scores_alex_ratio_subclass.sh val perturbed  
    $ bash save_scores_alex_ratio_subclass.sh test normal  
    $ bash save_scores_alex_ratio_subclass.sh test perturbed  

### 6. Do retrievals
   Download train.csv and val.csv.  

    $ wget http://vision.princeton.edu/ms/shrec17-data/train.csv  
    $ wget http://vision.princeton.edu/ms/shrec17-data/val.csv  

####  Main results
    $ python classify_dir_and_save.py classes.txt results_alex train normal Alex  
    $ python classify_dir_and_save.py classes.txt results_alex train perturbed Alex  
    $ python classify_dir_and_save.py classes.txt results_alex val normal Alex  
    $ python classify_dir_and_save.py classes.txt results_alex val perturbed Alex  
    $ python classify_dir_and_save_test.py classes.txt results_alex normal Alex  
    $ python classify_dir_and_save_test.py classes.txt results_alex perturbed Alex  

####  Subclass results
    $ python classify_dir_and_save.py classes.txt results_alex_ratio_subclass train normal AlexRatio_sub 203  
    $ python classify_dir_and_save.py classes.txt results_alex_ratio_subclass train perturbed AlexRatio_sub 203  
    $ python classify_dir_and_save.py classes.txt results_alex_ratio_subclass val normal AlexRatio_sub 203  
    $ python classify_dir_and_save.py classes.txt results_alex_ratio_subclass val perturbed AlexRatio_sub 203  
    $ python classify_dir_and_save_test.py classes.txt results_alex_ratio_subclass normal AlexRatio_sub 203  
    $ python classify_dir_and_save_test.py classes.txt results_alex_ratio_subclass perturbed AlexRatio_sub 203  

####  Results with subclass reranking
    $ python rerank_dir_and_save.py Alex AlexRatio_sub AlexSR  

####  We submitted *AlexSR* for SHREC2017 competition. However, *Alex* is actually better.
