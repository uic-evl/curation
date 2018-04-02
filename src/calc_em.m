function [ output_args ] = calc_em( features )
%CALC_EM Summary of this function goes here
%   Detailed explanation goes here
    
    [ nVectors, dimVector] = size(features);
    nGaussians = 2;
    
    ml_global_max = -Inf;
    assgn_global_max = zeros(1, nVectors);
    
    % save something in case of singularity
    sing_assignment = zeros(1, nVectors);
    sing_ml = -Inf;
    
    % call EM 10 times, adding noise to the means to avoid shallow maxima
    for it = 1 : 10
        % generate random means
        clear Mi;
        for i = 1 : nGaussians
            Mi(i,:) = 3 * randn(1, dimVector);
        end
        
        [ret, ml, retMi, retSigma, retAlpha, er] = EMmy( nGaussians, dimVector, nVectors, features, Mi);
        
        % check singularity
        if (ml > sing_ml)
            sing_ml = ml;
            sing_assignment = ret;
        end
        
        if ml > ml_global_max && ml ~= Inf && er ~= 1
            ml_global_max = ml;
            assgn_global_max = ret;
        end        
    end
    
    

end

