
% Equation de Fisher : equation de réaction-diffusion dans laquelle le terme de réaction est une logistique
% diffusion : schema numerique implicite en temps et conditions de Dirichlet 
% reaction : schema numerique explicite en temps sur la diffusion


%%%%%%%%% paramètres de simulation 

clear all
clf

N = 300;     % nombre de points
dx = 1000/N;     % pas d'espace 

Tmax = 200;     % temps final
dt = 0.5;    % pas de temps 

nu = 0.5;     % coefficient de diffusion 

A = 0;         % initialisation des matrices
B = 0;
C = 0;

index1 = 0;    % initialisation de l'animation

%%%%%%%% definition de la fonction u en t=0      

u = zeros(N,1); 

for J = N/3 : 2*N/3,      % fonction creneau entre N/3 et 2N/3
    u(J) = 1; 
end 


%%%%%%%%% matrices de diffusion   

for I = 2 : N-1,
	B(I,I) = -2;
	B(I-1,I) = 1;
	B(I+1,I) = 1;
end

B(2,1) = 1;
B(N-1,N) = 1;

% conditions de Dirichlet

B(1,1) = -2;
B(N,N) = -2;

A = eye(N) - nu * (dt/(dx^2)) * B;

C = inv(A);


%%%%%%%%% boucle de calcul sur le temps  

for t = dt : dt : Tmax,  
    index1 = index1 + 1;

% Etape de reaction (EDO)

for I = 1 : N,
	u(I) = u(I)+ dt* (u(I)*(1-u(I)));
end

% Etape de diffusion

u = C*u;

% graphe de u

plot(u,'blue','LineWidth',2);
axis([0 N 0 1.2]);                % echelle des axes
drawnow;
MOVI(index1) = getframe; % creation de l'animation

end

