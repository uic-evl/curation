function [Ep , En] = local_dot(M, x, y, s, v)
%M covariance matrix; x y coords of pixel; s variance; v unit length vector

if(s==0) Ep =0;En = 0;
else
     [nl,nc,k]=size(M);
     if x >= s  lstart = x-s; 
        else lstart = 0;
     end;

     if x+s >= nl  lend = nl; 
        else lend = x+s;
     end;

     if y >= s  cstart = y-s; 
        else cstart = 0;
     end;

     if y+s >= nc  cend = nc; 
        else cend = y+s;
     end;
     
     
     for ii = 1 : (lend -lstart)
        for jj = 1 : (cend - cstart)
          T(ii,jj,1) = M(lstart+ii,cstart+jj,1);
          T(ii,jj,2) = M(lstart+ii,cstart+jj,2);
        end;
     end;
     D  = dot_product(T,v);
     [nnl, nnc ] = size(D);
     Ep = 0;
     En = 0;
     for i = 1 : nnl
       for j = 1 : nnc
         if D(i,j)>0 Ep = Ep + 1; % this is incorrect
            elseif D(i,j)<0 En = En + 1; % this is incorrect
         end; 
     end; 
     end;
end;

