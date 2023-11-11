%% Compare time-domain waveforms...

clear

[x1, Fs] = audioread('author_AM.wav');
[x2, Fs] = audioread('author_AM_corrected.wav');

n = 1:length(x1);
t = n/Fs;

figure(1)
clf
subplot(2, 1, 1)
plot(t, x1, t, x2 - 0.3)
title('AM modulation by block processing')
legend('Discontinuity artifact', 'Correct version')
xlabel('Time (sec)')
zoom xon

orient landscape
print -dpdf author_AM-fig1


%%
% See discontinuities in x1

title('AM modulation by block processing (Detail)')
xlim([0.63 0.7])
ylim([-0.5 0.3])

print -dpdf author_AM-fig2


