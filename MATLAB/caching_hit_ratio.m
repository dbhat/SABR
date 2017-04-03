
%% Display Groups of Bars
% Display four groups of three bars.

% Copyright 2015 The MathWorks, Inc.

clear all
close all
figname1 = ['qual_hitratio_BOLA_glob_qual.fig']


colorVec ={[92/255 51/255 23/255],	[255/255 127/255 36/255], [255/255 20/255 147/255],[139/255 137/255 137/255]};
%colorVec=hsv(10)
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

% % % Playback bitrate
bitrate_all1 = csvread('bitrate_BOLA_glob_baseline.csv', 0);
bitrate_q1a = bitrate_all1(:,1);
bitrate_q2a = bitrate_all1(:,2);
bitrate_q3a = bitrate_all1(:,3);
bitrate_q4a = bitrate_all1(:,4);
bitrate_q5a = bitrate_all1(:,5);
%y=[bitrate_q1,bitrate_q2,bitrate_q3,bitrate_q4,bitrate_q5]

 
[muhat1a,sigmahat1a,muci1a,sigmaci1a]=normfit(bitrate_q1a)
[muhat2a,sigmahat2a,muci2a,sigmaci2a]=normfit(bitrate_q2a)
[muhat3a,sigmahat3a,muci3a,sigmaci3a]=normfit(bitrate_q3a)
[muhat4a,sigmahat4a,muci4a,sigmaci4a]=normfit(bitrate_q4a)
[muhat5a,sigmahat5a,muci5a,sigmaci5a]=normfit(bitrate_q5a)

y1=[muhat1a,muhat2a,muhat3a,muhat4a,muhat5a]
err_y1=[(muci1a(1)-muhat1a),(muci2a(1)-muhat2a),(muci3a(1)-muhat3a),(muci4a(1)-muhat4a),(muci5a(1)-muhat5a)]
bitrate_all2 = csvread('qual_hitratio_BOLA_local.csv', 0);
bitrate_q1b = bitrate_all2(:,1);
bitrate_q2b = bitrate_all2(:,2);
bitrate_q3b = bitrate_all2(:,3);
bitrate_q4b = bitrate_all2(:,4);
bitrate_q5b = bitrate_all2(:,5);
%y=[bitrate_q1,bitrate_q2,bitrate_q3,bitrate_q4,bitrate_q5]

[muhat1b,sigmahat1b,muci1b,sigmaci1b]=normfit(bitrate_q1b)
[muhat2b,sigmahat2b,muci2b,sigmaci2b]=normfit(bitrate_q2b)
[muhat3b,sigmahat3b,muci3b,sigmaci3b]=normfit(bitrate_q3b)
[muhat4b,sigmahat4b,muci4b,sigmaci4b]=normfit(bitrate_q4b)
[muhat5b,sigmahat5b,muci5b,sigmaci5b]=normfit(bitrate_q5b)

y2=[muhat1b,muhat2b,muhat3b,muhat4b,muhat5b]
err_y2=[(muci1b(1)-muhat1b),(muci2b(1)-muhat2b),(muci3b(1)-muhat3b),(muci4b(1)-muhat4b),(muci5b(1)-muhat5b)]
bitrate_all3 = csvread('qual_hitratio_BOLA_glob_fr.csv', 0);
bitrate_q1c = bitrate_all3(:,1);
bitrate_q2c = bitrate_all3(:,2);
bitrate_q3c = bitrate_all3(:,3);
bitrate_q4c = bitrate_all3(:,4);
bitrate_q5c = bitrate_all3(:,5);
%y=[bitrate_q1,bitrate_q2,bitrate_q3,bitrate_q4,bitrate_q5]

[muhat1c,sigmahat1c,muci1c,sigmaci1c]=normfit(bitrate_q1c)
[muhat2c,sigmahat2c,muci2c,sigmaci2c]=normfit(bitrate_q2c)
[muhat3c,sigmahat3c,muci3c,sigmaci3c]=normfit(bitrate_q3c)
[muhat4c,sigmahat4c,muci4c,sigmaci4c]=normfit(bitrate_q4c)
[muhat5c,sigmahat5c,muci5c,sigmaci5c]=normfit(bitrate_q5c)

