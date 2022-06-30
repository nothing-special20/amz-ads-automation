# Standard Amazon Ads Metrics used throughout other report
def product_ads_metrics():
    dimensions = ['campaignName', 'adGroupName', 'asin', 'sku']
    dimensions = ','.join(dimensions)

    core_metrics = ['impressions', 'clicks', 'cost']
    core_metrics = ','.join(core_metrics)

    sales_metrics = ['attributedSales1d', 'attributedSales7d', 'attributedSales14d', 'attributedSales30d']
    sales_metrics = ','.join(sales_metrics)

    order_metrics = ['attributedUnitsOrdered1d', 'attributedUnitsOrdered7d', 'attributedUnitsOrdered14d', 'attributedUnitsOrdered30d']
    order_metrics = ','.join(order_metrics)

    conversion_metrics = ['attributedConversions1d', 'attributedConversions7d', 'attributedConversions14d', 'attributedConversions30d']
    conversion_metrics = ','.join(conversion_metrics)

    metrics = ','.join([dimensions, core_metrics, sales_metrics, order_metrics, conversion_metrics])

    return metrics