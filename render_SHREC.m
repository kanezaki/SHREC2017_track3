function render_SHREC( subset, reverse_flg )
% subset = 'train_normal'

addpath(genpath('mvcnn_utils'));

fig = figure('Visible','off');

if nargin < 2
  reverse_flg = false
end

dirpath = ['data/' subset]
imdirpath = ['images/' subset]
mkdir(imdirpath)
files = dir(dirpath)

inds = 3:length(files);
if reverse_flg
  inds = length(files):-1:3;
end

for i=inds
  modelname = files(i).name
  modelname_ = strsplit(modelname,'.');
  imname = modelname_{1};
  if exist([imdirpath '/' imname '_' num2str(20,'%03d') '.png']) > 0
    continue
  end

  try
    tic
      mesh = loadMesh([dirpath '/' modelname]);
      ims = render_views(mesh, 'use_dodecahedron_views', true, 'figHandle', fig);
      
      if length(ims) ~= 20
        fprintf('Please check mvcnn_utils/render_views.m!\n');
        return
      end
    toc
    tic
      for k=1:20
        imwrite(ims{k}, [imdirpath '/' imname '_' num2str(k,'%03d') '.png']);
      end
    toc
  end
end
