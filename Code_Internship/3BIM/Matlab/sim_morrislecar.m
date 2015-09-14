function simulation_output = sim_morrislecar()
%SIM_MORRISLECAR simule le modele de morrislecar

% Parametres du modele

clear all

I = 400; % courant applique (muA/cm2)
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
    
% Parametres de simulation
t0 = -20;
tfinal = 200;
tspan = [t0,tfinal];


% option de simulation
default = odeset()
options_1 = odeset('AbsTol',1e-9,'RelTol',1e-9);



% Conditions initiales
IC = [  -35;
        0];



% Lancement de la simulation

% sol = ode23(@(t,x) morrislecar(t,x,par),tspan,IC,default);
sol_precise = ode23(@(t,x) morrislecar(t,x,par),tspan,IC,options_1);

for i = 1:5
    intensite = i*100
    par(1) = intensite
    sol = ode23(@(t,x) morrislecar(t,x,par),tspan,IC,default);
    

% Retour Solution :

simulation_output = sol;

% Trace de la figure

figure(1); clf;
plot(sol.x,sol.y(1,:))
xlabel('temps (ms)')
ylabel('V (mV)')
axis tight

% Fonctions imbriquees
% ------------------------------------------------------------------

   function dxdt = morrislecar(t,x,par)
   % MORRIS LECAR : système EDO

       % variables dynamiques
       V = x(1);
       N = x(2);
       % equations differentielle
          if t < 0
              dxdt = [ ( 0 - par(3)*(V - par(6)) - par(4)*Mss(V)*(V-par(7)) - par(5)*N*(V - par(8)))/par(13) ;
       lambda(V)*(Nss(V)-N)];
          else
              
          dxdt = [ (par(1) - par(3)*(V - par(6)) - par(4)*Mss(V)*(V-par(7)) - par(5)*N*(V - par(8)))/par(13) ;
       lambda(V)*(Nss(V)-N)];
          end
             
    % Fonction imbriquees
    % --------------------------------------------------------------
    
        function res_1 = Mss(V)
        % Defini la fonction Mss
        
            res_1 = (1/2)*(1+tanh((V-par(9))/par(10)));
        end

        function res_2 = Nss(V)
        % Defini la fonction Nss
            
            res_2 = (1/2)*(1+tanh((V-par(11))/par(12)));
        end
        
       function res_3 = lambda(V)
       % Defini la fonction lambda
       
            res_3 = (1/par(14))*cosh([V-par(11)]/(2*par(12)))
       end
       
    % --------------------------------------------------------------
    
   end


% ------------------------------------------------------------------

end