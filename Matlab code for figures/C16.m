clc
clear num
num = xlsread('composition_16');
c16(1,:) = min(num(:,:));
c16(2,:) = max(num(:,:));
c16(3,:) = mean(num(:,:));