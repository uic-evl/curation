function [assgnment,ml,retMi,retSigma,retAlpha, er] = em(K,d,N,feat,Mi)
%does EM: K number of Gaussians, d length of a feature vector, N
%number of vectors, feat the feature vectors, Mi - K median vectors to
%start with

%init alpha and sigma
for i = 1 : K
    alpha(i) = 1/K;
    sigma(:,:,i) = eye(d);
end;

likelihood = -Inf;

for iter = 1 : 100
    
    
    
    
    %//**************************************************************E step*****
    
    
    
    %//clear f invSigma dt dto;
    %//calc f(i,j)  (formula 2, section3)
    for i = 1 : K
        
        if(min(abs(diag(sigma(:,:,i),0))) < 0.0001)
            display('singular detected');
            
            for ii=1:N
                [Y,I] = max(pbt(:,ii));
                assgnment(ii) = I(1);
            end;
            
            ml = likelihood;
            
            
            retMi = Mi;
            retSigma = sigma;
            
            er = 1;
            for fifi=1:N
                [Y,I] = max(pbt(:,fifi));
                assgnment(fifi) = I(1);
                %//pbt(1,i) - pbt(2,i);
            end;
            
            %added 2018
            retAlpha = alpha;
            
            return;
        end;
        if(rcond(sigma(:,:,i)) < 9.989153e-31)
            display('rcond singular detected');
            
            for ii=1:N
                [Y,I] = max(pbt(:,ii));
                assgnment(ii) = I(1);
            end;
            
            ml = likelihood;
            
            
            retMi = Mi;
            retSigma = sigma;
            for fifi=1:N
                [Y,I] = max(pbt(:,fifi));
                assgnment(fifi) = I(1);
                %//pbt(1,i) - pbt(2,i);
            end;
            
            er = 1;
            retAlpha = alpha;
            return;
        end;
        %// disp('ante invSigma');
        invSigma = inv(sigma(:,:,i));
        %// disp('ante det Sigma');
        %// disp('ante f');
        dt = sqrt(abs(det(sigma(:,:,i))));
        
        for j = 1 : N
            f(i,j) = 1/ ((2.0*pi)^(d/2) * dt) * exp(-0.5*((feat(j,:) - Mi(i,:)) * invSigma * (feat(j,:) - Mi(i,:))'));
            %'//
        end;
    end;
    
    
    %//calc pbt(i,j) (formula 6, section3)
    clear pbt;
    for j = 1 : N
        sum = 0;
        for k = 1: K
            sum = sum + alpha(k) * f(k,j);
        end;
        if(sum == 0) display('the f-s are too small');
            
            for i=1:N
                [Y,I] = max(pbt(:,i));
                assgnment(i) = I(1);
            end;
            
            ml = likelihood;
            
            er = 1;
            retMi = Mi;
            retSigma = sigma;
            
            
            return;
        end;
        for i = 1 : K
            pbt(i,j) = alpha(i) * f(i,j) / sum;
        end;
    end;
    
    
    %//calc likelihood before updating;
    clear prod;
    prod = 0;
    for k = 1 : N
        sum = 0;
        for i = 1 : K
            sum = sum + alpha(i) * f(i,k);
        end;
        prod = prod + log(sum);
    end;
    
    %  if(((prod - likelihood) < 0)&) %bad condition: it cries when  -78.7627< -78.7627
    %    prod
    %    display('is less than');
    %    likelihood
    %    error('likelihood non increasing!!!!!!!!');
    %  return;
    %  end;
    
    if(abs(prod-likelihood) < 0.01)
        display('breaking');
        break;
    end;
    
    likelihood = prod;
    if(likelihood == Inf)
        display('Likelihood is Inf');
        likelihood = -10000;
        ml = likelihood;
        
        er = 1;
        return;
    end;
    %iter
    
    %likelihood
    
    %//***********************************************************M step*****
    %//update
    clear su sum
    for i = 1 : K
        su = 0;
        sum = zeros(1,d);
        for j = 1 : N
            su = su + pbt(i,j);
            sum = sum + feat(j,:).* pbt(i,j);
        end;
        alpha(i) = 1/N * su;
        Mi(i,:) = sum./su;
        %clear sum;
        sum2 = zeros(d);
        for j = 1 : N
            sum2 = sum2 + pbt(i,j)*(feat(j,:) - Mi(i,:))'*(feat(j,:) - Mi(i,:));
            %' //'
        end;
        sigma(:,:,i) = sum2 ./ su;
    end;
    
    
    
    
end;

for i=1:N
    [Y,I] = max(pbt(:,i));
    assgnment(i) = I(1);
    %//pbt(1,i) - pbt(2,i);
end;

ml = likelihood;
er = 0;

retMi = Mi;
retSigma = sigma;
retAlpha = alpha;


