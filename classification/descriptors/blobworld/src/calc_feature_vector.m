function [ features, nrows_c, ncols_c ] = calc_feature_vector( L, a, b, P, lambda1, lambda2, sigmaStar, pSigmaStar )
%CALC_FEATURE_VECTOR Summary of this function goes here
%   Detailed explanation goes here
    
    [nrows, ncols, nz] = size(P);
    
    for i = 1 : nrows
     for j = 1 : ncols
      ka = sigmaStar(i,j)*2;
      if(ka == 0) 
        pol(i,j) = 0;
        ani(i,j) = 0;
        con(i,j) = 0;
      else
        pol(i,j) = pSigmaStar(i,j,ka);
        con(i,j) = 2 * sqrt(lambda1(i,j,ka)+lambda2(i,j,ka));
        if lambda1(i,j,ka) == 0 
            ani(i,j) = -1000; % can replace denominator with lambda1 + eps
        else
            ani(i,j) = 1 - lambda2(i,j,ka)/lambda1(i,j,ka);
        end
      end
     end
    end    
    
    clear ac pc c
    %compute texture descriptors
    ac = ani .* con;
    pc = (pol*10) .* con; % idk why is multiplied by 10
    c = con;
    
    for k = 1 : 8
      Lblurred(:,:,k) = blur_image_gauss(L,(k-1)/2);
      ablurred(:,:,k) = blur_image_gauss(a,(k-1)/2);
      bblurred(:,:,k) = blur_image_gauss(b,(k-1)/2);
    end

    for i = 1 : nrows
     for j = 1 : ncols
      Lone(i,j) = Lblurred(i,j,sigmaStar(i,j)*2 + 1);
      aone(i,j) = ablurred(i,j,sigmaStar(i,j)*2 + 1);
      bone(i,j) = bblurred(i,j,sigmaStar(i,j)*2 + 1);
     end;
    end;

    Lbis = normalizeIm(Lone(5:nrows - 4, 5:ncols - 4));
    abis = normalizeIm(aone(5:nrows - 4, 5:ncols - 4));  
    bbis = normalizeIm(bone(5:nrows - 4, 5:ncols - 4));

    pcb = normalizeIm(pc(5:nrows - 4, 5:ncols - 4));
    acb = normalizeIm(ac(5:nrows - 4, 5:ncols - 4));
    cb  = normalizeIm(c (5:nrows - 4, 5:ncols - 4)); 

    %place everything into feature matrix
    
    [nrows_c, ncols_c, nz_c] = size(Lbis);
    for i = 1:nrows_c
     for j = 1 : ncols_c
        featM(i,j,1) = Lbis(i,j);
        featM(i,j,2) = abis(i,j);
        featM(i,j,3) = bbis(i,j);
        featM(i,j,4) = i/nrows; % added but not used in blobworld
        featM(i,j,5) = j/ncols;
        featM(i,j,6) = pcb(i,j);
        featM(i,j,7) = acb(i,j);
        featM(i,j,8) = cb(i,j);
     end
    end   
    
    [ll, cc, kk] = size(featM);
    for i = 1 : ll
     for j = 1 : cc
        features((i-1)*cc + j,:) = featM(i,j,:);
     end
    end
end

