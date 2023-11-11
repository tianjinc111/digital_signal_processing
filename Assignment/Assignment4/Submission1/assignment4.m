
[x, Fs] = audioread('author.wav');

N = length(x);
n = 1:N;
t = n/Fs;

a = zeros(1, 801);
a(1) = 1.0;
b = zeros(1, 801);
b(1) = 1.0;
b(801) = 0.8;
% sound(x, Fs);



%% Make filter
% band-pass filter

%[b, a] = butter(2, [500 1000]*2/Fs)

%% Pole-zero diagram

figure(1)
clf
zplane(b, a)
title('Pole-zero diagram')








%% Impulse response
% discrete-time plot

L = 150;
imp = [1 zeros(1, L)];
h = filter(b, a, imp);

figure(2)
clf
stem(0:L, h)
xlabel('Discrete time (n)')
title('Impulse response')

%% Impulse response
% continuous-time plot

figure(4)
clf
plot((0:L)/Fs, h)
xlabel('Time (sec)')
title('Impulse response')
