#!/usr/bin/env python
# coding: utf-8

# # AIT Development notebook

# ## notebook of structure

# | #  | Name                                               | cells | for_dev | edit               | description                                                                |
# |----|----------------------------------------------------|-------|---------|--------------------|----------------------------------------------------------------------------|
# | 1  | [Environment detection](##1-Environment-detection) | 1     | No      | uneditable         | detect whether the notebook are invoked for packaging or in production     |
# | 2  | [Preparing AIT SDK](##2-Preparing-AIT-SDK)         | 1     | Yes     | uneditable         | download and install AIT SDK                                               |
# | 3  | [Dependency Management](##3-Dependency-Management) | 3     | Yes     | required(cell #2)  | generate requirements.txt for Docker container                             |
# | 4  | [Importing Libraries](##4-Importing-Libraries)     | 2     | Yes     | required(cell #1)  | import required libraries                                                  |
# | 5  | [Manifest Generation](##5-Manifest-Generation)     | 1     | Yes     | required           | generate AIT Manifest                                                      |
# | 6  | [Prepare for the Input](##6-Prepare-for-the-Input) | 1     | Yes     | required           | generate AIT Input JSON (inventory mapper)                                 |
# | 7  | [Initialization](##7-Initialization)               | 1     | No      | uneditable         | initialization for AIT execution                                           |
# | 8  | [Function definitions](##8-Function-definitions)   | N     | No      | required           | define functions invoked from Main area.<br> also define output functions. |
# | 9  | [Main Algorithms](##9-Main-Algorithms)             | 1     | No      | required           | area for main algorithms of an AIT                                         |
# | 10 | [Entry point](##10-Entry-point)                    | 1     | No      | uneditable         | an entry point where Qunomon invoke this AIT from here                     |
# | 11 | [License](##11-License)                            | 1     | Yes     | required           | generate license information                                               |
# | 12 | [Deployment](##12-Deployment)                      | 1     | Yes     | uneditable         | convert this notebook to the python file for packaging purpose             |

# ## notebook template revision history

# 1.0.1 2020/10/21
# 
# * add revision history
# * separate `create requirements and pip install` editable and noeditable
# * separate `import` editable and noeditable
# 
# 1.0.0 2020/10/12
# 
# * new cerarion

# ## body

# ### #1 Environment detection

# [uneditable]

# In[1]:


# Determine whether to start AIT or jupyter by startup argument
import sys
is_ait_launch = (len(sys.argv) == 2)


# ### #2 Preparing AIT SDK

# [uneditable]

# In[2]:


if not is_ait_launch:
    # get ait-sdk file name
    from pathlib import Path
    from glob import glob
    import re
    import os

    current_dir = get_ipython().run_line_magic('pwd', '')

    ait_sdk_path = "./ait_sdk-*-py3-none-any.whl"
    ait_sdk_list = glob(ait_sdk_path)
    ait_sdk_name = os.path.basename(ait_sdk_list[-1])

    # install ait-sdk
    get_ipython().system('pip install -q --upgrade pip')
    get_ipython().system('pip install -q --no-deps --force-reinstall ./$ait_sdk_name')


# ### #3 Dependency Management

# #### #3-1 [uneditable]

# In[3]:


if not is_ait_launch:
    from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator
    requirements_generator = AITRequirementsGenerator()


# #### #3-2 [required]

# In[4]:


if not is_ait_launch:
    requirements_generator.add_package('pandas','2.2.3')
    requirements_generator.add_package('matplotlib','3.7.3')


# #### #3-3 [uneditable]

# In[ ]:


if not is_ait_launch:
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -q -r $requirements_path ')


# ### #4 Importing Libraries

# #### #4-1 [required]

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# #### #4-2 [uneditable]

# In[ ]:


# must use modules
from os import path
import shutil  # do not remove
from ait_sdk.common.files.ait_input import AITInput  # do not remove
from ait_sdk.common.files.ait_output import AITOutput  # do not remove
from ait_sdk.common.files.ait_manifest import AITManifest  # do not remove
from ait_sdk.develop.ait_path_helper import AITPathHelper  # do not remove
from ait_sdk.utils.logging import get_logger, log, get_log_path  # do not remove
from ait_sdk.develop.annotation import measures, resources, downloads, ait_main  # do not remove
# must use modules


# In[ ]:


ITEM_CATEGORY='カテゴリ'
ITEM_REQLEVEL='要求レベル'
ITEM_CHECK='チェック'
reqlevel_items = ['Required','Lv1','Lv2','Lv3']
check_items = ['〇','×',np.nan,'－']
NONE='NONE'


# ### #5 Manifest Generation

# [required]

# In[ ]:


