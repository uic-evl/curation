function [ features ] = get_descriptor( rgb_image )
%GET_DESCRIPTOR Get the features vector consisting of the scaled sigma per
%pixel applied to L, a, b, and the texture properties 

    [L, a, b] = rgb_to_lab(rgb_image);    
    % [gX, gY] = calc_gradient(L); Liz's gradient do not consider borders
    [Gx, Gy] = gradient(L); % NablaI(:,:,1), NablaI(:,:,2)
    Gxx = bsxfun(@times, Gx, Gx);
    Gyy = bsxfun(@times, Gy, Gy);
    Gxy = bsxfun(@times, Gx, Gy);
    
    % Calculate scale per pixel
    [P, lambda1, lambda2] = calc_polarities(Gx, Gy, Gxx, Gxy, Gyy);
    [sigmaStar, pSigmaStar] = calc_scale_polarity(P, lambda1, lambda2);
    [features, new_rows, new_cols] = calc_feature_vector(L, a, b, P, lambda1, lambda2, sigmaStar, pSigmaStar);
end

