function [ I_blurred ] = blur_image_gauss( I, std )
%BLUR_IMAGE_GAUSS Summary of this function goes here
%   Detailed explanation goes here
     if (std == 0) I_blurred = I; 
     else 
        [X,Y] = meshgrid(-std : std, -std : std);

        g = gauss(0,std,X,Y);
        g = g./sum(sum(g));
        I_blurred = conv2(I,g,'same');
     end
end