if not is_ait_launch:
## sample ##
     from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator
     manifest_genenerator = AITManifestGenerator(current_dir)
     manifest_genenerator.set_ait_name('eval_processcheck_problem_domain_analysis')
     manifest_genenerator.set_ait_description('機械学習品質マネジメントガイドライン第三版に従って、機械学習利用システムに用いるデータセットが問題領域分析の十分性を満たしているかをチェックリスト方式で審査する。'
                                              'チェックリストはhttps://github.com/aistairc/Qunomon_AIT_eval_processcheck_problem_domain_analysisからダウンロードできる。')
     manifest_genenerator.set_ait_source_repository('https://github.com/aistairc/Qunomon_AIT_eval_processcheck_problem_domain_analysis')
     manifest_genenerator.set_ait_version('0.2')
     manifest_genenerator.add_ait_keywords('checklist,sufficiency of problem domain')
     manifest_genenerator.set_ait_quality('https://ait-hub.pj.aist.go.jp/ait-hub/api/0.0.1/qualityDimensions/機械学習品質マネジメントガイドライン第三版/A-1問題領域分析の十分性')
     inventory_requirement_checklist = manifest_genenerator.format_ait_inventory_requirement(format_=['csv'])
     manifest_genenerator.add_ait_inventories(name='checklist', 
                                              type_='dataset', 
                                              description='問題領域分析の十分性のチェックリスト', 
                                              requirement=inventory_requirement_checklist)
     manifest_genenerator.add_ait_parameters(name='AISL', 
                                             type_='str', 
                                             description='外部品質特性レベルの一種。リスク回避性レベル', 
                                             default_val=NONE)
     manifest_genenerator.add_ait_parameters(name='AIPL', 
                                             type_='str', 
                                             description='外部品質特性レベルの一種。AIパフォーマンスレベル', 
                                             default_val=NONE)
     manifest_genenerator.add_ait_parameters(name='AIFL', 
                                             type_='str', 
                                             description='外部品質特性レベルの一種。公平性レベル', 
                                             default_val=NONE)
     manifest_genenerator.add_ait_measures(name='pass_fail', 
                                           type_='bool', 
                                           description='審査は次の2観点から判定される。1.要求レベルを満たす項目がすべて〇であること。2.要求レベルがRequiredの項目がすべて〇、もしくは－であること', 
                                           structure='single')
     manifest_genenerator.add_ait_downloads(name='Log', 
                                            description='AIT実行ログ')
     manifest_path = manifest_genenerator.write()


# ### #6 Prepare for the Input

# [required]

# In[ ]:


if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories(name='checklist',
                                        value='checklist.csv')
    input_generator.set_ait_params(name='AISL',value=NONE)
    input_generator.set_ait_params(name='AIPL',value='1.0')
    input_generator.set_ait_params(name='AIFL',value='1.0')
    input_generator.write()


# ### #7 Initialization

# [uneditable]

# In[ ]:


logger = get_logger()

ait_manifest = AITManifest()
ait_input = AITInput(ait_manifest)
ait_output = AITOutput(ait_manifest)

if is_ait_launch:
    # launch from AIT
    current_dir = path.dirname(path.abspath(__file__))
    path_helper = AITPathHelper(argv=sys.argv, ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)
else:
    # launch from jupyter notebook
    # ait.input.json make in input_dir
    input_dir = '/usr/local/qai/mnt/ip/job_args/1/1'
    current_dir = get_ipython().run_line_magic('pwd', '')
    path_helper = AITPathHelper(argv=['', input_dir], ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)

ait_input.read_json(path_helper.get_input_file_path())
ait_manifest.read_json(path_helper.get_manifest_file_path())

### do not edit cell


# ### #8 Function definitions

# [required]

# In[ ]:


# 要求レベルの判定
@log(logger)
def set_RequirementLevel(s_AISL, s_AIPL, s_AIFL):
    # validate
    try:
        # 初期値の場合は暫定的に(float化できる)'0'を入れる
        s_AISL = '0' if s_AISL==NONE else s_AISL
        s_AIPL = '0' if s_AIPL==NONE else s_AIPL
        s_AIFL = '0' if s_AIFL==NONE else s_AIFL
        
        AISL = float(s_AISL)
        AIPL = float(s_AIPL)
        AIFL = float(s_AIFL)
    except ValueError as e:
        print('Numerical conversion failed.')
        return -1
    
    
    # AISL 1 → Lv 3
    # AISL 2～4 → Lv 3 に追加すべき要求について、今後検討する。
    if AISL >=1:
        return 3.0
    
    # AISL 0.2 → Lv 2 以上
    # AIPL 2 → Lv 2 以上
    # AIFL 2 → Lv 2 以上
    elif (AISL>=0.2)or(AIPL>=2.0)or(AIFL>=2.0):
        return 2.0
    
    # AISL 0.1 → Lv 1 以上
    # AIPL 1 → Lv 1 以上
    # AIFL 1 → Lv 1 以上
    elif (AISL>=0.1)or(AIPL>=1.0)or(AIFL>=1.0):
        return 1.0
    
    # 内部品質レベル未定義
    elif (AISL==0)or(AIPL==0)or(AIFL==0):
        return 0.0 # Requiredのみ
    
    print('Unknown input level.')
    return -1