y3=[muhat1c,muhat2c,muhat3c,muhat4c,muhat5c]
err_y3=[(muci1c(1)-muhat1c),(muci2c(1)-muhat2c),(muci3c(1)-muhat3c),(muci4c(1)-muhat4c),(muci5c(1)-muhat5c)]
bitrate_all4 = csvread('qual_hitratio_BOLA_glob_nr.csv', 0);
bitrate_q1d = bitrate_all4(:,1);
bitrate_q2d = bitrate_all4(:,2);
bitrate_q3d = bitrate_all4(:,3);
bitrate_q4d = bitrate_all4(:,4);
bitrate_q5d = bitrate_all4(:,5);
%y=[bitrate_q1,bitrate_q2,bitrate_q3,bitrate_q4,bitrate_q5]
 
[muhat1d,sigmahat1d,muci1d,sigmaci1d]=normfit(bitrate_q1d)
[muhat2d,sigmahat2d,muci2d,sigmaci2d]=normfit(bitrate_q2d)
[muhat3d,sigmahat3d,muci3d,sigmaci3d]=normfit(bitrate_q3d)
[muhat4d,sigmahat4d,muci4d,sigmaci4d]=normfit(bitrate_q4d)
[muhat5d,sigmahat5d,muci5d,sigmaci5d]=normfit(bitrate_q5d)

y4=[muhat1d,muhat2d,muhat3d,muhat4d,muhat5d]
err_y4=[(muci1d(1)-muhat1d),(muci2d(1)-muhat2d),(muci3d(1)-muhat3d),(muci4d(1)-muhat4d),(muci5d(1)-muhat5d)]
bitrate_all5 = csvread('qual_hitratio_BOLA_glob_qual.csv', 0);
bitrate_q1e = bitrate_all5(:,1);
bitrate_q2e = bitrate_all5(:,2);
bitrate_q3e = bitrate_all5(:,3);
bitrate_q4e = bitrate_all5(:,4);
bitrate_q5e = bitrate_all5(:,5);
%y=[bitrate_q1,bitrate_q2,bitrate_q3,bitrate_q4,bitrate_q5]
 
[muhat1e,sigmahat1e,muci1e,sigmaci1e]=normfit(bitrate_q1e)
[muhat2e,sigmahat2e,muci2e,sigmaci2e]=normfit(bitrate_q2e)
[muhat3e,sigmahat3e,muci3e,sigmaci3e]=normfit(bitrate_q3e)
[muhat4e,sigmahat4e,muci4e,sigmaci4e]=normfit(bitrate_q4e)
[muhat5e,sigmahat5e,muci5e,sigmaci5e]=normfit(bitrate_q5e);

y5=[muhat1e,muhat2e,muhat3e,muhat4e,muhat5e]

err_y5=[(muci1e(1)-muhat1e),(muci2e(1)-muhat2e),(muci3e(1)-muhat3e),(muci4e(1)-muhat4e),(muci5e(1)-muhat5e)]
y=[y1;y2;y3;y4;y5]
err_y=[err_y1;err_y2;err_y3;err_y4;err_y5]
numgroups=size(y, 1);
numbars = size(y, 2);
groupwidth = min(0.8, numbars/(numbars+1.5));
figure
h=bar((y),'hist')
hold on
for i = 1:numbars
      % Based on barweb.m by Bolu Ajiboye from MATLAB File Exchange
      x = (1:numgroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*numbars);  % Aligning error bar with individual bar
      errorbar(x, (y(:,i)), err_y(:,i), 'k', 'linestyle', 'none','HandleVisibility','off','CapSize',4);
    
end
set(h(1),'FaceColor',[255/255 160/255 122/255])
set(h(2),'FaceColor',[205/255 175/255 149/255])
set(h(3),'FaceColor',[205/255 133/255 63/255])
set(h(4),'FaceColor',[139/255 115/255 85/255])
set(h(5),'FaceColor',[139/255 87/255 66/255])
Labels = {'Baseline', 'Local','Global_{fullrep}', 'Global_{norep}','Quality'}
set(gca, 'XTick', 1:5, 'XTickLabel', Labels);
title('Cache Hit Rate (BOLA(O))')
set(gca,'fontsize',12)
%xlabel('Algorithm')
ylabel('Hit Rate (C_{hr})')
ylim([0,1])
% Add a legend
legend('Q_{1}', 'Q_{2}', 'Q_{3}', 'Q_{4}','Q_{5}','show','Location','northwest')
saveas(gcf, figname1, 'fig')
