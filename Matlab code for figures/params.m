%%%%%%%%%%%%%%%%%%%%%%%%%%% finding the desired function for drawing
clc
clear num
for i=1:3
Abstract_time(i,:)=[c2(i,1),c4(i,1),c8(i,1),c16(i,1),c32(i,1)];
Encoding_time(i,:)=[c2(i,2),c4(i,2),c8(i,2),c16(i,2),c32(i,2)];
Gurobi_time(i,:)=[c2(i,3),c4(i,3),c8(i,3),c16(i,3),c32(i,3)];
min_output1(i,:)=[c2(i,4),c4(i,4),c8(i,4),c16(i,4),c32(i,4)];
max_output1(i,:)=[c2(i,5),c4(i,5),c8(i,5),c16(i,5),c32(i,5)];
min_output2(i,:)=[c2(i,6),c4(i,6),c8(i,6),c16(i,6),c32(i,6)];
max_output2(i,:)=[c2(i,7),c4(i,7),c8(i,7),c16(i,7),c32(i,7)];
min_output3(i,:)=[c2(i,8),c4(i,8),c8(i,8),c16(i,8),c32(i,8)];
max_output3(i,:)=[c2(i,9),c4(i,9),c8(i,9),c16(i,9),c32(i,9)];
min_output4(i,:)=[c2(i,10),c4(i,10),c8(i,10),c16(i,10),c32(i,10)];
max_output4(i,:)=[c2(i,11),c4(i,11),c8(i,11),c16(i,11),c32(i,11)];
end