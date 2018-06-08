function g=gauss(m,s,X,Y)
 g=1/(s*sqrt(2.0*pi))*exp(-((X-m).^2+(Y-m).^2)/(2*s^2));
end