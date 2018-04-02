function [ L, a, b ] = rgb_to_lab( rgb_image )
% Liz's transformation from RGB to LAB. RGB -> CIE XYZ -> CIE Lab

    R = rgb_image(:,:,1);
    G = rgb_image(:,:,2);
    B = rgb_image(:,:,3);
    
    [nrows, ncols, k] = size(rgb_image);
    
    %transform to XYZ
    for i = 1 : nrows
      for j = 1 : ncols
        X(i,j) = 0.412 * double(R(i,j)) + 0.358 * double(G(i,j)) + 0.180 * double(B(i,j));
        Y(i,j) = 0.213 * double(R(i,j)) + 0.715 * double(G(i,j)) + 0.072 * double(B(i,j));
        Z(i,j) = 0.019 * double(R(i,j)) + 0.119 * double(G(i,j)) + 0.950 * double(B(i,j));
      end
    end
    
    %transform to Lab
    for i = 1 : nrows
      for j = 1 : ncols
        L(i,j) = 116 * (Y(i,j)^(1/3)) - 16;
        a(i,j) = 500 * (X(i,j)^(1/3) - Y(i,j)^(1/3));
        b(i,j) = 200 * (Y(i,j)^(1/3) - Z(i,j)^(1/3));
      end
    end
    
end

