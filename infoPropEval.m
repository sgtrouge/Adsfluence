load('/data/iteration.mat','p_iu','renameRelationship')
[~,renameIndex] = sort(renameRelationship(:,2));
RRsorted = unique(renameRelationship(renameIndex,:),'rows');


%% 
for currentDataSet=1:4
    if(currentDataSet == 4)
        d = csvread('data/Tweet_Info_TGiving.csv');
    else
        filepath = ['data/Tweet_Info_' num2str(currentDataSet+1) '.csv'];
        d = csvread(filepath);
    end


d = d(d(:,4)<=2 | d(:,4)==9 ,:);
d(d(:,4)==9,4) = 3;

n1_2 = d(:,1);
n2_2 = d(:,2);
M2 = [n1_2; n2_2];   % stack user id columns
[~, ~, nodes2] = unique(M2);
renameRelationship2 = [M2, nodes2];
[~,renameIndex2] = sort(renameRelationship2(:,2));
RRsorted2 = unique(renameRelationship2(renameIndex2,:),'rows');
nrows2 = length(nodes2);
node1_2 = nodes2(1:nrows2/2);
node2_2 = nodes2(nrows2/2 + 1:end);
data_T2 = [node1_2, d(:,4)+1, ones(length(node1_2),1)];
tweeters2 = [node2_2, d(:,4)+1, ones(length(node2_2),1)];
tweeters2 = unique(tweeters2,'rows');
data_T2 = [data_T2; tweeters2];
pt = spconvert(data_T2)>0;

j = 0;
p_hat = 0*pt;
p_test = 0*pt;
for i=1:length(RRsorted2(:,1))
    originalIndex = find(RRsorted2(i,1)==RRsorted(:,1));
    if(~isempty(originalIndex))
        j = j+1;
        p_hat(j,:) = p_iu(RRsorted(originalIndex,2),:)>0.5;
        p_test(j,:) = pt(j,:);
    end
end
p_hat = p_hat(1:j,:);
p_test = p_test(1:j,:);
tp = sum(sum(p_hat+p_test==2));
fp = sum(sum(p_hat==1 & p_test==0));
fn = sum(sum(p_hat==0 & p_test==1));
testAccuracy(currentDataSet) = mean(mean(p_hat==p_test));
testPrecision(currentDataSet) = tp / (tp+fp);
testRecall(currentDataSet) = tp / (tp+fn);
testFscore(currentDataSet) = 2*tp / (2*tp+fp+fn);
predictedNumberRetweeters(currentDataSet) = sum(sum(p_hat));
actualNumberRetweeters(currentDataSet) = sum(sum(p_test));
end

barLabels={'Test Set 1','Test Set 2', 'Test Set 3', 'Test Set 4' };
bar([testAccuracy',testPrecision',testRecall',testFscore'])
set(gca,'xticklabel',barLabels)
legend('accuracy','precision','recall','F')
ylim([0 1])

figure
barLabels={'Test Set 1','Test Set 2', 'Test Set 3', 'Test Set 4' };
bar([predictedNumberRetweeters',actualNumberRetweeters'])
set(gca,'xticklabel',barLabels)
legend('Predicted Number of Retweeters','Actual Number of Retweeters')

%% 
load('data/iteration.mat','A')
load('data/F.mat','F')
alphas = A.*F;
[ir,influencers] = sort(sum(alphas,1),'descend');
topInfluencers = RRsorted(influencers,1);


%% 