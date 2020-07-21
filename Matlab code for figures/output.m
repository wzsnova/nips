%%%%%%%%%%%%%%%%%%%%%%%%%%% drawing Output range 1, 2, 3, 4
clc
clear num i

% for i=1
%     x = 1:5
%     if max_output1(i,:) & min_output1(i,:) ~= NaN
%         plot(x,(max_output1(i,:)-min_output1(i,:)));
%         hold on
%         plot(x,(max_output2(i,:)-min_output2(i,:)));
%         hold on
%         plot(x,(max_output3(i,:)-min_output3(i,:)));
%         hold on
%         plot(x,(max_output4(i,:)-min_output4(i,:)));
%     
% end
%a =['b','s','a']
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% output1
x = [2, 4, 8, 16, 32];
p11=plot(x,(max_output1(1,:)-min_output1(1,:)));  
hold on 
p12=plot(x,(max_output1(2,:)-min_output1(2,:)));  
hold on 
p13=plot(x,(max_output1(3,:)-min_output1(3,:)));  
legend([p11 p12 p13],'minRangOutput','maxRangOutput','avgRangOutput')
xlabel('Number of abstract nodes')
ylabel('Output range 1')
figure
%%%%%%%%%%%%%%%%%%%%%%%%%%%% output2
p21=plot(x,(max_output2(1,:)-min_output2(1,:)));  
hold on 
p22=plot(x,(max_output2(2,:)-min_output2(2,:)));  
hold on 
p23=plot(x,(max_output2(3,:)-min_output2(3,:)));
legend([p21 p22 p23],'minRangOutput','maxRangOutput','avgRangOutput')
xlabel('Number of abstract nodes')
ylabel('Output range 2')
figure
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% output3
p31=plot(x,(max_output3(1,:)-min_output3(1,:)));  
hold on 
p32=plot(x,(max_output3(2,:)-min_output3(2,:)));  
hold on 
p33=plot(x,(max_output3(3,:)-min_output3(3,:)));  
legend([p31 p32 p33],'minRangOutput','maxRangOutput','avgRangOutput')
xlabel('Number of abstract nodes')
ylabel('Output range 3')
figure
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% output4
p41=plot(x,(max_output4(1,:)-min_output4(1,:)));  
hold on 
p42=plot(x,(max_output4(2,:)-min_output4(2,:)));  
hold on 
p43=plot(x,(max_output4(3,:)-min_output4(3,:)));  
legend([p41 p42 p43],'minRangOutput','maxRangOutput','avgRangOutput')
xlabel('Number of abstract nodes')
ylabel('Output range 4')






