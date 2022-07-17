import re

def django_static_file_ref_update(file):
    data = open(file, 'r').read()
    file_paths = re.findall('".{1,255}?"', data)
    file_paths = [re.sub('"', '', x) for x in file_paths]
    keep_file_exts = ['.css', '.js', '.svg', '.png']
    keep_file_exts = ['\\' + x for x in keep_file_exts]
    keep_file_exts = '|'.join(keep_file_exts)

    file_exts = []
    for x in file_paths:
        try:
            file_exts.append(re.search('\\..{1,5}',x).group(0))
        except:
            pass

    file_exts = list(set(file_exts))

    file_paths = [x for x in file_paths if bool(re.findall(keep_file_exts, x))]
    file_paths = [x for x in file_paths if x[0]!='.']
    file_paths = list(set(file_paths))

    for x in file_paths:
        print('~~~~~~')
        print(x)
        new_path = "{% static '" + x + "' %}"
        data = re.sub(x, new_path, data)
        print(new_path)
    
    new_file = file.split('.')
    new_file = new_file[0] + '_NEW.' + new_file[1]

    f = open(new_file, "w")
    f.write(data)
    f.close()

import re
def change_case(str):
    res = [str[0].lower()]
    for c in str[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ012346789'):
            res.append('_')
            res.append(c)
        else:
            res.append(c)
    output = ''.join(res).upper()
    output = re.sub('S_K_U', 'SKU', output)
    output = re.sub('1_4', '14', output)
    output = re.sub('3_0', '30', output)
    output = re.sub('Sku', 'SKU', output)
    output += ' = models.TextField()'
    return output

# Driver code

names = ['campaign_Id','campaignName','campaignStatus','adGroupId','adGroupName','asin','sku','impressions','clicks','cost','campaignBudget','campaignBudgetType','currency','attributedSales1d','attributedSales7d','attributedSales14d','attributedSales30d','attributedSales1dSameSKU','attributedSales7dSameSKU','attributedSales14dSameSKU','attributedSales30dSameSKU','attributedUnitsOrdered1d','attributedUnitsOrdered7d','attributedUnitsOrdered14d','attributedUnitsOrdered30d','attributedUnitsOrdered1dSameSKU','attributedUnitsOrdered7dSameSKU','attributedUnitsOrdered14dSameSKU','attributedUnitsOrdered30dSameSKU','attributedConversions1d','attributedConversions7d','attributedConversions14d','attributedConversions30d','attributedConversions1dSameSKU','attributedConversions7dSameSKU','attributedConversions14dSameSKU','attributedConversions30dSameSKU','date']
names = ['adGroupId','adGroupName','currency','campaignBudget','campaignBudgetType','campaignId','campaignName','campaignStatus','impressions','clicks','cost','attributedSales1d','attributedSales7d','attributedSales14d','attributedSales30d','attributedSales1dSameSKU','attributedSales7dSameSKU','attributedSales14dSameSKU','attributedSales30dSameSKU','attributedUnitsOrdered1d','attributedUnitsOrdered7d','attributedUnitsOrdered14d','attributedUnitsOrdered30d','attributedUnitsOrdered1dSameSKU','attributedUnitsOrdered7dSameSKU','attributedUnitsOrdered14dSameSKU','attributedUnitsOrdered30dSameSKU','keywordText','matchType','keywordText','query*','attributedConversions1d','attributedConversions7d','attributedConversions14d','attributedConversions30d','attributedConversions1d','attributedConversions7dSameSKU','attributedConversions14dSameSKU','attributedConversions1dSameSKU','attributedConversions30dSameSKU','date']
for x in names:
    print(change_case(x))

if __name__ ==  '__main__':
    path = ''
    django_static_file_ref_update(path)