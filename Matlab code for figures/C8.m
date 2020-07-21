clc
clear num
num = xlsread('composition_8');
c8(1,:) = min(num(:,:));
c8(2,:) = max(num(:,:));
c8(3,:) = mean(num(:,:));