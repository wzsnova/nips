clc
clear num
num = xlsread('composition_4');
c4(1,:) = min(num(:,:));
c4(2,:) = max(num(:,:));
c4(3,:) = mean(num(:,:));