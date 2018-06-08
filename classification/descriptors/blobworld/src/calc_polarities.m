function [ P, lambda1, lambda2 ] = calc_polarities( Gx, Gy, Gxx, Gxy, Gyy )
%CALC_POLARITY Summary of this function goes here
%   Detailed explanation goes here

    [nrows, ncols] = size(Gxx);
    
    NablaI(:,:,1) = Gx;
    NablaI(:,:,2) = Gy;

    for k = 0 : 7
        Mxx = blur_image_gauss(Gxx,k/2);
        Mxy = blur_image_gauss(Gxy,k/2);
        Myy = blur_image_gauss(Gyy,k/2);
        
        for i = 1 : nrows
            for j = 1 : ncols
               M(1,1) = Mxx(i,j);
               M(1,2) = Mxy(i,j);
               M(2,1) = Mxy(i,j);
               M(2,2) = Myy(i,j);
               
               [V,D] = eig(M);
               if (D(1,1)>D(2,2))
                  lambda1(i,j,k+1) = D(1,1);
                  lambda2(i,j,k+1) = D(2,2);
                  eigVec1 = V(:,1);
                  eigVec2 = V(:,2);
               else
                  lambda2(i,j,k+1) = D(1,1);
                  lambda1(i,j,k+1) = D(2,2);
                  eigVec2 = V(:,1);
                  eigVec1 = V(:,2);
               end;
               
               if (eigVec1(1) == 0)
                 if (eigVec1(2) > 0) phi = 3.14 / 2;
                 else phi = -3.14 / 2;
                 end;
               else       
                    phi = atan(eigVec1(2)/eigVec1(1));
               end;

               n(2) = sin(phi);
               n(1) = cos(phi);
               [Ep , En] = local_dot(NablaI, i, j, k, n);
               P(i,j,k+1) = abs(Ep-En)/(Ep + En + 0.1);
            end
        end    
    end
end