# In[ ]:


# チェックリストのバリデート
@log(logger)
def validate_input(checklist_table_data):
    
    returncode = 0
    
    # カテゴリのチェック
    num_cate = len(set(checklist_table_data[ITEM_CATEGORY]))
    if num_cate > 20:
        print('The category value has reached the upper limit.')
        print('num_cate:{}'.format(num_cate))
        returncode = -2
    
    # 要求レベルのチェック
    li_reqlevel = list(set(checklist_table_data[ITEM_REQLEVEL]))
    if not set(li_reqlevel) <= set(reqlevel_items):
        print('The request level is other than expected value.')
        print(li_reqlevel)
        returncode = -3
    
    # チェック項目のチェック
    li_check = list(set(checklist_table_data[ITEM_CHECK]))
    if not set(li_check) <= set(check_items):
        print('The check is other than expected value.')
        print(li_check)
        returncode = -4

    return returncode


# In[ ]:


# passチェック
@log(logger)
@measures(ait_output, 'pass_fail')
def pass_check(checklist_pickuped):
    '''
    pass条件
    1.要求レベルを満たす項目がすべて〇、もしくは－(×が含まれない)
    '''
    
    # －を除外
    checklist_pickuped = checklist_pickuped[checklist_pickuped[ITEM_CHECK]!=check_items[3]]
    
    df_pass = checklist_pickuped[checklist_pickuped[ITEM_CHECK]==check_items[0]] # 〇
    df_fail = checklist_pickuped[checklist_pickuped[ITEM_CHECK].isin(check_items[1:3])] # ×,空値はエラー扱い
    
    print('df_pass: {}'.format(len(df_pass)))
    print('df_fail: {}'.format(len(df_fail)))
    
    # 念のため2重チェック
    if len(df_fail) != 0:
        return False

    if len(df_pass) == len(checklist_pickuped):
        return True # pass
    
    return False


# In[ ]:


@log(logger)
@downloads(ait_output, path_helper, 'Log', 'ait.log')
def move_log(file_path: str=None) -> str:
    shutil.move(get_log_path(), file_path)


# ### #9 Main Algorithms

# [required]

# In[ ]:


@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:
    # チェックリストを読み取り
    print('\nInput data load.')
    checklist_table_data = pd.read_csv(ait_input.get_inventory_path('checklist'),
                                       usecols=['No.', 'カテゴリ', '要求レベル', 'チェック'],
                                       index_col=0)

    s_AISL = ait_input.get_method_param_value('AISL')
    s_AIPL = ait_input.get_method_param_value('AIPL')
    s_AIFL = ait_input.get_method_param_value('AIFL')
    
    # 入力チェック
    print('\nValidation.')
    if validate_input(checklist_table_data) != 0:
        return -1
    
    # 外部品質特性レベルから必要要求レベルを判定する
    print('\nSet Requirement level.')
    requirementlevel = set_RequirementLevel(s_AISL, s_AIPL, s_AIFL)
    if requirementlevel<=-1.0:
        return -1
    print('AISL:{}, AIPL:{}, AIFL:{}'.format(s_AISL, s_AIPL, s_AIFL))
    print('requirementlevel: {}'.format(requirementlevel))
    
    # 要求レベル該当項目の判定
    print('\nPickup.')
    if requirementlevel == 3.0:
        reqlevel_range = reqlevel_items
    elif requirementlevel == 2.0:
        reqlevel_range = reqlevel_items[:-1]
    elif requirementlevel == 1.0:
        reqlevel_range = reqlevel_items[:-2]
    else:
        reqlevel_range = reqlevel_items[:-3]
    print('reqlevel_range: {}'.format(reqlevel_range))
    
    checklist_pickuped = checklist_table_data[checklist_table_data[ITEM_REQLEVEL].isin(reqlevel_range)]
    print('number of pickup data: {}/{}'.format(len(checklist_pickuped), len(checklist_table_data)))
    print(checklist_pickuped)
    
    # 総合審査
    print('\nPass Check.')
    print('pass: {}'.format(pass_check(checklist_pickuped)))
    
    move_log()


# ### #10 Entry point

# [uneditable]

# In[ ]:


if __name__ == '__main__':
    main()


# ### #11 License

# [required]

# In[ ]:


## sample ##
ait_owner='AIST'
ait_creation_year='2023'


# ### #12 Deployment

# [uneditable] 

# In[ ]:


if not is_ait_launch:
    from ait_sdk.deploy import prepare_deploy
    from ait_sdk.license.license_generator import LicenseGenerator
    
    current_dir = get_ipython().run_line_magic('pwd', '')
    prepare_deploy(ait_sdk_name, current_dir, requirements_path)
    
    # output License.txt
    license_generator = LicenseGenerator()
    license_generator.write('../top_dir/LICENSE.txt', ait_creation_year, ait_owner)

