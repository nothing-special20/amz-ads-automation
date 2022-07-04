# Standard Amazon Ads Metrics used throughout other report
def product_ads_metrics_old():
    dimensions = ['campaignName', 'adGroupName', 'asin', 'sku']

    core_metrics = ['impressions', 'clicks', 'cost']

    sales_metrics = ['attributedSales1d', 'attributedSales7d', 'attributedSales14d', 'attributedSales30d']

    order_metrics = ['attributedUnitsOrdered1d', 'attributedUnitsOrdered7d', 'attributedUnitsOrdered14d', 'attributedUnitsOrdered30d']

    conversion_metrics = ['attributedConversions1d', 'attributedConversions7d', 'attributedConversions14d', 'attributedConversions30d']

    new_to_brand_metrics = ['attributedOrderRateNewToBrand14d', 
                            'attributedOrdersNewToBrand14d', 
                            'attributedOrdersNewToBrandPercentage14d',
                            'attributedSalesNewToBrand14d',
                            'attributedSalesNewToBrandPercentage14d',
                            'attributedUnitsOrderedNewToBrand14d',
                            'attributedUnitsOrderedNewToBrandPercentage14d'
                            ]

    metrics = [dimensions, core_metrics, sales_metrics, order_metrics, conversion_metrics]
    metrics = [','.join(x) for x in metrics]
    metrics = ','.join(metrics)

    return metrics

def product_ads_metrics():
    dimensions = ['campaignId', 'campaignName', 'campaignStatus', 'adGroupId', 'adGroupName', 'asin', 'sku']

    core_metrics = ['impressions', 'clicks', 'cost', 'campaignBudget', 'campaignBudgetType', 'currency']

    sales_metrics = ['attributedSales1d', 'attributedSales7d', 'attributedSales14d', 'attributedSales30d',
                       'attributedSales1dSameSKU', 'attributedSales7dSameSKU', 'attributedSales14dSameSKU', 'attributedSales30dSameSKU']

    order_metrics = ['attributedUnitsOrdered1d', 'attributedUnitsOrdered7d', 'attributedUnitsOrdered14d', 'attributedUnitsOrdered30d',
                       'attributedUnitsOrdered1dSameSKU', 'attributedUnitsOrdered7dSameSKU', 'attributedUnitsOrdered14dSameSKU', 'attributedUnitsOrdered30dSameSKU'] 

    conversion_metrics = ['attributedConversions1d', 'attributedConversions7d', 'attributedConversions14d', 'attributedConversions30d',
                           'attributedConversions1dSameSKU', 'attributedConversions7dSameSKU', 'attributedConversions14dSameSKU','attributedConversions30dSameSKU']

    new_to_brand_metrics = ['attributedOrderRateNewToBrand14d', 
                            'attributedOrdersNewToBrand14d', 
                            'attributedOrdersNewToBrandPercentage14d',
                            'attributedSalesNewToBrand14d',
                            'attributedSalesNewToBrandPercentage14d',
                            'attributedUnitsOrderedNewToBrand14d',
                            'attributedUnitsOrderedNewToBrandPercentage14d'
                            ]

    metrics = [dimensions, core_metrics, sales_metrics, order_metrics, conversion_metrics]
    metrics = [','.join(x) for x in metrics]
    metrics = ','.join(metrics)

    return metrics

def search_term_keyword_metrics_old():
    dimensions = ['keywordId']

    core_metrics = ['impressions', 'clicks', 'cost']

    keyword_metrics = ['keywordText', 'matchType'] #'keywordStatus',

    conversion_metrics = ['attributedConversions1d', 'attributedConversions7d', 'attributedConversions14d', 'attributedConversions30d']

    metrics = [dimensions, core_metrics, keyword_metrics, conversion_metrics]
    metrics = [','.join(x) for x in metrics]
    metrics = ','.join(metrics)

    return metrics

def search_term_keyword_metrics():
    dimensions = ['adGroupId', 'adGroupName', 'currency', 'campaignBudget', 'campaignBudgetType', 'campaignId', 'campaignName', 'campaignStatus']

    core_metrics = ['impressions', 'clicks', 'cost']

    keyword_metrics = ['keywordText', 'matchType', 'keywordText'] #'keywordStatus',

    conversion_metrics = ['attributedConversions1d', 'attributedConversions7d', 'attributedConversions14d', 'attributedConversions30d',
                            'attributedConversions1d', 'attributedConversions7dSameSKU', 'attributedConversions14dSameSKU',
                            'attributedConversions1dSameSKU', 'attributedConversions30dSameSKU']

    attributed_sales = ['attributedSales1d', 'attributedSales7d', 'attributedSales14d', 'attributedSales30d',
                        'attributedSales1dSameSKU', 'attributedSales7dSameSKU', 'attributedSales14dSameSKU', 'attributedSales30dSameSKU']

    attributed_orders = ['attributedUnitsOrdered1d', 'attributedUnitsOrdered7d', 'attributedUnitsOrdered14d', 'attributedUnitsOrdered30d',
                            'attributedUnitsOrdered1dSameSKU', 'attributedUnitsOrdered7dSameSKU' ,'attributedUnitsOrdered14dSameSKU', 'attributedUnitsOrdered30dSameSKU']


    metrics = [dimensions, core_metrics, attributed_sales, attributed_orders, keyword_metrics, conversion_metrics]
    metrics = [','.join(x) for x in metrics]
    metrics = ','.join(metrics)

    return metrics



def search_term_target_metrics():
    core_metrics = ['impressions', 'clicks', 'cost', 'vctr', 'vtr']

    search_term_specific_metrics = ['searchTermImpressionRank', 'searchTermImpressionShare', 'query']

    uncategorized = ['targetingExpression', 'targetingText', 'targetingType']

    bid_metrics = ['keywordBid']

    new_to_brand_metrics = ['attributedOrderRateNewToBrand14d', 
                            'attributedOrdersNewToBrand14d', 
                            'attributedOrdersNewToBrandPercentage14d',
                            'attributedSalesNewToBrand14d',
                            'attributedSalesNewToBrandPercentage14d',
                            'attributedUnitsOrderedNewToBrand14d',
                            'attributedUnitsOrderedNewToBrandPercentage14d'
                            ]