
clear all
close all
figname1 = ['CDF_bitrat_squad_qual.fig']
figname2 = ['CDF_cntswitch_squad_qual.fig']
figname3 = ['CDF_magswitch_squad_qual.fig']
figname4 = ['CCDF_rebuffers_squad_qual.fig']
%cvec ={'m','k','[0.5 0.5 1]','[0.8 0.8 0]','[0.6 0.4 0]'};
%cvec ={'m','[0.8 0.8 0]'};
colorVec ={[92/255 51/255 23/255],	[255/255 127/255 36/255], [255/255 20/255 147/255],[108/255 123/255 139/255],[139/255 10/255 80/255]};
%colorVec=hsv(10)
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

% % % Playback bitrate
bitrate_all2 = csvread('abr_fullcap_rate_SQUAD_fr.csv', 1);
bitrate_sabr2 = bitrate_all2(:,2);
bitrate_all4 = csvread('abr_fullcap_rate_SQUAD_nr.csv', 1);
bitrate_sabr4 = bitrate_all4(:,2);
bitrate_all6 = csvread('abr_fullcap_rate_SQUAD.csv', 1);
bitrate_sabr6 = bitrate_all6(:,2);
bitrate_all8 = csvread('abr_fullcap_rate_SQUAD_qual.csv', 1);
bitrate_sabr8 = bitrate_all8(:,2);
bitrate_sabr9 = bitrate_all6(:,1);



mean_bitrate_sabr2 = mean(bitrate_sabr2)



mean_bitrate_sabr4 = mean(bitrate_sabr4)

mean_bitrate_sabr6 = mean(bitrate_sabr6)
mean_bitrate_sabr8 = mean(bitrate_sabr8)
mean_bitrate_sabr9 = mean(bitrate_sabr9)

[f_bitrate_sabr2,x_bitrate_sabr2,flo_bitrate_sabr2,fup_bitrate_sabr2]  = ecdf(bitrate_sabr2);
[f_bitrate_sabr4,x_bitrate_sabr4,flo_bitrate_sabr4,fup_bitrate_sabr4]  = ecdf(bitrate_sabr4);
[f_bitrate_sabr6,x_bitrate_sabr6,flo_bitrate_sabr6,fup_bitrate_sabr6]  = ecdf(bitrate_sabr6);
[f_bitrate_sabr8,x_bitrate_sabr8,flo_bitrate_sabr8,fup_bitrate_sabr8]  = ecdf(bitrate_sabr8);
[f_bitrate_sabr9,x_bitrate_sabr9,flo_bitrate_sabr9,fup_bitrate_sabr9]  = ecdf(bitrate_sabr9);


figure
plot(x_bitrate_sabr9,f_bitrate_sabr9,'-g','Linewidth',1.5,'MarkerSize',1,'DisplayName', ['SQUAD']);
hold on
plot(x_bitrate_sabr9,flo_bitrate_sabr9,':g','HandleVisibility','off');
plot(x_bitrate_sabr9,fup_bitrate_sabr9,':g','HandleVisibility','off');
plot(x_bitrate_sabr6,f_bitrate_sabr6,'--g','Linewidth',1.5,'MarkerSize',1,'DisplayName', ['SQUAD-Local']);
plot(x_bitrate_sabr6,flo_bitrate_sabr6,':g','HandleVisibility','off');
plot(x_bitrate_sabr6,fup_bitrate_sabr6,':g','HandleVisibility','off');
plot(x_bitrate_sabr2,f_bitrate_sabr2,'--','Linewidth',1.5,'Color',colorVec{2},'DisplayName', ['SQUAD-Global_{fullrep}']);
plot(x_bitrate_sabr2,flo_bitrate_sabr2,':','Color',colorVec{2},'HandleVisibility','off');
plot(x_bitrate_sabr2,fup_bitrate_sabr2,':','Color',colorVec{2},'HandleVisibility','off');
plot(x_bitrate_sabr4,f_bitrate_sabr4,'--','Linewidth',1.5,'Color',colorVec{4},'DisplayName', ['SQUAD-Global_{norep}']);
plot(x_bitrate_sabr4,flo_bitrate_sabr4,':','Color',colorVec{4},'HandleVisibility','off');
plot(x_bitrate_sabr4,fup_bitrate_sabr4,':','Color',colorVec{4},'HandleVisibility','off');
plot(x_bitrate_sabr8,f_bitrate_sabr8,'--','Color',colorVec{5},'Linewidth',1.5,'MarkerSize',1,'DisplayName', ['SQUAD-Quality']);
plot(x_bitrate_sabr8,flo_bitrate_sabr8,':','Color',colorVec{5},'HandleVisibility','off');
plot(x_bitrate_sabr8,fup_bitrate_sabr8,':','Color',colorVec{5},'HandleVisibility','off');
set(gca,'fontsize',12)
% ylim([1e-2,1])
% xlim([0,550])
l = legend('show','Location','Best');
% set(l,'Interpreter','Latex');
xlabel('Playback Bitrate [Mbps]')
ylabel('CDF')
f=gcf;
saveas(gcf, figname1, 'fig')

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

