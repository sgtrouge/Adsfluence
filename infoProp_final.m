clear
% import data
data = csvread('/Users/smasooman/Desktop/hits/tweet_data.csv');
% data = data(data(:,4)<=2 | data(:,4)==8 ,:);
% data(data(:,4)==8,4) = 3;
randindex = randsample(size(data,1),1000);
data = data(randindex,:);
data(:,3) = data(:,3)/(1e9);
data(:,3) = (data(:,3) - min(data(:,3)))/1+1;

% renumber id's
%% 
n1 = data(:,1);
n2 = data(:,2);
M = [n1; n2];   % stack user id columns
[users, ~, nodes] = unique(M); %  M = users(nodes)
nrows = length(nodes);
node1 = nodes(1:nrows/2);
node2 = nodes(nrows/2 + 1:end);
Wfull = [node1,node2, ones(length(node1),1)];
[users2,~,rows] = unique(Wfull(:,1:2),'rows');

% creating T matrix, T_ik = [time that user i retweeted topic k]
data_T = [node1, data(:,4)+1, data(:,3)];
tweeters = [node2, data(:,4)+1, data(:,3)/2];
tweeters = unique(tweeters,'rows');
data_T = [data_T; tweeters];
T = spconvert(data_T);
%data_T = [data_T; tweeters];
P = T>0;
T(T==0) = max(max(T));
T = full(T);

% creating P matrix
% P_ij = [1 if user i retweeted tweet/user/topic j, 0 otherwise], should we
%also use tweets?
% data_P = [node1, data(:,4)+1, ones(length(node1),1)];
% data_P = unique(data_P,'rows');
% P = spconvert(data_P);
% P = T<max(max(T))

% creating F matrix, F_ij = [1 if user i retweeted user j, 0 otherwise]
% data_F = [users2, accumarray(rows,Wfull(:,3))];
data_F = [users2, ones(size(users2,1),1)];
F = spconvert(data_F);
[fm,fn] = size(F);
if fm>fn
    F(:,end+1:fm) = sparse(zeros(fm,fm-fn));
elseif fn>fm
    F(end+1:fn,:) = sparse(zeros(fn-fm,fn));
end


% n = 10;
% m = 5;
% 
% % P_ij = [1 if user i retweeted tweet/user/topic j, 0 otherwise]
% P = rand(n,m) > .3;
% 
% % % T_ij = [time that user i retweeted tweet/user/topic j, 0 otherwise]
% T = 1e2*P.*rand(n,m);
% T(T==0) = 1e2;
% 
% % F_ij = [1 if user i follows user j, 0 otherwise]
% F = round(rand(n));
% F(eye(n)==1) = 0;


%Initialize X parameters
n = size(P,1);
m = size(P,2);
A = rand(n);
% Avar
G = rand(m,1);
B = rand(n,1);

%MU = rand(n,1);
MU = mean(T,2);
% SIG = rand(n,1);
SIG = sqrt(var(T,0,2));

%Initialize Partial Functions
dpdB = sparse(n,m);
dpdA = zeros(n,n,m);
%dpdA = zeros(n);
dpdMU = sparse(n,m);
dpdSIG = sparse(n,m);
dpdG = sparse(n,m);

%Initial P conditionaly values
P_ktp = zeros(n,n,m);
P_kfp = zeros(n,n,m);
% P_ktp = zeros(n);
% P_kfp = zeros(n);

%Iteration parameters
p_iu = sparse(n,m);
sqtp = sqrt(2*pi);
sqt = sqrt(2);
c = .1;
iteration = 0;
maxAccuracy = 0;
%load('/Users/smasooman/Desktop/hits/iteration.mat','A','G','B','MU','SIG')


%%
difference = 1;

