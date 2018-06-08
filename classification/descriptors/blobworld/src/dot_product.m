function D = dot_product(M,v)
     [nl,nc,k]=size(M);
     for ii = 1 : nl
        for jj = 1 : nc
          D(ii,jj) = M(ii,jj,1) * v(1) + M(ii,jj,2) * v(2);
        end
     end
end
