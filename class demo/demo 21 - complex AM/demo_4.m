%% demo_4: Single sided filter.
% Create a single sided filter using a recursive filter.
% The filter passes positive frequencies and 
% stops negative frequencies.

%% Define recursive filter 

K = 4;
[b, a] = cheby2(K, 40, 0.5);

Nfft = 64;
H = fft(b, Nfft) ./ fft(a, Nfft);
f = (0:Nfft-1)/Nfft;
om = 2*pi*f;

figure(1)
clf
subplot(2, 1, 1)
zplane(b, a)
title('H(z)   [Z Transform]')

subplot(2, 1, 2)
plot(om - pi, fftshift(abs(H)))
title('|H(\omega)|   [Frequency response]')
xlabel('\omega')
xlim([-pi pi])
ylim([0 1.2])

print -dpdf figures/demo-4-1

%% Modulation
% Complex modulation.
% Shift the spectrum by 0.5 pi

I = sqrt(-1);
s = exp( I * 0.5 * pi * (0:K) );
% s = I.^(0:K);  % Equivalent

b2 = b .* s;    % filter coefficients are complex !
a2 = a .* s;

H2 = fft(b2, Nfft) ./ fft(a2, Nfft);

figure(1)
clf
subplot(2, 1, 1)
zplane(b2, a2)
title('H2(z)   [Z Transform]')

subplot(2, 1, 2)
plot(om - pi, fftshift(abs(H2)))
title('|H2(\omega)|   [Frequency response]')
xlabel('\omega')
xlim([-pi pi])
ylim([0 1.2])

print -dpdf figures/demo-4-2

%%
% The filter H2(z) = B2(z)/A2(z)
% passes positive frequencies and stops negative frequencies!

% We can use it to isolate the positive frequencies,
% then use complex signal modulation to shift the spectrum, 
% then take the real part.
% See next example...


