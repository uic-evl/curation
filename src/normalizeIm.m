function M = normalizeIm(Imm)
    
    [nnl,nnc] = size(Imm);
    min = Imm(1,1);
    max = Imm(1,1);
    
    for i = 1:nnl
      for j = 1: nnc
        if (Imm(i,j) < min) min = Imm(i,j);
        end;
        if (Imm(i,j) > max) max = Imm(i,j);
        end
      end
    end;
    
    for i = 1:nnl
      for j = 1: nnc
        M(i,j) =  (Imm(i,j) - min)/(max - min);
      end;
    end
end
