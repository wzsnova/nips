clc
clear num
num = xlsread('composition_32');
c32(1,:) = min(num(:,:));
c32(2,:) = max(num(:,:));
c32(3,:) = mean(num(:,:));