while difference>1e-7
    iteration = iteration+1;
    disp(['Iteration ' num2str(iteration) ' has started.'])
    %pause(1)
    %Set old parameters
    A_old = A;
    G_old = G; 
    B_old = B;
    MU_old = MU;
    SIG_old = SIG;   
    A2 = A.*F;
    for u=1:m
        disp(['Iteration ' num2str(iteration) ', topic ' num2str(u) '.'])
        %Repeat the uth column of P,B
        P2 = repmat(P(:,u),1,n);
        B2 = repmat(B',n,1);
        
        %Find the product   
        p = 1-G(u)*A2.*P2;
        product = prod(p,2);
        %test = find(sum(p == 0,2));
        %test
        %Product with one term removed
        p2 = repmat(product,1,n)./p;
%         p2 = zeros(n);
%         for i=1:n
%            p2(:,i) = prod(p(:,1:end ~=i),2);
%         end     

        
        coeff = -(A2'.*P2);
        %Find the distribution parameters
        exponent = exp(-(-log(T(:,u))-MU)./((SIG*sqt).^2));
        errorfc = (1/2)*erfc((-log(T(:,u))-MU)./(SIG*sqt));
        errorfc2 = repmat(errorfc,1,n);
        
        %Solve for the partials
        dpdB(:,u) = G(u)*product;
        dpdA(:,:,u) = (G(u)*P2).*(1-G(u)*B2).*p2.*errorfc2;
%         dpdA = (G(u)*P2).*(1-G(u)*B2).*p2.*errorfc2;
        dpdMU(:,u) = (1-(1-G(u)*B).*product).*exponent./(SIG*sqtp);
        dpdSIG(:,u) = dpdMU(:,u).*(log(T(:,u))+MU)./(SIG.^2);
        dpdG(:,u) = B.*product.*errorfc + (G(u)*B-1).*errorfc.*(sum(coeff.*p2,2));
        p_iu(:,u) = (1-(1-G(u)*B).*product).*errorfc;
        
        P_ktp(:,:,u) = repmat(P(:,u)==1,1,n);
        P_kfp(:,:,u) = repmat(P(:,u)==0,1,n);
%         P_ktp = repmat(P(:,u)==1,1,n);
%         P_kfp = repmat(P(:,u)==0,1,n);
    end
    %Solve for k paramters
    ktp = sum(sum(p_iu(P==1)));
    kfp = sum(sum(p_iu(P==0)));
    kfn = sum(sum(1-p_iu(P==1)));
    den = 2*ktp+kfp+kfn;
    
    % Find the updated parameters
    A1 = den*2*(sum(dpdA.*P_ktp,3)) - ...
                2*ktp*(2*sum(dpdA.*P_ktp,3)+ sum(dpdA.*P_kfp,3));
    A = A + c*A1/(den^2);
    G = G + c*((den*2*(sum(dpdG.*P,1)) - 2*ktp*(sum(dpdG.*P,1)...
                +sum(dpdG.*(1-P),1))) / (den^2))';
    B = B + c*((den*2*(sum(dpdB.*P,2)) - 2*ktp*(sum(dpdB.*P,2)...
                +sum(dpdB.*(1-P),2))) / (den^2));
    MU = MU + c*((den*2*(sum(dpdMU.*P,2)) - 2*ktp*(sum(dpdMU.*P,2)...
                +sum(dpdMU.*(1-P),2))) / (den^2));
    SIG = SIG + c*((den*2*(sum(dpdSIG.*P,2)) - 2*ktp*(sum(dpdSIG.*P,2)...
                +sum(dpdSIG.*(1-P),2))) / (den^2));
    
    %Make sure values are within [0,1] range
    A(A<0) = 0;
    A(A>1) = 1;
    G(G<0) = 0;
    G(G>=1-10^(-7)) = 1-10^(-7);
    %G(G>1) = 1;
    B(B<0) = 0;
    B(B>1) = 1;
    MU(MU<0) = 0;
    SIG(SIG<0) = 0;
    
    diffA = norm(A_old-A,'fro');
    diffG = norm(G_old-G,'fro');
    diffB = norm(B_old-B,'fro');
    diffMU = norm(MU_old-MU,'fro');
    diffSIG = norm(SIG_old-SIG,'fro');
    diff = diffA + diffG + diffB + diffMU + diffSIG;

    testP = p_iu > 0.5;
    accuracy = mean(mean(testP==P));
    F = 2*ktp / den;
    disp(['Iteration ' num2str(iteration) ' complete.'])
    disp(['F(previous iteration) = ' num2str(F) '. Accuracy(previous iteration) = ' num2str(accuracy) '.'])
    disp(['Difference = ' num2str(diff) '.']);
    save('/Users/smasooman/Desktop/hits/iteration.mat','A','G','B','MU','SIG')
    disp(['Iteration ' num2str(iteration) ' data has been saved.'])
end
