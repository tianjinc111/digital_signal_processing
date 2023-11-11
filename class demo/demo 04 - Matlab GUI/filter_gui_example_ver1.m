function filter_gui_example_ver1

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + 0.5 * randn(1, N);        % Input signal

figure(1)
clf
line_handle = plot(n, x);
title('Noisy data', 'fontsize', 12 )
xlabel('Time')
box off
xlim([0, N]);
ylim([-3 3])

drawnow;

uicontrol('Style', 'slider', ...
    'Min', 0.0, 'Max', 0.5,...
    'Value', 0.2, ...
    'SliderStep', [0.02 0.05], ...
    'Position', [5 5 200 20], ...           % [left, bottom, width, height]
    'Callback',  {@fun1, line_handle, x}    );

end


function fun1(hObject, eventdata, line_handle, x)

fc = get(hObject, 'Value');  % fc : cut-off frequency

fc = max(fc, 0.01);
fc = min(fc, 0.49);

% b, a : difference equation coefficients for Butterworth filter 
f1 = 700; 
f2 = 1000;
Fs = 600;
%[b, a] = butter(2, [f1, f2]*2/Fs);
[b, a] = butter(2, 2*fc);   % Order-2 Butterworth filter (multiply fc by 2 due to non-conventional Matlab convention)
y = filter(b, a, x);

[H, om] = freqz(b, a);

f_freqz = om*Fs/(2*pi);
subplot(1,2,1)
plot(f_freqz, abs(H))


title('Frequency response of filter')
xlabel('Frequency (Hz)')




[H, om] = impz(b, a);
f_freqz = om*500/(2*pi);
subplot(1,2,2)
plot(f_freqz, abs(H))
title('Impulse response of filter')
xlabel('Discrete Time')
% Update data in figure

title( sprintf('Output of LPF. Cut-off frequency = %.3f', fc), 'fontsize', 12 )

end

