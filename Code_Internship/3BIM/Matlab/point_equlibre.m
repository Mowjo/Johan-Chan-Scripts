%% Recherche des equilibres 

function simulation_output = sim_morrislecar()
%SIM_MORRISLECAR simule le modele de morrislecar

% Parametres du modele

I = 1000; % courant applique (muA/cm2)
duree = 200; % duree de l'application du courant

g_L  =   2; % conductance 'leak' (mS/cm2)
g_Ca =   4; % conductance Ca++   (mS/cm2)
g_K  =   8; % conductance K+     (mS/cm2)
V_L =  -50; % potentiel d'equilibre correspondant au conductancs 'leak' (mV)
V_Ca = 100; % potentiel d'equilibre correspondant au conductancs Ca++ (mV)
V_K =  -70; % potentiel d'equilibre correspondant au conductancs K+ (mV)
V1 =  10.0; % potentiel pour lequel M_ss = 0.5  (mV)
V2 =  15.0; % inverse de la pente de la dependence de voltage de M_ss (mV)
V3 =  -1.0; % potentiel pour lequel N_ss = 0.5  (mV)
V4 =  14.5; % inverse de la pente de la dependence de voltage de W_ss (mV)
C  =    20; % capacitance de la membranne (muF/cm2)
T0 =    15; % Constante de temps pour ouverture des canaux (ms) (1/lambda dans le papier)

par = [I, duree, g_L, g_Ca, g_K, V_L, ...
        V_Ca, V_K, V1, V2, V3, V4, C, T0];

function res = Null(X,par)
        res = (1/2)*(1+tanh((X-par(11))/par(12))) - (par(1) - par(3)*(X - par(6)) - par(4)*(1/2)*(1+tanh((X-par(9))/par(10)))*(X-par(7)))/(par(5)*(X-par(8)));
end

% options = optimoptions('fsolve','Display','iter');
fminsearch(@(X) Null(X, par), -20)
end
