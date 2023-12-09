function a = equalCompare(num1,num2)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    if(abs(num1 -num2)<0.0000001)
        a = 1;
    else
        a = 0;
    end
end