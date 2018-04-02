function [ gX, gY ] = calc_gradient( img )
%CALC_GRADIENT Calculate the gradient (NablaI) for the image
% The implementation is different from Matlab's  in handling the borders of
% the first and last column of the image. The sum(sum(abs(difference))) was
% in the order of e+05

    [nrows,ncols] = size(img);
    gX = size(image);
    gY = size(image);
    
    for i = 1 : nrows
     for j = 1 : ncols
       gX(i,j) = img(i,j);
       gY(i,j) = img(i,j);
     end;
    end;

    for i = 2 : (nrows-1)
      for j = 1 : ncols
        gY(i,j) = (img(i+1,j) - img(i-1,j))/2;
      end
    end

    for i = 1 : nrows
     for j = 2 : (ncols-1)
        gX(i,j) = (img(i,j+1) - img(i,j-1))/2;
     end
    end

end

