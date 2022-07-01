# Standard Amazon Ads Metrics used throughout other report
def product_ads_metrics():
    dimensions = ['campaignName', 'adGroupName', 'asin', 'sku']

    core_metrics = ['impressions', 'clicks', 'cost', 'vctr', 'vtr']

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

    metrics = [dimensions, core_metrics, sales_metrics, order_metrics, conversion_metrics, new_to_brand_metrics]
    metrics = [','.join(x) for x in metrics]
    metrics = ','.join(metrics)

    return metrics


def search_term_metrics():
    dimensions = []

    core_metrics = ['impressions', 'clicks', 'cost', 'vctr', 'vtr']

    search_term_specific_metrics = ['searchTermImpressionRank', 'searchTermImpressionShare', 'query']

    keyword_metrics = ['keywordStatus', 'keywordText', 'matchType']

    uncategorized = ['targetingExpression', 'targetingText', 'targetingType']

    bid_metrics = ['keywordBid']

    conversion_metrics = ['attributedConversions1d', 'attributedConversions7d', 'attributedConversions14d', 'attributedConversions30d']

    new_to_brand_metrics = ['attributedOrderRateNewToBrand14d', 
                            'attributedOrdersNewToBrand14d', 
                            'attributedOrdersNewToBrandPercentage14d',
                            'attributedSalesNewToBrand14d',
                            'attributedSalesNewToBrandPercentage14d',
                            'attributedUnitsOrderedNewToBrand14d',
                            'attributedUnitsOrderedNewToBrandPercentage14d'
                            ]
    new_to_brand_metrics = ','.join(new_to_brand_metrics)

    metrics = [dimensions, core_metrics, search_term_specific_metrics, bid_metrics, keyword_metrics, conversion_metrics, new_to_brand_metrics, uncategorized]
    metrics = [','.join(x) for x in metrics]
    metrics = ','.join(metrics)

    return metrics