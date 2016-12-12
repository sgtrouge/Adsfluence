function [I,P, influencers2] = IP_algorithm
filepath = 'data/thanksgivingretweet.txt';
[n1, n2] = textread(filepath,'%s %s');
M = [n2; n1];
[users, ~, nodes] = unique(M);
nrows = length(nodes);
node1 = nodes(1:nrows/2);
node2 = nodes(nrows/2 + 1:end);
Wfull = [node1,node2, ones(length(node1),1)];
[users2,~,rows] = unique(Wfull(:,1:2),'rows');
out = [users2, accumarray(rows,Wfull(:,3))];
W = spconvert(out);
[m,n] = size(W);
if m>n
    W(:,end+1:m) = sparse(zeros(m,m-n));
elseif n>m
    W(end+1:n,:) = sparse(zeros(n-m,n));
end
W = W/max(max(W));
n = max(m,n);
U = W;
V = (1-U)';
for j=1:n
    if(sum(U(:,j))~=0)
        U(:,j) = U(:,j)/sum(U(:,j));
    end
    if(sum(V(j,:))~=0)
        V(j,:) = V(j,:)/sum(V(j,:));
    end
end
[I,~] = eigs(U*V,1);
I = I/sum(I);
[P,~] = eigs(V*U,1);
P = P/sum(P);
[I,sortedI] = sort(I,'descend');
influencers2 = users(sortedI);
end

