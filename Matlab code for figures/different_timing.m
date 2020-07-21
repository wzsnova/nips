%%%%%%%%%%%%%%%%%%%%%%%%%%% drawing Abstract Time, Encoding Time, Gurobi Time
clc
clear num


%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Abstract_time
x = [2, 4, 8, 16, 32];
p01=plot(x,(Abstract_time(1,:)));  
hold on 
p02=plot(x,(Abstract_time(2,:)));  
hold on 
p03=plot(x,(Abstract_time(3,:)));  
legend([p01 p02 p03],'minAbstracTime','maxAbstracTime','avgAbstracTime')
xlabel('Number of abstract nodes')
ylabel('Abstract Time')
figure
%%%%%%%%%%%%%%%%%%%%%%%%%%%% Encoding_time
p011=plot(x,(Encoding_time(1,:)));  
hold on 
p022=plot(x,(Encoding_time(2,:)));  
hold on 
p033=plot(x,(Encoding_time(3,:)));  
legend([p011 p022 p033],'minEncodingTime','maxEncodingTime','avgEncodingTime')
xlabel('Number of abstract nodes')
ylabel('Encoding Time')
figure
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Gurobi_time
p001=plot(x,(Gurobi_time(1,:)));  
hold on 
p002=plot(x,(Gurobi_time(2,:)));  
hold on 
p003=plot(x,(Gurobi_time(3,:)));  
legend([p001 p002 p003],'minGurobiTime','maxGurobiTime','avgGurobiTime')
xlabel('Number of abstract nodes')
ylabel('Gurobi Time')


















