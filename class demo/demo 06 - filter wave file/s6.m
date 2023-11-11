clc
clear
close all

[y, Fs] = audioread('audio_Q2.wav');

%Raw
sound(y, Fs)
pause(5)
clear sound

T = 1/Fs;             % Sampling period       
L = length(y);        % Length of signal
t = (0:L-1)*T;        % Time vector

Y = fft(y);

P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1)
title('Raw')

%Band pass
b = filter1('bp', y, 'fs', Fs, 'fc', [1000 2500]);
sound(b, Fs)
pause(5)
audiowrite('band-pass.wav',b, Fs)

clear sound