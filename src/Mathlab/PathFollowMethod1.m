%% 
clear all; close all ; clc

dt = 0.1;
ts = 20;
t = 0:dt:ts;

eta(:,1) = [0;1;0];

%% Pure puresuilt algorimth


%% Vehicle parameters

a = 0.05;
d = 0.2;
l = 0.2;
eta_d_x = [0 1 2];
eta_d_y = [0 1 0];
eta_des = [eta_d_x;eta_d_y];




for i = 1:length(t)
    eta_d(:,i) = [2*sin(0.5*t(i));2-2*cos(0.5*t(i));0];
    eta_d_dot = [1*cos(0.5*t(i));1*sin(0.5*t(i));0];
    eta_tilda = eta_d(:,i) - eta(:,i);

    psi = eta(3,i);
    J = [cos(psi),-sin(psi),0;
        sin(psi),cos(psi),0;
        0,0,1];
    zeta(:,i) = inv(J)*(eta_d_dot+diag([1,1,8])*eta_tilda);

    W = [-a/3,-a/3,(2*a)/3;
         (sqrt(3)*a/3),-(sqrt(3)*a/3),sym(0);
         a/(3*l),a/(3*l),a/(3*l);];
    w = inv(W) *zeta(:,i);

    zeta(:,i) = W*w;
    eta(:,i+1) = eta(:,i)+(1-exp(-1*t(i)))*J*zeta(:,i)*dt;

end

veh_box = [0.4*cosd(0:360);0.4*sind(0:360)];
veh_box1 = [0.6*cosd(0:360);0.6*sind(0:360)];
wheel_b = 0.5*[-0.2 0.2 0.2 -0.2 -0.2;-0.05 -0.05 0.05 0.05 -0.05;];

for i = 1:length(t)
%     plot(eta_des(1,:),eta_des(2,:),'k--')
%     hold on 
%     grid on
%     for i1= 1:length(eta_d_x)
%         plot (eta_des(1,i1),eta_des(2,i1),'k*')
%     end
    psi = eta(3,i);
    x(i) = eta(1,i);y(i)= eta(2,i);
    R_psi = [cos(psi),-sin(psi);
             sin(psi),cos(psi);];
    v_m = R_psi*veh_box;
    v_m1 = R_psi*veh_box1;
    theta1 = pi/6;
    theta2 = 5*pi/6;
    theta3 = 3*pi/2;
    R1 = [cos(psi + theta1),-sin(psi + theta1);sin(psi + theta1),cos(psi + theta1)];
    R2 = [cos(psi + theta2),-sin(psi + theta2);sin(psi + theta2),cos(psi + theta2)];
    R3 = [cos(psi + theta3),-sin(psi + theta3);sin(psi + theta3),cos(psi + theta3)];
    w_m3 = R3*(wheel_b + [l;0]);
    w_m2 = R2*(wheel_b + [l;0]);
    w_m1 = R1*(wheel_b + [l;0]);
    fill(v_m(1,:)+x(i),v_m(2,:)+y(i),'y')
    hold on 
    fill(w_m1(1,:)+x(i),w_m1(2,:)+y(i),'k')
    fill(w_m2(1,:)+x(i),w_m2(2,:)+y(i),'k')
    fill(w_m3(1,:)+x(i),w_m3(2,:)+y(i),'k')
%     plot(v_m1(1,:)+x(i),v_m1(2,:)+y(i),'k--')

%   plot(eta_d(1),eta_d(2),'k*')
%    plot([eta_d(1),eta_d(1)+0.2*cos(eta_d(3))],[eta_d(2),eta_d(2)+0.2*cos(eta_d(3))],'k--')
    plot(eta_d(1,1:i),eta_d(2,1:i),'r-')
    plot(eta(1,1:i),eta(2,1:i),'b-')
    plot(eta(1)+0.1*cosd(0:360),eta(2)+0.1*sind(0:360),'k--')
%     plot(eta(1,1:i)+0.5*cosd(0:360),eta(2,1:i)+0.5*sind(0:360),'c--')
     
    xmin = min(eta(1,:))- 0.5;
    xmax = max(eta(1,:))+ 0.5;
    ymin = min(eta(2,:))- 0.5;
    ymax = max(eta(2,:))+ 0.5;
    axis([xmin xmax ymin ymax]);
    axis equal
    grid on
    pause(0.1);
    hold off
end