% % % Number of switches

nr_switches_all2 = csvread('abr_numofswitches_SQUAD_fr.csv', 1);
nr_switches_sabr2 = nr_switches_all2(:,2);
nr_switches_all4 = csvread('abr_numofswitches_SQUAD_nr.csv', 1);
nr_switches_sabr4 = nr_switches_all4(:,2);
nr_switches_all6 = csvread('abr_numofswitches_SQUAD.csv', 1);
nr_switches_sabr6 = nr_switches_all6(:,2);
nr_switches_all8 = csvread('abr_numofswitches_SQUAD_qual.csv', 1);
nr_switches_sabr8 = nr_switches_all8(:,2);
nr_switches_sabr9 = nr_switches_all6(:,1);


mean_nr_switches_sabr2 = mean(nr_switches_sabr2)
mean_nr_switches_sabr4 = mean(nr_switches_sabr4)
mean_nr_switches_sabr6 = mean(nr_switches_sabr6)
mean_nr_switches_sabr8 = mean(nr_switches_sabr8)
mean_nr_switches_sabr9 = mean(nr_switches_sabr9)

[f_nr_switches_sabr2,x_nr_switches_sabr2,flo_nr_switches_sabr2,fup_nr_switches_sabr2]  = ecdf(nr_switches_sabr2);
[f_nr_switches_sabr4,x_nr_switches_sabr4,flo_nr_switches_sabr4,fup_nr_switches_sabr4]  = ecdf(nr_switches_sabr4);
[f_nr_switches_sabr6,x_nr_switches_sabr6,flo_nr_switches_sabr6,fup_nr_switches_sabr6]  = ecdf(nr_switches_sabr6);
[f_nr_switches_sabr8,x_nr_switches_sabr8,flo_nr_switches_sabr8,fup_nr_switches_sabr8]  = ecdf(nr_switches_sabr8);
[f_nr_switches_sabr9,x_nr_switches_sabr9,flo_nr_switches_sabr9,fup_nr_switches_sabr9]  = ecdf(nr_switches_sabr9);

figure
plot(x_nr_switches_sabr9,1-f_nr_switches_sabr9,'-g','Linewidth',1.5,'DisplayName', ['SQUAD']);
hold on
plot(x_nr_switches_sabr9,1-flo_nr_switches_sabr9,':g','HandleVisibility','off');
plot(x_nr_switches_sabr9,1-fup_nr_switches_sabr9,':g','HandleVisibility','off');

plot(x_nr_switches_sabr6,1-f_nr_switches_sabr6,'--g','Linewidth',1.5,'DisplayName', ['SQUAD-Local']);

