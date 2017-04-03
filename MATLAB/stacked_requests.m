
%% Display Groups of Bars
% Display four groups of three bars.

% Copyright 2015 The MathWorks, Inc.

clear all
close all
figname1 = ['qual_tot_BOLA.fig']


colorVec ={[92/255 51/255 23/255],	[255/255 127/255 36/255], [255/255 20/255 147/255],[139/255 137/255 137/255]};
%colorVec=hsv(10)
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

% % % Playback bitrate
bitrate_all1 = csvread('stacked_bola.csv', 0);
bitrate_q1 = bitrate_all1(1:5);
bitrate_q2 = bitrate_all1(2:5);
bitrate_q3 = bitrate_all1(3:5);
bitrate_q4 = bitrate_all1(4:5);
bitrate_q5 = bitrate_all1(5:5);
%squad_y=[39716,657,54278,36019,139283;25082,35,9172,20074,215200;16767,151,21425,18235,213422;35557,14,17940,19499,196857;80525,1292,10947,43398,133467]
bola_y=[7202,16176,53928,77896,114691;4824,8316,31902,60482,164369;4839,8431,30465,44394,181835;4613,3756,11959,17310,232362;5914,8362,31540,70136,153921]
%y=[bitrate_q1;bitrate_q2;bitrate_q3;bitrate_q4;bitrate_q5]
%y=[2416,5501,18224,26130,37729;
%1287,2997,10136,20144,55329;
%1480,2361,8607,10662,66854;
%1542,850,1952,3145,82511;
%1809,1498,3962,9281,73332];
%y=[2416,5501,18224,26130,37729;
%1287,2997,10136,20144,55329;
%1480,2361,8607,10662,66854;
%1542,850,1952,3145,82511;
%1809,1498,3962,9281,73332];
figure 
h=bar(bola_y,'stacked')
%set(h(1),'FaceColor','b')
%set(h(2),'FaceColor','g')
%set(h(4),'FaceColor','g')
%set(h(5),'FaceColor','y')
Labels = {'Baseline', 'Local','Global_{fullrep}', 'Global_{norep}','Quality'}
set(gca, 'XTick', 1:5, 'XTickLabel', Labels);
ylabel('#Requests')
set(h(1),'FaceColor',[255/255 160/255 122/255])
set(h(2),'FaceColor',[205/255 175/255 149/255])
set(h(3),'FaceColor',[205/255 133/255 63/255])
set(h(4),'FaceColor',[139/255 115/255 85/255])
set(h(5),'FaceColor',[139/255 87/255 66/255])
%xlabel('Algorithm')
title('Total Requests by Quality (BOLA(O))')
ylim([0,290000])
set(gca,'fontsize',12)
% Add a legend
legend('Q_{1}', 'Q_{2}', 'Q_{3}', 'Q_{4}','Q_{5}','show','Location','northwest')
saveas(gcf, figname1, 'fig')
