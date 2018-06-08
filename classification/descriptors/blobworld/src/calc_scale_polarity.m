function [ sigmaStar, pSigmaStar ] = calc_scale_polarity( P, lambda1, lambda2 )
%CALC_SCALE_POLARITY Returns matrix with the scaling per pixel

    %find p sigma star, for each k, all over the image
    % Get the smoothed polarity pSigmaStar (p1029) with 2*sigma
    for k = 0 : 7
      pSigma = P(:,:,k+1);
      pSigmaStar(:,:,k+1) = blur_image_gauss(pSigma,k);
    end;    
    
    clear sigmaStar;
    %find sigma star for each pixel
    [nrows, ncols, nz] = size(P);
    for i = 1 : nrows
        for j = 1 : ncols
            
          found = 0;
          for k = 2 : 8
             if (abs(pSigmaStar(i,j,k) - pSigmaStar(i,j,k-1)) < 0.02 ) && found == 0
               val = k;
               found = 1;
             end
          end

          if found == 0
            sigmaStar(i,j) = (k-1)/2;
          else 
            sigmaStar(i,j) = (val-1)/2;
          end
        end
    end   

    % Now look for uniform regions where contrast across scale is less than
    % 0.1, and set the scale to 0
    for i = 1 : nrows
        for j = 1 : ncols
            ka = sigmaStar(i,j)*2;
            con = 2 * sqrt(lambda1(i,j,ka)+lambda2(i,j,ka));
            if con < 0.1; sigmaStar(i,j) = 0; end
        end
    end
end