plot(x_nr_switches_sabr6,1-flo_nr_switches_sabr6,':g','HandleVisibility','off');
plot(x_nr_switches_sabr6,1-fup_nr_switches_sabr6,':g','HandleVisibility','off');
plot(x_nr_switches_sabr2,1-f_nr_switches_sabr2,'--','Linewidth',1.5,'Color',colorVec{2},'DisplayName', ['SQUAD-Global_{fullrep}']);
plot(x_nr_switches_sabr2,1-flo_nr_switches_sabr2,':','Color',colorVec{2},'HandleVisibility','off');
plot(x_nr_switches_sabr2,1-fup_nr_switches_sabr2,':','Color',colorVec{2},'HandleVisibility','off');
plot(x_nr_switches_sabr4,1-f_nr_switches_sabr4,'--','Linewidth',1.5,'Color',colorVec{4},'DisplayName', ['SQUAD-Global_{norep}']);
plot(x_nr_switches_sabr4,1-flo_nr_switches_sabr4,':','Color',colorVec{4},'HandleVisibility','off');
plot(x_nr_switches_sabr4,1-fup_nr_switches_sabr4,':','Color',colorVec{4},'HandleVisibility','off');
plot(x_nr_switches_sabr8,1-f_nr_switches_sabr8,'--','Color',colorVec{5},'Linewidth',1.5,'DisplayName', ['SQUAD-Quality']);
plot(x_nr_switches_sabr8,1-flo_nr_switches_sabr8,':','Color',colorVec{5},'HandleVisibility','off');
plot(x_nr_switches_sabr8,1-fup_nr_switches_sabr8,':','Color',colorVec{5},'HandleVisibility','off');
set(gca,'fontsize',12)
% ylim([1e-2,1])
xlim([0,120])
l = legend('show');
% set(l,'Interpreter','Latex');
xlabel('Nr of quality switches ')
ylabel('CCDF')
saveas(gcf, figname2, 'fig')
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 


% % % Number of switches
mag_switches_all2 = csvread('abr_magofswitches_SQUAD_fr.csv', 1);
mag_switches_sabr2 = mag_switches_all2(:,2);
mag_switches_all4 = csvread('abr_magofswitches_SQUAD_nr.csv', 1);
mag_switches_sabr4 = mag_switches_all4(:,2);
mag_switches_all6 = csvread('abr_magofswitches_SQUAD.csv', 1);
mag_switches_sabr6 = mag_switches_all6(:,2);
mag_switches_all8 = csvread('abr_magofswitches_SQUAD_qual.csv', 1);
mag_switches_sabr8 = mag_switches_all8(:,2);
mag_switches_sabr9 = mag_switches_all6(:,1);

mean_mag_switches_sabr2 = mean(mag_switches_sabr2)
mean_mag_switches_sabr4 = mean(mag_switches_sabr4)
mean_mag_switches_sabr6 = mean(mag_switches_sabr6)
mean_mag_switches_sabr8 = mean(mag_switches_sabr8)
mean_mag_switches_sabr9 = mean(mag_switches_sabr9)



[f_mag_switches_sabr2,x_mag_switches_sabr2,flo_mag_switches_sabr2,fup_mag_switches_sabr2]  = ecdf(mag_switches_sabr2);
[f_mag_switches_sabr4,x_mag_switches_sabr4,flo_mag_switches_sabr4,fup_mag_switches_sabr4]  = ecdf(mag_switches_sabr4);
[f_mag_switches_sabr6,x_mag_switches_sabr6,flo_mag_switches_sabr6,fup_mag_switches_sabr6]  = ecdf(mag_switches_sabr6);
[f_mag_switches_sabr8,x_mag_switches_sabr8,flo_mag_switches_sabr8,fup_mag_switches_sabr8]  = ecdf(mag_switches_sabr8);
[f_mag_switches_sabr9,x_mag_switches_sabr9,flo_mag_switches_sabr9,fup_mag_switches_sabr9]  = ecdf(mag_switches_sabr9);


figure
plot(x_mag_switches_sabr9,1-f_mag_switches_sabr9,'-g','Linewidth',1.5,'DisplayName', ['SQUAD']);
hold on
plot(x_mag_switches_sabr9,1-flo_mag_switches_sabr9,':g','HandleVisibility','off');
plot(x_mag_switches_sabr9,1-fup_mag_switches_sabr9,':g','HandleVisibility','off');
plot(x_mag_switches_sabr6,1-f_mag_switches_sabr6,'--g','Linewidth',1.5,'DisplayName', ['SQUAD-Local']);

plot(x_mag_switches_sabr6,1-flo_mag_switches_sabr6,':g','HandleVisibility','off');
plot(x_mag_switches_sabr6,1-fup_mag_switches_sabr6,':g','HandleVisibility','off');
plot(x_mag_switches_sabr2,1-f_mag_switches_sabr2,'--','Linewidth',1.5,'Color',colorVec{2},'DisplayName', ['SQUAD-Global_{fullrep}']);

