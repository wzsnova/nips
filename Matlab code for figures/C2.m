clc
clear num
num = xlsread('composition_2');
c2(1,:) = min(num(:,:));
c2(2,:) = max(num(:,:));
c2(3,:) = mean(num(:,:));