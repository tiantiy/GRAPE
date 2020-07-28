import os.path as osp
import numpy as np
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import tikzplotlib

# pre_path = "./uci/mdi_results"
# methods = ["mean","knn","mice","svd","spectral","gain","gnn_mdi"]
# method_names = ["Mean","KNN","MICE","SVD","Spectral","GAIN","GRAPE"]
# comment = '_v2train0.7'
# colors = ['b', 'g', 'c', 'm', 'y', 'pink', 'blue']
# ylabel = "Feature Imputation Test MAE"
# plot_name = 'mdi_known0.7_bar'

pre_path = "./uci/y_results"
methods = ["mean","knn","mice","svd","spectral","gain","tree","gnn"]
method_names = ["Mean","KNN","MICE","SVD","Spectral","GAIN","Tree","GRAPE"]
comment = '_v2train0.7'
colors = ['b', 'g', 'c', 'm', 'y', 'pink', 'k', 'blue']
ylabel = "Label Prediction Test MAE"
plot_name = 'reg_known0.7_bar'

# pre_path = "./uci/mdi_results"
# methods = ["mean_v2train0.7splitrandom0.7test",
# 			"knn_v2train0.7splitrandom0.7test",
# 			"mice_v2train0.7splitrandom0.7test",
# 			"svd_v2train0.7splitrandom0.7test",
# 			"spectral_v2train0.7splitrandom0.7test",
# 			"gain_v2train0.7splitrandom0.7train",
# 			"gnn_mdi_v2train0.7splitrandom0.7traintest"
# 			]
# method_names = ["Mean","KNN","MICE","SVD","Spectral","GAIN","GRAPE"]
# comment = ''
# colors = ['b', 'g', 'c', 'm', 'y', 'pink', 'blue']
# ylabel = "Feature Imputation Test MAE"
# plot_name = 'mdi_known0.7split0.7_bar'

# pre_path = "./uci/mdi_results"
# methods = ["gnn_mdi_v2train0.7","gnn_mdi_v2train0.7known1.0"]
# method_names = ["GRAPE with edge dropout","GRAPE without edge dropout"]
# comment = ''
# colors = ['red', 'blue']
# ylabel = "Feature Imputation Test MAE"
# plot_name = 'mdi_known0.7dropout_bar'

# pre_path = "./uci/y_results"
# methods = ["gnn","gnn_mdi"]
# method_names = ["GRAPE End-to-End","GRAPE with Linear Regression"]
# comment = '_v2train0.7'
# colors = ['red', 'blue']
# ylabel = "Label Prediction Test MAE"
# plot_name = 'reg_known0.7n2n_bar'

data = {"Dataset":[],ylabel:[],"Method":[]}
datasets = ["concrete","energy","housing","kin8nm","naval","power",
			"protein","wine","yacht"]
base_method = methods[0]
seeds = [0,1,2,3,4]
norm_bases = np.zeros(len(datasets))
for i,dataset in enumerate(datasets):
	for seed in seeds:
		load_path = '{}/results/{}{}/{}/{}/'.format(pre_path,base_method, comment,dataset, seed)
		obj = joblib.load(load_path+'result.pkl')
		# if base_method.startswith('gnn_mdi'):
		if base_method == 'gnn':
			norm_bases[i] += obj['curves']['test_l1'][-1]
		else:
			norm_bases[i] += obj['mae']
	norm_bases[i] = norm_bases[i]/float(len(seeds))

for method,method_name in zip(methods,method_names):
	for i,dataset in enumerate(datasets):
		for seed in seeds:
			data["Method"].append(method_name)
			data["Dataset"].append(dataset)
			load_path = '{}/results/{}{}/{}/{}/'.format(pre_path,method, comment,dataset, seed)
			obj = joblib.load(load_path+'result.pkl')
			# if method.startswith('gnn_mdi'):
			if method == 'gnn':
				data[ylabel].append(obj['curves']['test_l1'][-1]/norm_bases[i])
			elif method.startswith('gain'):
				# data[ylabel].append(obj['mdi_mae']/norm_bases[i])
				data[ylabel].append(obj['reg_mae']/norm_bases[i])
			else:
				data[ylabel].append(obj['mae']/norm_bases[i])
df = pd.DataFrame(data=data)

import seaborn as sns
sns.set(style="ticks", font_scale=3)
plt.figure(figsize=(20,7))
ax = sns.barplot(x="Dataset", y=ylabel, hue="Method", data=df, palette=colors,
				 errwidth=0.8)
plt.legend(loc='right', bbox_to_anchor=(1.25, 0.5), ncol=1)
# plt.legend(loc='upper center', bbox_to_anchor=(1.25, 0.5), ncol=1)
plt.savefig("{}/plots/{}.png".format(pre_path,plot_name), dpi=150, bbox_inches='tight')
plt.savefig("{}/plots/{}.pdf".format(pre_path,plot_name), bbox_inches='tight')
# tikzplotlib.save("{}/plots/{}.tex".format(pre_path,plot_name))