plot(x_mag_switches_sabr2,1-flo_mag_switches_sabr2,':','Color',colorVec{2},'HandleVisibility','off');
plot(x_mag_switches_sabr2,1-fup_mag_switches_sabr2,':','Color',colorVec{2},'HandleVisibility','off');
plot(x_mag_switches_sabr4,1-f_mag_switches_sabr4,'--','Linewidth',1.5,'Color',colorVec{4},'DisplayName', ['SQUAD-Global_{norep}']);
plot(x_mag_switches_sabr4,1-flo_mag_switches_sabr4,':','Color',colorVec{4},'HandleVisibility','off');
plot(x_mag_switches_sabr4,1-fup_mag_switches_sabr4,':','Color',colorVec{4},'HandleVisibility','off');
plot(x_mag_switches_sabr8,1-f_mag_switches_sabr8,'--','Linewidth',1.5,'DisplayName', ['SQUAD-Quality']);
plot(x_mag_switches_sabr8,1-flo_mag_switches_sabr8,':','Color',colorVec{5},'HandleVisibility','off');
plot(x_mag_switches_sabr8,1-fup_mag_switches_sabr8,':','Color',colorVec{5},'HandleVisibility','off');

set(gca,'fontsize',12)
% ylim([1e-2,1])
%xlim([0,400])
l = legend('show');
% set(l,'Interpreter','Latex');
xlabel('Spectrum')
ylabel('CCDF')
saveas(gcf, figname3, 'fig')
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

rebuffers_all2 = csvread('abr_rebuffers_SQUAD_fr.csv', 1);
rebuffers_sabr2 = rebuffers_all2(:,2);
rebuffers_all4 = csvread('abr_rebuffers_SQUAD_nr.csv', 1);
rebuffers_sabr4 = rebuffers_all4(:,2);
rebuffers_all6 = csvread('abr_rebuffers_SQUAD.csv', 1);
rebuffers_sabr6 = rebuffers_all6(:,2);


mean_rebuffers_sabr2 = mean(rebuffers_sabr2)
mean_rebuffers_sabr4 = mean(rebuffers_sabr4)
mean_rebuffers_sabr6 = mean(rebuffers_sabr6)
[f_rebuffers_sabr2,x_rebuffers_sabr2,flo_rebuffers_sabr2,fup_rebuffers_sabr2]  = ecdf(rebuffers_sabr2);
[f_rebuffers_sabr4,x_rebuffers_sabr4,flo_rebuffers_sabr4,fup_rebuffers_sabr4]  = ecdf(rebuffers_sabr4);
[f_rebuffers_sabr6,x_rebuffers_sabr6,flo_rebuffers_sabr6,fup_rebuffers_sabr6]  = ecdf(rebuffers_sabr6);


figure
plot(x_rebuffers_sabr2,1-f_rebuffers_sabr2,'--','Linewidth',1.5,'Color',colorVec{2},'DisplayName', ['SQUAD-Global_{fullrep}']);
hold on
plot(x_rebuffers_sabr2,1-flo_rebuffers_sabr2,':','Color',colorVec{2},'HandleVisibility','off');
plot(x_rebuffers_sabr2,1-fup_rebuffers_sabr2,':','Color',colorVec{2},'HandleVisibility','off');
plot(x_rebuffers_sabr4,1-f_rebuffers_sabr4,'--','Linewidth',1.5,'Color',colorVec{4},'DisplayName', ['SQUAD-Global_{norep}']);
plot(x_rebuffers_sabr4,1-flo_rebuffers_sabr4,':','Color',colorVec{4},'HandleVisibility','off');
plot(x_rebuffers_sabr4,1-fup_rebuffers_sabr4,':','Color',colorVec{4},'HandleVisibility','off');
plot(x_rebuffers_sabr6,1-f_rebuffers_sabr6,'--g','Linewidth',1.5,'DisplayName', ['SQUAD-Local']);
plot(x_rebuffers_sabr6,1-flo_rebuffers_sabr6,':g','HandleVisibility','off');
plot(x_rebuffers_sabr6,1-fup_rebuffers_sabr6,':g','HandleVisibility','off');

% ylim([1e-2,1])
% xlim([0,550])
l = legend('show');

% set(l,'Interpreter','Latex');
xlabel('Rebuffering Ratio [%]')
ylabel('CCDF')
saveas(gcf, figname4, 'fig')


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

