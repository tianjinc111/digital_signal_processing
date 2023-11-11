
%% read_wavefile_01.m
% View parameters, plot waveform, compute and display spectrum

%% Load .wav file 

clear
[x, Fs] = audioread('question_eight.wav');   % or use wavread

whos
%%


soundsc(x(:,2),Fs)
%%
soundsc(x(1,:),Fs)

%% What is the quantization increment ?

% smallest positive value (SPV)

SPV = min(x(x > 0))

%%

% The smallest positive value is 1/2^15
1/SPV
2^15

%% Time axis in seconds

N = length(x);
t = (1:N)/Fs;

%channel 1
figure(1)
clf
plot(t, x(:,1))
xlabel('Time (sec)')
title('Channel 1')
%zoom in
xlim(0.4 + [0 0.005])
%%

%channel 2
figure(2)
clf
plot(t, x(:,2))
xlabel('Time (sec)')
title('Channel 2')
%zoom in
xlim(0.4 + [0 0.005])



%%
%channel 3
figure(3)
clf
plot(t, x(:,3))
xlabel('Time (sec)')
title('Channel 3')
%zoom in
xlim(0.4 + [0 0.005])



